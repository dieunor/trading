import pandas as pd
import numpy as np
import math

def indicators(df):
    d=df.sort_index().copy(); c=d.close
    d['ema9']=c.ewm(span=9,adjust=False).mean(); d['ema21']=c.ewm(span=21,adjust=False).mean()
    delta=c.diff(); gain=delta.clip(lower=0).ewm(alpha=1/14,adjust=False,min_periods=14).mean(); loss=(-delta.clip(upper=0)).ewm(alpha=1/14,adjust=False,min_periods=14).mean()
    d['rsi']=100-100/(1+gain/loss.replace(0,np.nan)); d.loc[(loss==0)&(gain>0),'rsi']=100; d.loc[(loss==0)&(gain==0),'rsi']=50
    d['macd']=c.ewm(span=12,adjust=False).mean()-c.ewm(span=26,adjust=False).mean(); d['macd_signal']=d.macd.ewm(span=9,adjust=False).mean()
    day=d.index.tz_convert('America/New_York').date; v=d.volume.groupby(day).cumsum(); d['vwap']=(((d.high+d.low+c)/3*d.volume).groupby(day).cumsum()/v.replace(0,np.nan))
    return d

def signal(d):
    if len(d)<35: return 'WAIT'
    r=d.iloc[-1]
    if r.ema9>r.ema21 and r.close>r.vwap and 50<r.rsi<70 and r.macd>r.macd_signal: return 'BUY'
    if r.ema9<r.ema21 or r.close<r.vwap: return 'SELL'
    return 'WAIT'

def size(cash,equity,entry,stop,risk=.005):
    if not all(math.isfinite(x) for x in (cash,equity,entry,stop,risk)) or not (0<stop<entry and cash>0 and equity>0 and 0<risk<=.01): return 0
    return max(0,min(int(cash/entry),int(equity*risk/(entry-stop))))
