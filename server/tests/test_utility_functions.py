"""
Tests for utility functions.
"""
import pytest
import datetime
import sys
import os

# Add the server directory to the Python path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from routes.equipment import is_month_old, MONTH_LENGTH


class TestIsMonthOld:
    """Test the is_month_old utility function."""

    def test_is_month_old_recent_timestamp(self):
        """Test that recent timestamps are not considered old."""
        recent_timestamp = datetime.datetime.now() - datetime.timedelta(days=15)
        assert is_month_old(recent_timestamp) is False

    def test_is_month_old_exactly_one_month(self):
        """Test timestamp exactly one month old."""
        exactly_one_month = datetime.datetime.now() - datetime.timedelta(days=MONTH_LENGTH)
        assert is_month_old(exactly_one_month) is True

    def test_is_month_old_older_than_month(self):
        """Test timestamp older than one month."""
        older_timestamp = datetime.datetime.now() - datetime.timedelta(days=MONTH_LENGTH + 10)
        assert is_month_old(older_timestamp) is True

    def test_is_month_old_just_under_month(self):
        """Test timestamp just under one month old."""
        just_under_month = datetime.datetime.now() - datetime.timedelta(days=MONTH_LENGTH - 1)
        assert is_month_old(just_under_month) is False

    def test_is_month_old_future_timestamp(self):
        """Test future timestamp (should not be old)."""
        future_timestamp = datetime.datetime.now() + datetime.timedelta(days=1)
        assert is_month_old(future_timestamp) is False

    def test_is_month_old_edge_case_zero_days(self):
        """Test edge case with current timestamp."""
        current_timestamp = datetime.datetime.now()
        assert is_month_old(current_timestamp) is False

    def test_is_month_old_with_microseconds(self):
        """Test timestamp with microseconds precision."""
        timestamp_with_microseconds = datetime.datetime.now() - datetime.timedelta(
            days=MONTH_LENGTH,
            microseconds=1
        )
        assert is_month_old(timestamp_with_microseconds) is True

    def test_is_month_old_very_old_timestamp(self):
        """Test very old timestamp."""
        very_old_timestamp = datetime.datetime.now() - datetime.timedelta(days=365)
        assert is_month_old(very_old_timestamp) is True

    def test_is_month_old_constant_value(self):
        """Test that MONTH_LENGTH constant is used correctly."""
        # Test that the function uses the constant correctly
        timestamp_29_days_old = datetime.datetime.now() - datetime.timedelta(days=29)
        timestamp_31_days_old = datetime.datetime.now() - datetime.timedelta(days=31)

        # Since MONTH_LENGTH is 30, 29 days should be False, 31 days should be True
        assert is_month_old(timestamp_29_days_old) is False
        assert is_month_old(timestamp_31_days_old) is True
