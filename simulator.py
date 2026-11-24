"""Long-only paper simulation. Signals at close, fills at next open."""
from engine import indicators, signal, size
import pandas as pd

def backtest(frame, capital=10000, risk=.005, daily_limit=.01, slippage=.0005, halted=False):
    d=indicators(frame); cash=float(capital); pos=None; trades=[]; curve=[]; pending='WAIT'; day=None; baseline=cash; locked=False
    for i,(ts,r) in enumerate(d.iterrows()):
        today=ts.tz_convert('America/New_York').date()
        if today!=day:
            day=today; baseline=cash+(pos['qty']*r.open if pos else 0); locked=False; pending='WAIT'
        def close(price, reason):
            nonlocal cash,pos
            fill=float(price)*(1-slippage); cash+=pos['qty']*fill
            trades.append(dict(time=str(ts),entry=pos['entry'],exit=fill,shares=pos['qty'],pnl=pos['qty']*(fill-pos['entry']),reason=reason)); pos=None
        if pos and (pending=='SELL' or halted or locked): close(r.open,'exit signal / halt')
        if not pos and pending=='BUY' and not halted and not locked:
            entry=float(r.open)*(1+slippage); stop=entry*.99; qty=size(cash,cash,entry,stop,risk)
            if qty: cash-=qty*entry; pos=dict(entry=entry,stop=stop,target=entry*1.02,qty=qty)
        if pos:
            if r.low<=pos['stop']: close(min(r.open,pos['stop']),'stop')
            elif r.high>=pos['target']: close(pos['target'],'target')
        equity=cash+(pos['qty']*r.close if pos else 0)
        if equity<=baseline*(1-daily_limit):
            locked=True
            if pos: close(r.close,'daily loss threshold')
        last=i==len(d)-1 or d.index[i+1].tz_convert('America/New_York').date()!=today
        if last and pos: close(r.close,'session end')
        curve.append(cash+(pos['qty']*r.close if pos else 0)); pending=signal(d.iloc[:i+1]) if not last else 'WAIT'
    return pd.DataFrame(trades),pd.Series(curve,index=d.index,name='equity')
