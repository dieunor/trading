import pandas as pd
from simulator import backtest
from market import bars

def test_halt():
    trades,curve=backtest(bars('SPY','demo'),halted=True)
    assert trades.empty and (curve==10000).all()

def test_replay():
    trades,curve=backtest(bars('SPY','demo'))
    assert len(curve)==78 and curve.notna().all()
    assert abs(curve.iloc[-1]-10000-(trades.pnl.sum() if not trades.empty else 0))<1e-8
