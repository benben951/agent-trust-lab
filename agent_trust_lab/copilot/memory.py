from __future__ import annotations

from dataclasses import asdict
from pathlib import Path
import json

from .models import CopilotSession


def write_session_memory(session: CopilotSession, out_dir: str | Path) -> Path:
    path = Path(out_dir)
    path.mkdir(parents=True, exist_ok=True)
    target = path / f"{session.review_input.case_id}.json"
    target.write_text(json.dumps(asdict(session), indent=2), encoding="utf-8")
    return target
