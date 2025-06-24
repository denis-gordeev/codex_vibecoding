# Nendoroid Viewer Backend

This is the FastAPI backend for the Nendoroid Viewer project.

## Setup

1. Create a virtual environment and install dependencies:

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

2. Set the `DATABASE_URL` environment variable if necessary. The default is:
`postgresql+asyncpg://user:password@localhost/nendoroids`

3. Run the API:

```bash
uvicorn app.main:app --reload
```
