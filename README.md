# HerCycleV2 🌸

A private, modern menstrual cycle tracker with a premium glassmorphism UI.

**Live App:** https://hercyclev2.streamlit.app/

## ✨ Features

- **Log Periods** — Quick entry with start/end dates and optional notes
- **Edit Records** — Update or delete past entries with glass card UI
- **Dashboard** — Animated SVG phase ring, cycle stats, predictions, trend chart
- **Cycle Intelligence** — Dynamic phase detection, fertile window, PMS alerts
- **Export/Backup** — CSV download and import for data safety
- **Privacy First** — No external API calls. Data stays local in `data/cycles.csv`

## 🎨 UI Design

- **Glassmorphism** cards with frosted glass effect
- **Gradient background** (pink → lavender → cream)
- **Dark sidebar** with active state highlighting
- **Google Fonts** — Inter (body) + Playfair Display (headings)
- **Animated buttons** with hover/active effects
- **Custom scrollbar** and styled alerts
- **SVG phase ring** showing cycle progress
- **PWA-ready** manifest for home screen install

## 🩸 Cycle Intelligence

- **Phase Detection** — Menstrual, follicular, ovulation, luteal (adapts to your cycle length)
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

1. Push this repository to GitHub (public repo for Streamlit Cloud)
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Click **"New app"** and select your repository
4. Set the main file path to `app.py`
5. Click **"Deploy"**

## 📁 Project Structure

```
HerCycleV2/
├── app.py                  # Main Streamlit application
├── static/
│   ├── styles.css          # Modern glassmorphism CSS design system
│   └── manifest.json       # PWA manifest for home screen install
├── utils/
│   ├── __init__.py
│   └── data.py             # CRUD + statistics engine
├── data/
│   └── .gitkeep            # CSV storage (gitignored)
├── .streamlit/
│   └── config.toml         # Pink/cream theme config
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
| Frontend | Streamlit + Custom CSS (Glassmorphism) |
| Data | Pandas (CSV) |
| Charts | Plotly (custom pink theme) |
| Theme | Pink/cream gradient + dark sidebar |
| Fonts | Inter + Playfair Display (Google Fonts) |
| Deploy | Streamlit Cloud |

## 📝 Version History

### v2.1.0 — Mobile Responsive
- Changed layout from wide to centered for phone screens
- Sidebar starts collapsed on mobile
- Added responsive breakpoints (768px, 480px)
- 44px touch targets on buttons and inputs
- 16px input font to prevent iOS auto-zoom
- Compact glass cards and metrics on small screens
- CSS extracted to external static/styles.css
- PWA manifest + theme meta tags
- SVG phase ring guards against None values

### v2.0.0 — UI Redesign
- Complete glassmorphism redesign with gradient backgrounds
- Dark sidebar with active state highlighting
- Animated SVG phase ring showing cycle progress
- Google Fonts (Inter + Playfair Display)
- Glass cards, animated buttons, styled alerts
- Custom scrollbar in pink theme
- PWA manifest for home screen install
- CSS extracted to external file (static/styles.css)

### v1.0.0 — Initial Release
- Log periods, edit records, dashboard
- Dynamic phase detection, cycle stats, predictions
- CSV export/import, privacy-first design
- 20 QA tests passed

## License

Private — personal use only.