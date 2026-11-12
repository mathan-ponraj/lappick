# LaptopIQ — India Live Laptop Intelligence

A compact portfolio project that fetches current laptop listings from Croma through API.SH, normalizes the results with Pandas, summarizes listed prices, filters by brand, and exports CSV data.

## API details

- Provider: API.SH Croma API
- Endpoint: `GET https://api.api.sh/croma/v1/search`
- Authentication header: `x-api-key`
- Search parameter: `q` (for example, `laptop`)
- Other parameters used: `page`, `sort`
- API documentation: https://api.sh/croma-api

The API.SH page currently advertises 1,000 free credits per month for new accounts. Each Croma search request costs one credit according to its current documentation. Check the provider's pricing page before relying on the free allowance, because plans and quotas can change.

This is a third-party API that returns data from public Croma product pages. It is not an official Croma developer API.

## 1. Set up in VS Code

Open this project folder in VS Code, then run these commands in the terminal one at a time:

```powershell
python -m venv .venv
```

```powershell
.venv\Scripts\Activate.ps1
```

```powershell
pip install -r requirements.txt
```

## 2. Add your API key

Copy `.env.example` and rename the copy to `.env`.

Open `.env` and replace the placeholder:

```env
APISH_KEY=your_real_api_key
```

Do not add quotation marks. Never upload `.env` to GitHub.

## 3. Run LaptopIQ

```powershell
streamlit run app.py
```

Enter a search term such as `laptop`, `gaming laptop`, or `HP laptop`, choose a page and sort order, then select **Fetch latest listings**.

## Project structure

```text
LaptopIQ_India_Live_API/
├── app.py
├── requirements.txt
├── .env.example
├── .gitignore
├── README.md
├── src/
│   ├── __init__.py
│   ├── croma_client.py
│   └── data_utils.py
├── data/
│   └── .gitkeep
└── model/
    └── .gitkeep
```

## Notes about your existing XGBoost model

This API integration is intentionally kept separate from your historical ML training dataset. Croma search listings do not guarantee the same feature columns or a comparable `Rating` target as your original training CSV. Do not feed the live listings directly into the existing XGBoost model until the fields have been mapped and validated.

Keep your original `data/data.csv` and trained model files in a backup. This package does not contain your private dataset or trained model because those files were not attached to this chat.

## Data limitations

- Prices, discounts, stock and ratings can change.
- Search results may omit detailed processor/RAM/storage fields; the API's product-detail endpoint can be integrated later if needed.
- Treat the results as a current snapshot, not a guaranteed inventory or offer.
- Check API.SH terms, current quota and Croma's applicable terms before public/commercial use.
