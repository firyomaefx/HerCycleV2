# HerCycleV2 🌸

A simple, private menstrual cycle tracker.

## Features

- **Add Entries** — Log cycle dates and symptoms
- **Edit Records** — Update or correct past entries
- **Monitor & Dashboard** — Visual overview of cycle patterns

## Prerequisites

- Python 3.8+
- Streamlit
- Pandas

## Installation

```bash
git clone <repo-url>
cd HerCycleV2
pip install -r requirements.txt
streamlit run app.py
```

## Deploy to Streamlit Cloud

1. Push this repository to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Click "New app" and select your repository
4. Set the main file path to `app.py`
5. Click "Deploy"

## Privacy

All cycle data is stored locally in `data/cycles.csv`. This folder is gitignored and never leaves your environment. No external API calls are made.

## License

Private (personal use).
