from engine import size,indicators,signal
from market import bars

def test_risk():
    assert size(10000,10000,100,99)==50
    assert size(100,10000,100,99)==1
    assert size(10000,10000,100,100)==0

def test_demo():
    d=indicators(bars('SPY','demo'))
    assert len(d)==78
    assert signal(d) in ('BUY','SELL','WAIT')
    assert d.vwap.notna().all()
