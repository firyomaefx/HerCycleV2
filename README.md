# HerCycleV2 🌸

A simple, private, and easy-to-use Streamlit web app for tracking and monitoring menstrual cycles. Designed for personal use on mobile phones.

## ✨ Features

- **Log Periods** — Quick entry with start/end dates and optional notes
- **Edit Records** — Update or delete past entries
- **Dashboard** — Cycle stats, phase detection, predictions, and trend charts
- **Export/Backup** — Download and import CSV data
- **Privacy First** — No external API calls. Data stays local in `data/cycles.csv` (gitignored)

## 🩸 Cycle Intelligence

- **Phase Detection** — Menstrual, follicular, ovulation, luteal (dynamically adapts to your cycle length)
- **Cycle Stats** — Average cycle length, variation, next period prediction
- **Fertile Window** — Estimated fertile window based on cycle data
- **PMS Alert** — Warning 7 days before predicted next period
- **Irregularity Warning** — Flags when cycle variation exceeds ±7 days

## 🚀 Quick Start

### Prerequisites

- Python 3.8+
- pip

### Installation

```bash
git clone https://github.com/firyomaefx/HerCycleV2.git
cd HerCycleV2
pip install -r requirements.txt
streamlit run app.py
```

### Deploy to Streamlit Cloud

1. Push this repository to GitHub (private repo recommended)
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Click **"New app"** and select your repository
4. Set the main file path to `app.py`
5. Click **"Deploy"**

## 📱 Live App

**https://hercyclev2.streamlit.app/**

Optimised for mobile use — big buttons, full-width cards, warm pink/cream theme.

## 📁 Project Structure

```
HerCycleV2/
├── app.py                  # Main Streamlit application
├── utils/
│   ├── __init__.py
│   └── data.py             # CRUD + statistics engine
├── data/
│   └── .gitkeep            # CSV storage (gitignored)
├── .streamlit/
│   └── config.toml          # Pink/cream theme config
├── .gitignore
├── requirements.txt
└── README.md
```

## 🔒 Privacy

- `data/cycles.csv` is gitignored — never committed to the repo
- No external API calls — all processing is local
- No accounts or login required
- CSV export/import for personal backup

## ⚙️ Tech Stack

| Component | Technology |
|-----------|-----------|
| Frontend | Streamlit |
| Data | Pandas (CSV) |
| Charts | Plotly |
| Theme | Custom pink/cream CSS |
| Deploy | Streamlit Cloud |

## 📝 Version History

See [Releases](https://github.com/firyomaefx/HerCycleV2/releases) for changelog.

## License

Private — personal use only.