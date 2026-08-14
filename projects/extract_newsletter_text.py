from bs4 import BeautifulSoup
from pathlib import Path
import sys, re
for fname in sys.argv[1:]:
    html=Path(fname).read_text(errors='ignore')
    soup=BeautifulSoup(html,'html.parser')
    for tag in soup(['script','style','nav','footer','header','noscript','svg']): tag.decompose()
    main=soup.find('main') or soup.find('article') or soup.body or soup
    text=main.get_text('\n')
    lines=[]
    for line in text.splitlines():
        line=re.sub(r'\s+',' ',line).strip()
        if not line: continue
        if line in lines[-3:]: continue
        lines.append(line)
    print('===== FILE', fname, '=====')
    print('\n'.join(lines[:500]))
