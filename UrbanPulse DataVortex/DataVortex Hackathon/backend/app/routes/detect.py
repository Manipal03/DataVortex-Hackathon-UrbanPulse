from fastapi import APIRouter, UploadFile, File, HTTPException
from opentelemetry import trace
from PIL import Image
import io
import time
from typing import List, Dict, Any

from ..utils.model import get_model
from ..database.supabase_client import get_supabase

router = APIRouter()


@router.post("/frame")
async def detect_frame(file: UploadFile = File(...)):
	tracer = trace.get_tracer("detect")
	with tracer.start_as_current_span("preprocess") as span:
		content = await file.read()
		try:
			image = Image.open(io.BytesIO(content)).convert("RGB")
		except Exception as e:
			raise HTTPException(status_code=400, detail=f"Invalid image: {e}")
		span.set_attribute("image.size", str(image.size))

	with tracer.start_as_current_span("inference") as span:
		model = get_model()
		start = time.perf_counter()
		results = model.predict(image, imgsz=640, conf=0.25, verbose=False)
		inference_ms = (time.perf_counter() - start) * 1000
		span.set_attribute("inference_time_ms", int(inference_ms))

	with tracer.start_as_current_span("postprocess") as span:
		classes_map = {0: "person", 1: "bicycle", 2: "car", 3: "motorcycle", 4: "airplane", 5: "bus", 6: "train", 7: "truck", 8: "boat", 9: "traffic_light", 10: "fire_hydrant", 11: "stop_sign", 12: "parking_meter", 13: "bench", 14: "bird", 15: "cat", 16: "dog", 17: "horse", 18: "sheep", 19: "cow", 20: "elephant", 21: "bear", 22: "zebra", 23: "giraffe", 24: "backpack", 25: "umbrella", 26: "handbag", 27: "tie", 28: "suitcase", 29: "frisbee", 30: "skis", 31: "snowboard", 32: "sports_ball", 33: "kite", 34: "baseball_bat", 35: "baseball_glove", 36: "skateboard", 37: "surfboard", 38: "tennis_racket", 39: "bottle", 40: "wine_glass", 41: "cup", 42: "fork", 43: "knife", 44: "spoon", 45: "bowl", 46: "banana", 47: "apple", 48: "sandwich", 49: "orange", 50: "broccoli", 51: "carrot", 52: "hot_dog", 53: "pizza", 54: "donut", 55: "cake", 56: "chair", 57: "couch", 58: "potted_plant", 59: "bed", 60: "dining_table", 61: "toilet", 62: "tv", 63: "laptop", 64: "mouse", 65: "remote", 66: "keyboard", 67: "cell_phone", 68: "microwave", 69: "oven", 70: "toaster", 71: "sink", 72: "refrigerator", 73: "book", 74: "clock", 75: "vase", 76: "scissors", 77: "teddy_bear", 78: "hair_drier", 79: "toothbrush"}
		# map emergency classes: ambulance, fire_truck, police are commonly represented as 'truck', 'car', or 'bus' in COCO; for MVP filter to those proxies
		emergency_aliases = {"ambulance": ["truck", "car"], "fire_truck": ["truck", "bus"], "police": ["car"]}
		detections: List[Dict[str, Any]] = []
		for r in results:
			for b in r.boxes:
				cls_id = int(b.cls.item())
				label = classes_map.get(cls_id, str(cls_id))
				conf = float(b.conf.item())
				xyxy = [float(x) for x in b.xyxy[0].tolist()]
				vehicle_type = None
				if label in emergency_aliases["ambulance"]:
					vehicle_type = "ambulance"
				elif label in emergency_aliases["fire_truck"]:
					vehicle_type = "fire_truck"
				elif label in emergency_aliases["police"]:
					vehicle_type = "police"
				if vehicle_type:
					detections.append({
						"vehicle_type": vehicle_type,
						"confidence": conf,
						"bbox": xyxy,
					})
		span.set_attribute("num_detections", len(detections))

	with tracer.start_as_current_span("db.insert_detection") as span:
		if detections:
			sb = get_supabase()
			payload = [
				{
					"vehicle_type": d["vehicle_type"],
					"confidence": d["confidence"],
					"bbox": d["bbox"],
				}
				for d in detections
			]
			_ = sb.table("detections").insert(payload).execute()

	with tracer.start_as_current_span("schedule_signals") as span:
		# MVP: no-op scheduling; integration with /signal/update can be added
		span.set_attribute("scheduled_signals", 0)

	return {"detections": detections}
