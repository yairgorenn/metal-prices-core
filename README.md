\# Metal Prices API (Copper \& Aluminium)



Backend API for managing daily metal prices based on official LME data.



The system is designed to:

\- Receive validated daily metal prices from an external updater (Azure job)

\- Store the latest price per metal

\- Expose read-only endpoints for client applications (mobile / web)

\- Calculate final prices in ILS per kg based on EUR prices and exchange rates



This project is intentionally simple, stable, and deterministic.



---



\## Architecture Overview



\- \*\*FastAPI\*\* – REST API

\- \*\*SQLAlchemy ORM\*\*

\- \*\*SQLite\*\* for local development

\- \*\*PostgreSQL\*\* in production (Railway)

\- \*\*Token-based authentication\*\*

&nbsp; - One token for ingestion (write)

&nbsp; - One token for clients (read)



---



\## Endpoints



\### POST /ingest/metal-price



Used by the backend updater (Azure).



\*\*Headers\*\*



X-Token: INGEST\_TOKEN



\*\*Query Parameters\*\*

\- `metal` – Metal code (e.g. CU, AL)

\- `price\_eur\_per\_ton` – Metal price in EUR / ton

\- `eur\_to\_ils` – EUR → ILS exchange rate

\- `price\_date` – Price date (YYYY-MM-DD)



Stores or updates the latest price for the metal.



---



\### GET /prices/latest



Used by client applications.



\*\*Headers\*\*

X-Token: CLIENT\_TOKEN



\*\*Response\*\*

Returns the latest price per metal in:

\- ILS per kg

\- Last update date



---



\## Environment Variables



Required variables:





DATABASE\_URL

INGEST\_TOKEN

CLIENT\_TOKEN



Examples:



\### Local development



DATABASE\_URL=sqlite:///./dev.db





\### Production (Railway)



DATABASE\_URL=postgresql://...





---



\## Development



\### Setup

```bash

python -m venv venv

venv\\Scripts\\activate

pip install -r requirements.txt



Run locally

uvicorn app.main:app --reload



API Docs

http://127.0.0.1:8000/docs



Design Notes



Only the latest price per metal is stored



No historical pricing at this stage



Stability and predictability are preferred over complexity



Business logic is kept server-side to avoid client-side inconsistencies





