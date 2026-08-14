from bs4 import BeautifulSoup
from pathlib import Path
import sys, re
html=Path(sys.argv[1]).read_text(errors='ignore')
soup=BeautifulSoup(html,'html.parser')
for tag in soup(['script','style','nav','footer','header','noscript','svg']): tag.decompose()
main=soup.find('main') or soup.find('article') or soup.body or soup
text=main.get_text('\n')
lines=[]
for line in text.splitlines():
    line=re.sub(r'\s+',' ',line).strip()
    if not line: continue
    if line in lines[-4:]: continue
    lines.append(line)
Path(sys.argv[2]).write_text('\n'.join(lines)+'\n')
print(sys.argv[2], len(lines))
