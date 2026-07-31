/* West FW Living — early-list prompt (exit-intent desktop / scroll-depth mobile), once per session */
(function(){
  if (sessionStorage.getItem('wfl_prompted')) return;
  var shown=false;
  function show(){
    if(shown) return; shown=true;
    sessionStorage.setItem('wfl_prompted','1');
    var el=document.createElement('div');
    el.id='wfl-prompt';
    el.innerHTML='<div class="wfl-card" role="dialog" aria-label="Join the early list">'
      +'<button class="wfl-x" aria-label="Close">×</button>'
      +'<p class="wfl-k">BEFORE YOU GO</p>'
      +'<p class="wfl-h">Renewal season shouldn\u2019t ambush you.</p>'
      +'<p class="wfl-b">Drop your lease-end date on the early list \u2014 we\u2019ll send the market table when your 90-day window opens. Two fields, zero spam.</p>'
      +'<a class="wfl-btn" href="sms:+16822331426?&body=Add%20me%20to%20the%20West%20FW%20Living%20early%20list!%20My%20lease%20ends%3A%20___">Text to join \u2014 15 seconds</a></div>';
    document.body.appendChild(el);
    el.querySelector('.wfl-x').onclick=function(){el.remove();};
    el.onclick=function(e){if(e.target===el)el.remove();};
  }
  // desktop exit intent
  document.addEventListener('mouseout',function(e){
    if(!e.relatedTarget && e.clientY<8) show();
  });
  // mobile: 60% scroll depth, then 4s dwell
  var armed=false;
  window.addEventListener('scroll',function(){
    if(armed) return;
    var d=(window.scrollY+window.innerHeight)/document.body.scrollHeight;
    if(d>0.6){armed=true; setTimeout(show,4000);}
  },{passive:true});
})();
