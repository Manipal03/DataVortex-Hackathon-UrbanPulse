import os
from ultralytics import YOLO
from typing import Optional

_model: Optional[YOLO] = None


def get_model() -> YOLO:
	global _model
	if _model is None:
		weights = os.getenv("MODEL_WEIGHTS", "yolov8n.pt")
		_model = YOLO(weights)
	return _model
