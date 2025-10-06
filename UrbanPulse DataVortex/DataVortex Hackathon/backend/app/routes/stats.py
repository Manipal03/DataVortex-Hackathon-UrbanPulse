from fastapi import APIRouter

router = APIRouter()

@router.get("/summary")
async def summary():
	return {
		"detections": 0,
		"avg_response_time_ms": 0,
		"corridor_activations": 0,
	}
