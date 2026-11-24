# Trading Copilot — v0.1 research prototype
No live or simulated order execution is implemented. The dashboard calculates hypothetical plans only. Not a validated strategy. No automatic scanning, backtest, persistence, or daily loss controls yet. Terraform provisions ECR and a log group only, not compute. Never expose Streamlit publicly without authentication.

## Local setup
Python 3.12 recommended. Create a virtual environment, install `pip install -r requirements.txt`, copy `.env.example` to `.env`, then `streamlit run app.py`. Demo mode needs no keys. Windows: activate with `.venv\Scripts\Activate.ps1`.

## Schwab
Register at https://developer.schwab.com/products/trader-api--individual and request Market Data Production access. Register the exact HTTPS callback in `.env`; wait for approval. Run `python auth_setup.py` and follow the browser instructions. Do not share token files or credentials. Reauthorize when required. Select Schwab in dashboard and refresh. Quotes may be delayed; last candle timestamp is displayed. No broker order endpoints are invoked. Read the broker terms regarding data sharing before enabling AI explanations. AI receives the selected indicator snapshot, not credentials or account data. Configure OPENAI_MODEL and OPENAI_API_KEY only if desired.

## Docker
`docker build -t trading-copilot .` then `docker run --rm -p 127.0.0.1:8501:8501 trading-copilot` for demo. Use local Python for OAuth. Keep credentials outside images and source control.

## AWS foundation
With an authenticated AWS CLI, run `cd terraform && terraform init && terraform plan && terraform apply` after reviewing resources and costs. ECR and log storage may incur charges. `terraform destroy` removes the foundation (empty ECR first). No cloud runtime provisioned.

## Tests
`pip install pytest` then `python -m pytest -q`.

## Next milestones
Persistent paper fills with next-bar execution, slippage and commissions; daily loss limits, exchange calendar, stale-data detection, scanner and walk-forward backtests; authenticated private AWS compute; notifications and manual review of order proposals. Keep live ordering disabled until independent validation.

## v2 additions
Use the dashboard Watchlist scanner button to scan six symbols. Historical paper simulation uses completed-bar signals and next-open entries, modeled slippage, long-only positions, conservative stop-first handling and end-of-session exits. Turn off the emergency halt toggle to allow simulated entries. This is historical replay, not a continuous paper broker. The final bar of each supplied session is treated as session end, even for partial data. No fees, exchange calendar or liquidity model. Demo data is synthetic. No live orders are implemented.

Run `python scan_loop.py --mode demo --interval 300` for periodic read-only scans. Ctrl+C stops it. Schwab mode requires approved credentials and does not filter stale signals or market hours; do not use output for unattended execution.
