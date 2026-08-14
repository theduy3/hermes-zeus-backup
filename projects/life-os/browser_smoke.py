import json
import urllib.request
from pathlib import Path

secrets = dict(x.split('=', 1) for x in (Path.home() / '.config/life-tracker/secrets.env').read_text().splitlines() if '=' in x)
login = urllib.request.Request(
    'http://127.0.0.1:8788/api/login',
    data=json.dumps({'password': secrets['BROWSER_PASSWORD']}).encode(),
    headers={'Content-Type': 'application/json'}, method='POST'
)
with urllib.request.urlopen(login) as response:
    cookie = response.headers['Set-Cookie'].split(';', 1)[0]
dashboard = urllib.request.Request('http://127.0.0.1:8788/api/dashboard', headers={'Cookie': cookie})
with urllib.request.urlopen(dashboard) as response:
    assert response.status == 200
html = urllib.request.urlopen('http://127.0.0.1:8788/').read().decode()
assert 'viewport' in html and 'min-height:44px' in html and '<form' not in html
print('browser cookie/read-only-data/a11y smoke: PASS')
