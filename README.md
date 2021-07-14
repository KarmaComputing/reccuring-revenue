# Quickly see recurring revenue

## Setup & run locally
```
python3 -m venv venv
. venv/bin/activate
pip install -r requirements.txt
cp .env.example .env # and set to sandbox environment.
```

Setup endpoints in ./endoints/endpoints.json (see endpoints.json.example,  e.g.  endpoint `https://subscriptionwebsitebuilder.co.uk/open`)

### Run
uvicorn main:app --reload
```
Visit http://127.0.0.1:8000



