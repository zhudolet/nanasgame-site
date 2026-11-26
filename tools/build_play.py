# Builds the browser copy of the game for nanasgame.com/play from the game source.
import re, shutil, sys, pathlib
src=pathlib.Path(sys.argv[1]); out=pathlib.Path(sys.argv[2]); fonts=pathlib.Path(sys.argv[3])
if out.exists(): shutil.rmtree(out)
out.mkdir(parents=True)
for d in ['studio-kit','levels','city']: shutil.copytree(src/d, out/d)
shutil.copytree(fonts, out/'fonts')
html=(src/'index.html').read_text(encoding='utf8')
def patch(name, pat, rep):
    global html
    new,n=re.subn(pat, rep, html, count=1)
    assert n==1, 'patch failed: '+name
    html=new
patch('preconnect', r'<link rel="preconnect" href="https://fonts\.googleapis\.com">\s*', '')
patch('fredoka', r'<link rel="stylesheet" href="https://fonts\.googleapis\.com/css2\?family=Fredoka[^"]*">', '<link rel="stylesheet" href="fonts/fonts.css">')
patch('fraunces', r'<link rel="stylesheet" href="https://fonts\.googleapis\.com/css2\?family=Fraunces[^"]*">\s*', '')
assert not re.search('googleapis|gstatic', html)
# web copy: the test-mode buttons stay out of the More menu; the site's "Tester tools" button switches test mode on
html += '\n<style>#bTest,#bGiftT{display:none!important}</style>\n'
(out/'index.html').write_text(html, encoding='utf8')
print('play/ built', sum(f.stat().st_size for f in out.rglob('*') if f.is_file())//1024, 'KB')
