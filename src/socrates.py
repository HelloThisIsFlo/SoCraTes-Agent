import pandas as pd

SOCRATES_SPREADSHEET_ID = "1dd73iBd5nV0l_7rH4BZX-_YNk0fDnoHaAbzyJU81goA"
SOCRATES_SHEET_ID = "0"


def sheet_csv_url(spreadsheet_id: str, sheet_id: str) -> str:
    return f"https://docs.google.com/spreadsheets/d/{spreadsheet_id}/export?format=csv&gid={sheet_id}"


def load_schedule_csv() -> pd.DataFrame:
    return pd.read_csv(sheet_csv_url(SOCRATES_SPREADSHEET_ID, SOCRATES_SHEET_ID))
