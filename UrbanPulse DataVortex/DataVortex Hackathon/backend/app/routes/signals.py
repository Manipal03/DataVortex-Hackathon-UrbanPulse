from fastapi import APIRouter
from enum import Enum
from typing import Dict

router = APIRouter()

# in-memory signal state for scaffold
SIGNALS: Dict[str, str] = {
	"A1": "red",
	"A2": "red",
	"B1": "red",
}

class SignalStatus(str, Enum):
	red = "red"
	yellow = "yellow"
	green = "green"

@router.get("/all")
async def all_signals():
	return {"signals": SIGNALS}

@router.post("/update")
async def update_signal(signal_id: str, status: SignalStatus):
	SIGNALS[signal_id] = status.value
	return {"ok": True, "signals": SIGNALS}
