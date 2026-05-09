import csv
import datetime
import os
import shutil
from pathlib import Path

import pandas as pd

DATA_DIR = Path(__file__).resolve().parent.parent / "data"
CSV_PATH = DATA_DIR / "cycles.csv"

COLUMNS = [
    "id", "start_date", "end_date", "duration",
    "notes", "created_at", "updated_at",
]

PHASES = {
    "menstrual": {"days": (1, 5), "emoji": "🩸", "description": "Menstrual phase - uterine lining sheds."},
    "follicular": {"days": (6, 13), "emoji": "🌱", "description": "Follicular phase - follicles develop and estrogen rises."},
    "ovulation": {"days": (14, 14), "emoji": "🥚", "description": "Ovulation - egg is released from the ovary."},
    "luteal": {"days": (15, 28), "emoji": "🌸", "description": "Luteal phase - progesterone rises, PMS may occur."},
}


def _ensure_csv():
    if not CSV_PATH.exists():
        CSV_PATH.parent.mkdir(parents=True, exist_ok=True)
        with open(CSV_PATH, "w", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(COLUMNS)


def _next_id() -> int:
    _ensure_csv()
    try:
        df = pd.read_csv(CSV_PATH)
    except pd.errors.EmptyDataError:
        return 1
    if df.empty:
        return 1
    return int(df["id"].max()) + 1


def _calc_duration(start_date, end_date):
    if start_date and end_date:
        d1 = pd.Timestamp(start_date)
        d2 = pd.Timestamp(end_date)
        return (d2 - d1).days + 1
    return None


def _now_str():
    return datetime.datetime.now().isoformat()


def add_entry(start_date, end_date=None, notes=""):
    _ensure_csv()
    entry_id = _next_id()
    duration = _calc_duration(start_date, end_date)
    now = _now_str()
    row = {
        "id": entry_id,
        "start_date": start_date,
        "end_date": end_date if end_date else "",
        "duration": duration if duration else "",
        "notes": notes,
        "created_at": now,
        "updated_at": now,
    }
    with open(CSV_PATH, "a", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=COLUMNS)
        writer.writerow(row)
    return row


def edit_entry(entry_id, start_date=None, end_date=None, notes=None):
    _ensure_csv()
    df = get_all_entries()
    mask = df["id"] == int(entry_id)
    if not mask.any():
        raise ValueError(f"Entry with id {entry_id} not found.")

    idx = df[mask].index[0]
    if start_date is not None:
        df.at[idx, "start_date"] = start_date
    if end_date is not None:
        df.at[idx, "end_date"] = end_date
    if notes is not None:
        df.at[idx, "notes"] = notes

    s = df.at[idx, "start_date"]
    e = df.at[idx, "end_date"]
    e = e if pd.notna(e) and str(e).strip() != "" else None
    df.at[idx, "duration"] = _calc_duration(s, e) if e else ""
    df.at[idx, "updated_at"] = _now_str()

    df.to_csv(CSV_PATH, index=False)
    return df.iloc[idx].to_dict()


def delete_entry(entry_id):
    _ensure_csv()
    df = get_all_entries()
    mask = df["id"] == int(entry_id)
    if not mask.any():
        return False
    df = df[~mask]
    df.to_csv(CSV_PATH, index=False)
    return True


def get_all_entries():
    _ensure_csv()
    try:
        df = pd.read_csv(CSV_PATH)
    except pd.errors.EmptyDataError:
        df = pd.DataFrame(columns=COLUMNS)
    if df.empty:
        return pd.DataFrame(columns=COLUMNS)
    df["start_date"] = pd.to_datetime(df["start_date"], errors="coerce")
    df["end_date"] = pd.to_datetime(df["end_date"], errors="coerce")
    df["created_at"] = pd.to_datetime(df["created_at"], errors="coerce")
    df["updated_at"] = pd.to_datetime(df["updated_at"], errors="coerce")
    df["duration"] = pd.to_numeric(df["duration"], errors="coerce").astype("Int64")
    return df.sort_values("start_date", ascending=False).reset_index(drop=True)


def get_cycle_stats(df=None):
    if df is None:
        df = get_all_entries()
    stats = {
        "avg_cycle": None,
        "std_cycle": None,
        "last_period": None,
        "next_predicted": None,
        "total_entries": len(df),
        "irregular": False,
    }
    if df.empty:
        return stats

    valid = df[df["start_date"].notna()].sort_values("start_date")
    if len(valid) < 2:
        last = valid.iloc[0]["start_date"]
        stats["last_period"] = last.strftime("%Y-%m-%d") if pd.notna(last) else None
        return stats

    diffs = valid["start_date"].diff().dropna().dt.days
    if len(diffs) == 0:
        return stats

    avg = diffs.mean()
    std = diffs.std(ddof=1) if len(diffs) > 1 else 0
    stats["avg_cycle"] = round(avg, 1)
    stats["std_cycle"] = round(std, 1)

    last_period = valid.iloc[-1]["start_date"]
    stats["last_period"] = last_period.strftime("%Y-%m-%d") if pd.notna(last_period) else None

    if avg > 0:
        next_date = last_period + pd.Timedelta(days=int(round(avg)))
        stats["next_predicted"] = next_date.strftime("%Y-%m-%d")

    if stats["total_entries"] >= 3 and (std > 5 or (avg > 0 and std / avg > 0.15)):
        stats["irregular"] = True

    return stats


def get_current_phase(df=None, today=None, avg_cycle=None):
    if df is None:
        df = get_all_entries()
    if today is None:
        today = datetime.date.today()

    today = pd.Timestamp(today)

    result = {
        "phase": None,
        "emoji": None,
        "day_in_cycle": None,
        "description": None,
        "fertile_window": None,
    }

    if df.empty or df["start_date"].isna().all():
        return result

    if avg_cycle is None:
        stats = get_cycle_stats(df)
        avg_cycle = stats["avg_cycle"] if stats["avg_cycle"] else 28

    last_period = df["start_date"].dropna().max()
    day_in_cycle = (today - last_period).days + 1

    if day_in_cycle < 1 or day_in_cycle > 60:
        return result

    result["day_in_cycle"] = day_in_cycle

    ovulation_day = avg_cycle - 14

    if 1 <= day_in_cycle <= 5:
        result["phase"] = "menstrual"
        result["emoji"] = PHASES["menstrual"]["emoji"]
        result["description"] = PHASES["menstrual"]["description"]
    elif 6 <= day_in_cycle <= ovulation_day - 1:
        result["phase"] = "follicular"
        result["emoji"] = PHASES["follicular"]["emoji"]
        result["description"] = PHASES["follicular"]["description"]
    elif day_in_cycle == ovulation_day:
        result["phase"] = "ovulation"
        result["emoji"] = PHASES["ovulation"]["emoji"]
        result["description"] = PHASES["ovulation"]["description"]
    elif ovulation_day + 1 <= day_in_cycle <= avg_cycle:
        result["phase"] = "luteal"
        result["emoji"] = PHASES["luteal"]["emoji"]
        result["description"] = PHASES["luteal"]["description"]
    else:
        result["phase"] = "luteal"
        result["emoji"] = PHASES["luteal"]["emoji"]
        result["description"] = "Extended luteal phase - cycle may be longer than average."

    fertile_start = last_period + pd.Timedelta(days=9)
    fertile_end = last_period + pd.Timedelta(days=15)
    result["fertile_window"] = (
        f"{fertile_start.strftime('%b %d')} – {fertile_end.strftime('%b %d')}"
    )

    return result


def export_csv():
    _ensure_csv()
    return str(CSV_PATH.resolve())


def import_csv(uploaded_file):
    _ensure_csv()
    temp_path = CSV_PATH.parent / "_temp_import.csv"
    with open(temp_path, "wb") as f:
        f.write(uploaded_file.getvalue())

    try:
        incoming = pd.read_csv(temp_path)
    except Exception:
        os.remove(temp_path)
        raise ValueError("Could not parse the uploaded CSV file.")

    existing = get_all_entries()
    existing_max_id = int(existing["id"].max()) if not existing.empty else 0

    if "id" not in incoming.columns:
        incoming.insert(0, "id", range(existing_max_id + 1, existing_max_id + 1 + len(incoming)))

    required = {"start_date"}
    if not required.issubset(set(incoming.columns)):
        os.remove(temp_path)
        raise ValueError("CSV must contain at least a 'start_date' column.")

    for col in COLUMNS:
        if col not in incoming.columns:
            incoming[col] = ""

    incoming["created_at"] = incoming["created_at"].replace("", _now_str())
    incoming["updated_at"] = incoming["updated_at"].replace("", _now_str())

    incoming = incoming[COLUMNS]

    merged = pd.concat([existing, incoming], ignore_index=True)

    for idx in merged.index:
        s = merged.at[idx, "start_date"]
        e = merged.at[idx, "end_date"]
        d = merged.at[idx, "duration"]
        if pd.notna(s) and pd.notna(e) and str(e).strip() != "" and (pd.isna(d) or str(d).strip() == ""):
            merged.at[idx, "duration"] = _calc_duration(s, e) if _calc_duration(s, e) else ""

    merged.to_csv(CSV_PATH, index=False)

    count = len(incoming)
    os.remove(temp_path)
    return count
