import re
import socket


def is_cloud() -> bool:
    user_pattern = re.compile(
        r"^(vm)-"
        r"([0-9a-fA-F]{8}-"
        r"[0-9a-fA-F]{4}-"
        r"[0-9a-fA-F]{4}-"
        r"[0-9a-fA-F]{4}-"
        r"[0-9a-fA-F]{12})-"
        r"([a-zA-Z0-9]+)-"
        r"([a-zA-Z0-9]+)-"
        r"([a-zA-Z0-9]+)-"
        r"([a-zA-Z0-9]+)$"
    )
    user_match = user_pattern.match(socket.gethostname())

    if user_match is not None:
        return (
            user_match.group(1) is not None
            and user_match.group(2) is not None
            and user_match.group(3) is not None
            and user_match.group(4) is not None
        )

    pattern = re.compile(
        r"^(vm)-"
        r"([0-9a-fA-F]{8}-"
        r"[0-9a-fA-F]{4}-"
        r"[0-9a-fA-F]{4}-"
        r"[0-9a-fA-F]{4}-"
        r"[0-9a-fA-F]{12})-"
        r"([a-zA-Z0-9]+)-"
        r"([a-zA-Z0-9]+)-"
        r"([a-zA-Z0-9]+)$"
    )
    match = pattern.match(socket.gethostname())

    return (
        match is not None
        and match.group(1) is not None
        and match.group(2) is not None
        and match.group(3) is not None
    )
