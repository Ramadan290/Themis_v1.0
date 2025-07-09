""""

This file includes generating readable id formats and datetime formats i just seperated them for modularity

"""


from datetime import datetime
import uuid
import random
import string
import os
import sys
import contextlib


def generate_readable_user_id(user_id: int, role: str) -> str:
    """
    Converts raw user ID into readable format.
    EMP-00001, HR-00003, ADM-00012
    """
    prefix_map = {
        "employee": "EMP",
        "hr": "HR",
        "admin": "ADM"
    }
    prefix = prefix_map.get(role.lower(), "USR")
    return f"{prefix}-{str(user_id).zfill(5)}"


def generate_news_uid() -> str:
    return f"NEWS-{uuid.uuid4().hex[:8].upper()}"

def format_datetime(dt: datetime) -> str:
    """
    Converts a datetime object to a human-readable string.
    Format: YYYY-MM-DD HH:MM AM/PM
    Example: 2025-06-09 04:33 PM
    """
    return dt.strftime("%Y-%m-%d %I:%M %p")

def parse_date(date_str: str) -> datetime.date:
    """
    Converts a string (YYYY-MM-DD) to a date object.
    """
    return datetime.strptime(date_str, "%Y-%m-%d").date()



def generate_uid(prefix: str = "UID", length: int = 6) -> str:
    """
    Generate a unique identifier with a prefix.
    Format: <PREFIX>-<YYMMDD>-<RANDOM_STRING>
    Example: RR-250618-KZ4P1Q

    Args:
        prefix (str): A string to prefix the UID, like 'RR', 'NEWS', etc.
        length (int): Length of the random suffix.

    Returns:
        str: A unique UID string.
    """
    date_part = datetime.utcnow().strftime("%y%m%d")
    random_part = ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))
    return f"{prefix}-{date_part}-{random_part}"



@contextlib.contextmanager
def suppress_tf_lite_logs():
    original_stderr = sys.stderr
    with open(os.devnull, 'w') as devnull:
        sys.stderr = devnull
        try:
            yield
        finally:
            sys.stderr = original_stderr

@contextlib.contextmanager
def suppress_stderr():
    """Suppress stderr (used for TensorFlow native C++ warnings/info)."""
    with open(os.devnull, 'w') as devnull:
        old_stderr = sys.stderr
        sys.stderr = devnull
        try:
            yield
        finally:
            sys.stderr = old_stderr