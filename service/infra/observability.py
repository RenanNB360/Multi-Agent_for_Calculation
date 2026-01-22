from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import SimpleSpanProcessor, ConsoleSpanExporter
from opentelemetry.sdk.resources import Resource


def setup_tracing(service_name: str) -> None:
    provider = TracerProvider(
        resource=Resource.create(
            {"service.name": service_name}
        )
    )

    provider.add_span_processor(
        SimpleSpanProcessor(ConsoleSpanExporter())
    )

    trace.set_tracer_provider(provider)
