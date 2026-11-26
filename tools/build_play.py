# Builds the browser copy of the game for nanasgame.com/play from the game source.
#
#   python3 tools/build_play.py path/to/xmas-lights-app/game play path/to/fonts [levels]
#
# "levels" is how many levels the web demo allows (default 10 = District 1).
import re, shutil, sys, pathlib
src=pathlib.Path(sys.argv[1]); out=pathlib.Path(sys.argv[2]); fonts=pathlib.Path(sys.argv[3])
LIMIT=int(sys.argv[4]) if len(sys.argv)>4 else 10
FORM='https://docs.google.com/forms/d/e/1FAIpQLSdXcc9EGKCobpm0PpayjFovDhJnvt9fzfqe63KZqGMDl3-UOw/viewform'
if out.exists(): shutil.rmtree(out)
out.mkdir(parents=True)
for d in ['studio-kit','levels','city']: shutil.copytree(src/d, out/d)
shutil.copytree(fonts, out/'fonts')
html=(src/'index.html').read_text(encoding='utf8')
def patch(name, pat, rep):
    global html
    new,n=re.subn(pat, lambda m: rep, html, count=1)
    assert n==1, 'patch failed: '+name
    html=new
patch('preconnect', r'<link rel="preconnect" href="https://fonts\.googleapis\.com">\s*', '')
patch('fredoka', r'<link rel="stylesheet" href="https://fonts\.googleapis\.com/css2\?family=Fredoka[^"]*">', '<link rel="stylesheet" href="fonts/fonts.css">')
patch('fraunces', r'<link rel="stylesheet" href="https://fonts\.googleapis\.com/css2\?family=Fraunces[^"]*">\s*', '')
assert not re.search('googleapis|gstatic', html)
# web demo: test mode off, and every level start goes through the gate below
patch('test off', r'let TEST=[^;]*;', 'let TEST=false;')
patch('gate', r'function openJIntro\(i\)\{', 'function openJIntro(i){if(window.xlWebGate&&window.xlWebGate(i))return;')
html += '''
<style>
#bTest,#bGiftT,#testBadge,#jTest{display:none!important}
#xlGate{position:fixed;inset:0;z-index:9999;display:grid;place-items:center;padding:22px;background:rgba(10,10,32,.82);font-family:Fredoka,Nunito,system-ui,sans-serif}
#xlGate,#xlGate *{box-sizing:border-box}
#xlGate[hidden]{display:none}
#xlGate .box{width:min(340px,100%);padding:26px 22px 22px;border-radius:26px;background:#1d1a4a;box-shadow:0 0 0 3px #ffd23f,0 24px 60px rgba(0,0,0,.6);color:#f3f1ff;text-align:center}
#xlGate h2{margin:0;font-family:Fredoka,Nunito,system-ui,sans-serif;font-size:26px;line-height:1.1;font-weight:700;color:#ffd23f}
#xlGate p{margin:12px 0 0;font-family:Nunito,system-ui,sans-serif;font-size:16px;line-height:1.45;color:#cfcbf0}
#xlGate a,#xlGate button{display:block;width:100%;margin-top:14px;padding:14px 16px;border:0;border-radius:999px;font:700 17px Fredoka,system-ui,sans-serif;cursor:pointer;text-decoration:none}
#xlGate a{margin-top:20px;color:#201600;background:#ffd23f;box-shadow:0 4px 0 #b98700}
#xlGate button{color:#f3f1ff;background:transparent;box-shadow:inset 0 0 0 2px rgba(255,255,255,.2)}
</style>
<div id="xlGate" hidden role="dialog" aria-modal="true" aria-labelledby="xlGateH"><div class="box">
  <h2 id="xlGateH">That's the web demo</h2>
  <p>You can play the first __LIMIT__ levels here. The other __REST__ levels and the rest of the city are in the Android app.</p>
  <a href="__FORM__" target="_blank" rel="noopener">Become a tester</a>
  <button type="button" id="xlGateBack">Back to the map</button>
</div></div>
<script>
window.XL_WEB_LEVELS=__LIMIT__;
window.xlWebGate=function(i){
  if(i<window.XL_WEB_LEVELS)return false;
  var g=document.getElementById('xlGate');g.hidden=false;
  document.getElementById('xlGateBack').focus();
  return true;
};
document.getElementById('xlGateBack').onclick=function(){
  document.getElementById('xlGate').hidden=true;
  try{window.__nl.openMap()}catch(e){}
};
</script>
'''.replace('__LIMIT__',str(LIMIT)).replace('__REST__',str(60-LIMIT)).replace('__FORM__',FORM)
(out/'index.html').write_text(html, encoding='utf8')
print('play/ built, web demo =',LIMIT,'levels,', sum(f.stat().st_size for f in out.rglob('*') if f.is_file())//1024, 'KB')
