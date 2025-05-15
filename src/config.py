from pathlib import Path
from dataclasses import dataclass


@dataclass
class Settings:
    BASE_DIR: Path = Path(__file__).resolve().parents[1]
    OUTPUT_DIR: Path = BASE_DIR / "artifacts" / "result"
    DATA_DIR: Path = BASE_DIR / "data"
