from market import bars
from engine import indicators,signal

def scan(symbols, mode='demo'):
    rows=[]
    for symbol in symbols:
        try:
            d=indicators(bars(symbol,mode)); r=d.iloc[-1]
            rows.append(dict(symbol=symbol,price=float(r.close),rsi=float(r.rsi),signal=signal(d),timestamp=str(d.index[-1]),source=mode))
        except Exception as e: rows.append(dict(symbol=symbol,signal='UNAVAILABLE',error=type(e).__name__))
    return rows
