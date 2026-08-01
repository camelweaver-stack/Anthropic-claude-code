// West FW Living — lite video embeds. ACTIVATE: paste real YouTube IDs below.
// Videos load only on tap (no iframe payload on page load — mobile budget safe).
window.WFLVIDEO = {
  rentReport: "",   // <- paste the latest monthly Rent Report video ID
  channelUrl: "https://www.youtube.com/@westfwliving" // <- confirm handle
};
window.WFLVIDEO.mount = function(elId, videoId, title){
  var el = document.getElementById(elId); if(!el) return;
  if(!videoId){ el.innerHTML = '<p class="tool-note">This month\'s video lands here with the next report — <a href="'+window.WFLVIDEO.channelUrl+'" rel="noopener">watch the channel</a> meanwhile.</p>'; return; }
  el.innerHTML = '<button type="button" class="vid-poster" aria-label="Play: '+title+'" style="position:relative;display:block;width:100%;border:1.5px solid var(--line);border-radius:14px;overflow:hidden;padding:0;cursor:pointer;background:#000">'+
    '<img src="https://i.ytimg.com/vi/'+videoId+'/hqdefault.jpg" alt="'+title+'" style="width:100%;display:block;opacity:.85" loading="lazy">'+
    '<span style="position:absolute;inset:0;display:flex;align-items:center;justify-content:center;font:600 16px Instrument Sans,sans-serif;color:#fff;text-shadow:0 1px 8px rgba(0,0,0,.7)">▶ '+title+'</span></button>';
  el.querySelector('button').onclick = function(){
    el.innerHTML = '<div style="position:relative;padding-top:56.25%;border-radius:14px;overflow:hidden"><iframe src="https://www.youtube-nocookie.com/embed/'+videoId+'?autoplay=1" title="'+title+'" allow="autoplay; encrypted-media" allowfullscreen style="position:absolute;inset:0;width:100%;height:100%;border:0"></iframe></div>';
  };
};
