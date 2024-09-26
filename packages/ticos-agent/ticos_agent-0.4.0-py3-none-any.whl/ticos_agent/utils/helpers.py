import uuid


# Add any helper functions here
def format_bytes(bytes):
    """Convert bytes to human-readable format."""
    for unit in ["B", "KB", "MB", "GB", "TB"]:
        if bytes < 1024:
            return f"{bytes:.2f}{unit}"
        bytes /= 1024
    return f"{bytes:.2f}PB"


def get_mac_address():
    return ":".join(
        [
            "{:02x}".format((uuid.getnode() >> elements) & 0xFF)
            for elements in range(0, 2 * 6, 2)
        ][::-1]
    )
