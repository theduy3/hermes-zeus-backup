import json, os, time, urllib.request, urllib.error
from pathlib import Path
BASE='http://127.0.0.1:8788'
S=dict(x.split('=',1) for x in (Path.home()/'.config/life-tracker/secrets.env').read_text().splitlines() if '=' in x)
def request(path, method='GET', data=None, bearer=False):
    r=urllib.request.Request(BASE+path, method=method)
    if bearer:r.add_header('Authorization','Bearer '+S['AGENT_TOKEN'])
    if data is not None:
        r.add_header('Content-Type','application/json');r.data=json.dumps(data).encode()
    return urllib.request.urlopen(r,timeout=3)
def main():
    try: request('/api/today')
    except urllib.error.HTTPError as e: assert e.code==401
    else: raise AssertionError('unauthorized access accepted')
    request('/api/habits','POST',{'id':'habit-focus','title':'Focused work','schedule':{'kind':'weekdays','days':[0,1,2,3,4]},'paused':False},True)
    x=json.loads(request('/api/today',bearer=True).read()); assert any(i['id']=='habit-focus' for i in x['items'])
    d=x['date']; request('/api/complete','POST',{'id':'habit-focus','day':d,'state':'completed'},True)
    x=json.loads(request('/api/today',bearer=True).read()); assert next(i for i in x['items'] if i['id']=='habit-focus')['completed']
    request('/api/metrics','POST',{'id':'energy','label':'Energy','kind':'rating','unit':'/10','min':1,'max':10,'aggregation':'mean','chart':'line','privacy':'private','missing':'unknown'},True)
    request('/api/observations','POST',{'id':'obs-energy-20260812','metric_id':'energy','day':d,'value':7,'estimated':False,'description':'explicit test observation'},True)
    dashboard=json.loads(request('/api/dashboard',bearer=True).read()); assert dashboard['metrics'][0]['coverage']>=1
    print('live smoke: PASS')
if __name__=='__main__': main()
