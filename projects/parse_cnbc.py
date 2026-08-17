import json
d=json.load(open('cnbc.json'))
q=d.get('QuoteResponse',{}).get('Quotes',{})
if isinstance(q,dict): q=q.get('Quote',[])
if not isinstance(q,list): q=[q]
for x in q:
    sym=x.get('symbol')
    pe=x.get('peRatio')
    fpe=x.get('forwardPE') or x.get('forwardPeRatio')
    eps=x.get('eps')
    # print all keys containing pe/forward
    keys=[k for k in x.keys() if 'pe' in k.lower() or 'forward' in k.lower() or 'eps' in k.lower()]
    print(sym,'peRatio=',pe,'forwardPE=',fpe,'eps=',eps,'| pe-keys=',keys)
