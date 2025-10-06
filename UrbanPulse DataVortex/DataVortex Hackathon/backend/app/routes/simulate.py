from fastapi import APIRouter
from pydantic import BaseModel
from opentelemetry import trace

router = APIRouter()

class GPSPoint(BaseModel):
	lat: float
	lon: float
	ts: float

@router.post("/gps_point")
async def gps_point(point: GPSPoint):
	tracer = trace.get_tracer("simulate")
	with tracer.start_as_current_span("route_predict") as span:
		# placeholder: echo back a fake route and ETA
		span.set_attribute("eta_sec", 0)
		route = {"coordinates": [[point.lon, point.lat]], "eta_sec": 0}
	return {"route": route}
