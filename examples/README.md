# Examples

Two runnable scripts against a local or remote RIXL API.

## Setup

```bash
cd examples
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
```

## Run

```bash
export RIXL_API_KEY=<key>
export RIXL_BASE_URL=http://localhost:8081   # optional, defaults to https://api.rixl.com

python basic/main.py        # list images, fetch one by IMAGE_ID (X-API-Key)
python advanced/main.py     # full image and video upload pipelines (X-API-Key)
python bearer/main.py       # mint client JWT, then call with Bearer auth
```

The `bearer/` example needs `RIXL_CLIENT_ID`, `RIXL_CLIENT_SECRET`, `RIXL_PROJECT_ID`, and `RIXL_SUBJECT` instead of `RIXL_API_KEY`.
