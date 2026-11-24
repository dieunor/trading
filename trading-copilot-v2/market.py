import os
import pandas as pd
import numpy as np
from dotenv import load_dotenv
load_dotenv()

def client():
    from schwab.auth import client_from_token_file
    return client_from_token_file(os.getenv('SCHWAB_TOKEN_PATH','data/token.json'),os.environ['SCHWAB_APP_KEY'],os.environ['SCHWAB_APP_SECRET'])

def bars(symbol,mode):
    if mode=='demo':
        rng=np.random.default_rng(sum(map(ord,symbol))); idx=pd.date_range('2025-01-06 09:30',periods=78,freq='5min',tz='America/New_York'); c=100+np.cumsum(rng.normal(.03,.25,len(idx)))
        return pd.DataFrame(dict(open=c,high=c+.15,low=c-.15,close=c,volume=rng.integers(100,10000,len(idx))),index=idx)
    from datetime import datetime,timedelta,timezone
    end=datetime.now(timezone.utc); response=client().get_price_history_every_five_minutes(symbol,start_datetime=end-timedelta(days=5),end_datetime=end,need_extended_hours_data=False); response.raise_for_status(); d=pd.DataFrame(response.json()['candles']); d.index=pd.to_datetime(d.pop('datetime'),unit='ms',utc=True); return d[d.index+pd.Timedelta(minutes=5)<=end].sort_index()
