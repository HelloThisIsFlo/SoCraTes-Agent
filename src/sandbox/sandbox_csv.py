import pandas as pd
import requests

spreadsheet_id = "1dd73iBd5nV0l_7rH4BZX-_YNk0fDnoHaAbzyJU81goA"
sheet_id = "0"


def sheet_csv_url(spreadsheet_id: str, sheet_id: str) -> str:
    return f"https://docs.google.com/spreadsheets/d/{spreadsheet_id}/export?format=csv&gid={sheet_id}"


# Direct pandas read
df = pd.read_csv(sheet_csv_url(spreadsheet_id, sheet_id))
print(df)

# # Or with requests
# response = requests.get(sheet_csv_url(spreadsheet_id, sheet_id))
# csv_data = response.text
