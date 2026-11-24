"""Read-only periodic scanner; stop with Ctrl+C. Never places orders."""
import argparse,json,time
from scanner import scan
if __name__=='__main__':
    p=argparse.ArgumentParser(); p.add_argument('--mode',choices=['demo','schwab'],default='demo'); p.add_argument('--interval',type=int,default=300); a=p.parse_args()
    while True:
        print(json.dumps(scan(['SPY','QQQ','AAPL','MSFT','NVDA','TSLA'],a.mode)),flush=True)
        time.sleep(max(60,a.interval))
