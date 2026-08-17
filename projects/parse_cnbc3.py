import json
d=json.load(open('cnbc3.json'))
q=d['FormattedQuoteResult']['FormattedQuote'][0]
for k,v in q.items():
    if any(s in k.lower() for s in ['pe','forward','eps','yield','mkt','beta','div']):
        print(k,'=',v)
