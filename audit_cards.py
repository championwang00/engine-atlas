"""Report unlinked model-like prose and actual rendered preview use (not library size)."""
from pathlib import Path
from html.parser import HTMLParser
import re,json
ROOT=Path(__file__).resolve().parent
BRANDS='Honda|Toyota|Nissan|Mazda|Subaru|Mitsubishi|Suzuki|BMW|Mercedes|Benz|Audi|VW|Volkswagen|Porsche|Ferrari|Lamborghini|Alfa|Fiat|Lancia|Maserati|Ford|Chevrolet|Cadillac|Buick|Oldsmobile|Chrysler|Dodge|Plymouth|Packard|Duesenberg|Bugatti|Bentley|Rolls|Jaguar|Rover|Lotus|McLaren|Williams|Renault|Peugeot|Citroën|Saab|Volvo|Opel|DKW|Trabant|Wartburg|Cosworth|BRM|Cizeta|Marmon|Koenigsegg|Infiniti|Lexus|Hyundai|Kia|Matra|Brabham|Tyrrell|Benetton|Sauber|Red Bull|Haas|Aston|Mini|Smart|Daimler|Maybach|Stanley|Doble|Selden|Ricardo|Pescara'
PAT=re.compile(rf'(?<![A-Za-z])(?:{BRANDS})(?:[ \-][A-Za-z0-9][A-Za-z0-9.\-/]*){{0,4}}')
class Prose(HTMLParser):
 def __init__(self):super().__init__();self.stack=[];self.fragments=[];self.used={'term':set(),'car':set(),'entry':set()}
 def handle_starttag(self,tag,attrs):
  a=dict(attrs)
  if tag not in ['meta','link','input','img','br','hr','source']:self.stack.append((tag,a))
  for kind in self.used:
   if a.get('data-'+kind):self.used[kind].add(a['data-'+kind])
 def handle_endtag(self,tag):
  for i in range(len(self.stack)-1,-1,-1):
   if self.stack[i][0]==tag:self.stack=self.stack[:i];break
 def handle_data(self,data):
  tags=[t for t,a in self.stack]
  if any(a.get('class')=='en' for t,a in self.stack):return
  if 'main' in tags and not any(t in tags for t in ['script','style','nav','a','button','h1','h2','dt']):self.fragments.append(data)
missing={};allused={'term':set(),'car':set(),'entry':set()};localisation=[]
for path in sorted((ROOT/'zh').rglob('*.html')):
 p=Prose();p.feed(path.read_text());names=sorted({m[0].strip() for t in p.fragments for m in PAT.finditer(t) if ' ' in m[0] or '-' in m[0]})
 if names:missing[str(path.relative_to(ROOT))]=names
 for kind,ids in p.used.items():allused[kind]|=ids
for path in (ROOT/'en').rglob('*.html'):
 match=re.search(r'<script id="page-data" type="application/json">(.*?)</script>',path.read_text(),re.S)
 if not match:continue
 data=json.loads(match[1])
 for key,car in data.get('cars',{}).items():
  if re.search(r'[\u4e00-\u9fff]',car.get('name_en','')+car.get('brief_en','')) or 'referenced example of' in car.get('brief_en',''):
   localisation.append({'page':str(path.relative_to(ROOT)),'id':key})
report={'actual_prose_previews':{k:len(v) for k,v in allused.items()},'unlinked_model_candidates':missing,'english_preview_issues':localisation,'note':'Candidates include prose brand names and are a review queue, not confirmed missing entities. Navigation auto-enhanced previews are not included in these prose counts.'}
(ROOT/'work/preview-audit.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(report,ensure_ascii=False,indent=2))
