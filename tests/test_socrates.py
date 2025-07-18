import pandas as pd
from datetime import datetime, date
from unittest.mock import patch, MagicMock
import pytest

from src.socrates import get_today_sessions, load_schedule_csv


def test_get_today_sessions_should_return_filtered_sessions_for_today():
    # Arrange - Create mock data with sessions for today and other days
    today_str = date.today().strftime("%Y-%m-%d")
    yesterday_str = "2025-01-15"  # Some past date

    mock_data = pd.DataFrame(
        {
            "title": ["Session A", "Session B", "Session C", "Session D"],
            "date": [today_str, yesterday_str, today_str, yesterday_str],
            "time": ["10:00", "14:00", "16:00", "09:00"],
            "loc.0": ["Room A", "Room B", "Room C", "Room D"],
            "people.0.name": ["John Doe", "Jane Smith", "Bob Wilson", "Alice Brown"],
        }
    )

    with patch("src.socrates.load_schedule_csv", return_value=mock_data):
        # Act - Call the function
        result = get_today_sessions()

        # Assert - Should return only today's sessions with correct structure
        assert len(result) == 2
        assert result[0]["title"] == "Session A"
        assert result[0]["time"] == "10:00"
        assert result[0]["room"] == "Room A"
        assert result[0]["session_owner"] == "John Doe"
        assert result[1]["title"] == "Session C"
        assert result[1]["time"] == "16:00"
        assert result[1]["room"] == "Room C"
        assert result[1]["session_owner"] == "Bob Wilson"


def test_get_today_sessions_should_return_empty_list_when_no_sessions_today():
    # Arrange - Create mock data with no sessions for today
    yesterday_str = "2025-01-15"  # Some past date

    mock_data = pd.DataFrame(
        {
            "title": ["Session A", "Session B"],
            "date": [yesterday_str, yesterday_str],
            "time": ["10:00", "14:00"],
            "loc.0": ["Room A", "Room B"],
            "people.0.name": ["John Doe", "Jane Smith"],
        }
    )

    with patch("src.socrates.load_schedule_csv", return_value=mock_data):
        # Act - Call the function
        result = get_today_sessions()

        # Assert - Should return empty list
        assert result == []


def test_get_today_sessions_should_handle_missing_data_gracefully():
    # Arrange - Create mock data with some missing values
    today_str = date.today().strftime("%Y-%m-%d")

    mock_data = pd.DataFrame(
        {
            "title": ["Session A", None, "Session C"],
            "date": [today_str, today_str, today_str],
            "time": ["10:00", "14:00", None],
            "loc.0": ["Room A", None, "Room C"],
            "people.0.name": ["John Doe", "Jane Smith", None],
        }
    )

    with patch("src.socrates.load_schedule_csv", return_value=mock_data):
        # Act - Call the function
        result = get_today_sessions()

        # Assert - Should return sessions with available data, handling NaN values
        assert len(result) == 3
        assert result[0]["title"] == "Session A"
        assert result[1]["title"] is None
        assert result[2]["session_owner"] is None
