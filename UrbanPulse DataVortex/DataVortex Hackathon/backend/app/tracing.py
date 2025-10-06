from typing import Optional
import os

from opentelemetry import trace
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor


def init_tracing(service_name: str = "urbanpulse-backend") -> None:
	otlp_endpoint = os.getenv("OTLP_ENDPOINT", "http://localhost:4318/v1/traces")
	resource = Resource.create({
		"service.name": service_name,
	})
	provider = TracerProvider(resource=resource)
	exporter = OTLPSpanExporter(endpoint=otlp_endpoint)
	processor = BatchSpanProcessor(exporter)
	provider.add_span_processor(processor)
	trace.set_tracer_provider(provider)


def instrument_fastapi(app) -> None:
	FastAPIInstrumentor.instrument_app(app)
