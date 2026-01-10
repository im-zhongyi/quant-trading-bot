from datetime import datetime

def generate_timestamp():
    # Get the current local date and time
    now = datetime.now()
    # Format as YYYYMMDDhhmmss
    timestamp = now.strftime("%Y%m%d%H%M%S")
    return timestamp