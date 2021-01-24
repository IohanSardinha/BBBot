from utils import get_answers
from pathlib import Path

for fold in get_answers():
        Path("train/"+fold+"/").mkdir(parents=True, exist_ok=True)
