// Shared embed helper for atlas figures. A figure page defines window.FIG = { play(on), reset(), playing() }
// and puts its drawing in <svg id="fig">. With ?embed=1 the page shows only the drawing + a 54px control bar.
(() => {
  const q = new URLSearchParams(location.search), embed = q.has('embed'), en = q.get('lang') === 'en';
  const L = en ? {play: 'Play', pause: 'Pause', reset: 'Reset view', hint: 'Drag to orbit'} : {play: '播放', pause: '暂停', reset: '重置视角', hint: '拖动旋转'};
  document.documentElement.lang = en ? 'en' : 'zh-CN';
  const css = document.createElement('style');
  css.textContent = `html,body{margin:0;background:#d9d9d6;overflow:hidden}
  #fig{display:block;width:100vw;height:calc(100vh - 54px);touch-action:none;cursor:grab}
  .fig-controls{position:fixed;left:8px;right:8px;bottom:7px;display:flex;gap:5px;align-items:center;font:11px ui-monospace,monospace}
  .fig-controls button{min-height:44px;padding:7px 10px;color:#343432;background:#ebebeae8;border:1px solid #14141424;font:inherit;cursor:pointer}
  .fig-controls button:focus-visible{outline:2px solid #141414;outline-offset:2px}
  .fig-controls .hint{margin-left:auto;color:#44443f;background:#ebebead9;padding:5px}
  @media(max-width:440px){.fig-controls .hint{display:none}}`;
  document.head.append(css);
  const bar = document.createElement('div'); bar.className = 'fig-controls';
  const play = document.createElement('button'); play.type = 'button';
  const reset = document.createElement('button'); reset.type = 'button'; reset.textContent = L.reset;
  const hint = document.createElement('span'); hint.className = 'hint'; hint.textContent = L.hint;
  bar.append(play, reset, hint); document.body.append(bar);
  const sync = () => { const on = !!(window.FIG && window.FIG.playing()); play.textContent = on ? L.pause : L.play; play.setAttribute('aria-pressed', String(on)); };
  play.addEventListener('click', () => { window.FIG.play(!window.FIG.playing()); sync(); });
  reset.addEventListener('click', () => { window.FIG.reset(); sync(); });
  addEventListener('load', () => {
    const calm = matchMedia('(prefers-reduced-motion: reduce)').matches;
    if (window.FIG) window.FIG.play(!calm && !q.has('still'));
    sync();
  });
})();
