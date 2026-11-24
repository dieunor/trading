import os
from pathlib import Path
from dotenv import load_dotenv
from schwab.auth import client_from_manual_flow
load_dotenv(); p=Path(os.getenv('SCHWAB_TOKEN_PATH','data/token.json')); p.parent.mkdir(parents=True,exist_ok=True); os.umask(0o077)
client_from_manual_flow(os.environ['SCHWAB_APP_KEY'],os.environ['SCHWAB_APP_SECRET'],os.environ['SCHWAB_CALLBACK_URL'],str(p)); p.chmod(0o600)
