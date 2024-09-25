from dataclasses import dataclass
from pathlib import Path


@dataclass
class ReceivedFile:
    file_name: str
    mime_type: str
    path: Path
