import os
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

from .tracing import init_tracing, instrument_fastapi

# Initialize tracing first
init_tracing()

app = FastAPI(title="UrbanPulse AI – Smart Emergency Traffic Management")
instrument_fastapi(app)

app.add_middleware(
	CORSMiddleware,
	allow_origins=["*"],
	allow_credentials=True,
	allow_methods=["*"],
	allow_headers=["*"]
)


@app.middleware("http")
async def add_trace_id_header(request: Request, call_next):
	from opentelemetry import trace
	span = trace.get_current_span()
	response = await call_next(request)
	context = span.get_span_context()
	if context and context.trace_id != 0:
		trace_id_hex = format(context.trace_id, "032x")
		response.headers["x-trace-id"] = trace_id_hex
	return response


@app.get("/health")
async def health():
	return {"status": "ok"}


# Include modular routers (placeholders; implemented in app/routes)
from .routes import detect, simulate, signals, stats  # noqa: E402

app.include_router(detect.router, prefix="/detect", tags=["detect"]) 
app.include_router(simulate.router, prefix="/simulate", tags=["simulate"]) 
app.include_router(signals.router, prefix="/signal", tags=["signal"]) 
app.include_router(stats.router, prefix="/stats", tags=["stats"])
