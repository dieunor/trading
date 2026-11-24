import os
import streamlit as st
from market import bars
from engine import indicators,signal,size
st.set_page_config(page_title='Trading Copilot',layout='wide')
st.title('Trading Copilot | Research & simulation')
mode=st.sidebar.radio('Data source',['demo','schwab'])
st.warning('SIMULATION ONLY — no live orders. Demo prices are synthetic. Signals are unvalidated.')
symbol=st.sidebar.selectbox('Symbol',['SPY','QQQ','AAPL','MSFT','NVDA','TSLA'])
capital=st.sidebar.number_input('Simulated capital',1000,1000000,10000)
if st.button('Load / refresh data') or 'frame' not in st.session_state or st.session_state.get('key')!=(mode,symbol):
    try: st.session_state.frame=indicators(bars(symbol,mode)); st.session_state.key=(mode,symbol)
    except Exception as e: st.error('Data unavailable; check credentials, token and API access. '+type(e).__name__); st.stop()
d=st.session_state.frame
if d.empty: st.error('No candles'); st.stop()
r=d.iloc[-1]; entry=float(r.close); stop=entry*.99; target=entry*1.02
st.caption(f'{symbol} | Last completed candle: {d.index[-1]} | Source: {mode}')
cols=st.columns(4)
for col,label,val in zip(cols,['Price','Rule signal','RSI','VWAP'],[f'${entry:.2f}',signal(d),f'{r.rsi:.1f}',f'{r.vwap:.2f}']): col.metric(label,val)
st.line_chart(d[['close','ema9','ema21','vwap']]); st.line_chart(d[['macd','macd_signal']])
qty=size(capital,capital,entry,stop)
st.write({'hypothetical_entry':round(entry,2),'stop':round(stop,2),'target':round(target,2),'shares':qty,'estimated_risk':round(qty*(entry-stop),2)})
if st.button('Explain signal with AI'):
    try:
        from openai import OpenAI
        response=OpenAI().responses.create(model=os.environ['OPENAI_MODEL'],input=f'Explain this historical rule-based signal for educational use. Do not recommend a trade or predict profits. Symbol {symbol}; signal {signal(d)}; indicators {r.to_dict()}')
        st.write(response.output_text)
    except Exception: st.error('AI unavailable; configure API key and model.')
st.caption('No execution engine in this version. Stop prices do not guarantee fills.')

st.header('Watchlist scanner')
from scanner import scan
from simulator import backtest
if st.button('Scan watchlist'):
    st.session_state.scan_rows=scan(['SPY','QQQ','AAPL','MSFT','NVDA','TSLA'],mode)
if 'scan_rows' in st.session_state: st.dataframe(st.session_state.scan_rows)
st.header('Historical paper simulation')
halted=st.toggle('Emergency halt (disable simulated entries)',value=True)
risk=st.slider('Risk per trade (%)',0.25,1.0,0.5)/100
limit=st.slider('Daily loss threshold (%)',0.5,3.0,1.0)/100
if st.button('Run historical simulation'):
    trades,curve=backtest(d,capital,risk,limit,halted=halted)
    st.metric('Ending simulated equity',f'${curve.iloc[-1]:,.2f}')
    st.line_chart(curve)
    st.dataframe(trades)
    st.download_button('Export simulated trades',trades.to_csv(index=False),'trades.csv')
st.caption('Historical replay only; no persistent positions or background order execution. Stops and loss thresholds are not guaranteed.')
