import pandas as pd
from datetime import date
from typing import List, Dict, Any

SOCRATES_SPREADSHEET_ID = "1dd73iBd5nV0l_7rH4BZX-_YNk0fDnoHaAbzyJU81goA"
SOCRATES_SHEET_ID = "0"


def sheet_csv_url(spreadsheet_id: str, sheet_id: str) -> str:
    return f"https://docs.google.com/spreadsheets/d/{spreadsheet_id}/export?format=csv&gid={sheet_id}"


def load_schedule_csv() -> pd.DataFrame:
    return pd.read_csv(sheet_csv_url(SOCRATES_SPREADSHEET_ID, SOCRATES_SHEET_ID))


def get_today_sessions() -> List[Dict[str, Any]]:
    """
    Return all sessions scheduled for today.

    Returns:
        List of dictionaries containing:
        - title: Session name
        - time: When it happens
        - room: Room location (from loc.0)
        - session_owner: Session owner name (from people.0.name)
    """
    df = load_schedule_csv()
    today_str = date.today().strftime("%Y-%m-%d")

    # Filter for today's sessions (comparing string dates)
    today_sessions = df[df["date"] == today_str]

    # Convert to list of dictionaries with the requested format
    sessions = []
    for _, row in today_sessions.iterrows():
        session = {
            "title": row["title"] if pd.notna(row["title"]) else None,
            "time": row["time"] if pd.notna(row["time"]) else None,
            "room": row["loc.0"] if pd.notna(row["loc.0"]) else None,
            "session_owner": (
                row["people.0.name"] if pd.notna(row["people.0.name"]) else None
            ),
        }
        sessions.append(session)

    return sessions
