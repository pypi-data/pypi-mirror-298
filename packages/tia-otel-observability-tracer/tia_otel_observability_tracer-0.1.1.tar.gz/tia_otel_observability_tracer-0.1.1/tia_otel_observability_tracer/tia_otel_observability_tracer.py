import os
import inspect
from contextlib import contextmanager
from opentelemetry import trace, baggage
from opentelemetry.sdk.resources import SERVICE_NAME, Resource
from opentelemetry.sdk.trace import TracerProvider, Span
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.trace import Link, set_span_in_context


class TracingManager:
    def __init__(self, service_name: str, environment: str = "dev"):
        resource = Resource(attributes={SERVICE_NAME: service_name, "environment": environment})
        otlp_endpoint = "http://localhost:4317"

        trace_provider = TracerProvider(resource=resource)
        otlp_exporter = OTLPSpanExporter(endpoint=otlp_endpoint)
        span_processor = BatchSpanProcessor(otlp_exporter)

        trace.set_tracer_provider(trace_provider)
        trace_provider.add_span_processor(span_processor)
        self.tracer = trace.get_tracer(__name__)
        self.active_spans = []  # Keep track of active spans for automatic linking

    @contextmanager
    def start_trace(self, additional_attributes=None):
        """
        Context manager to create both parent and child spans.
        Automatically links previous spans to the parent span.
        """
        # Get the filename of the calling script
        caller_frame = inspect.stack()[2]
        parent_span_name = os.path.basename(caller_frame.filename).replace('.py', '')

        # Automatically link previous active spans
        span_links = [Link(span.get_span_context()) for span in self.active_spans]

        # Start the parent span with automatically added links
        with self.tracer.start_as_current_span(parent_span_name, links=span_links) as parent_span:
            # Get the name of the calling function (child span)
            function_name = inspect.currentframe().f_back.f_back.f_code.co_name

            # Start the child span
            with self.tracer.start_as_current_span(function_name) as child_span:
                # Set additional attributes if provided
                if additional_attributes:
                    child_span.set_attributes(additional_attributes)

                # Add current spans to the active spans list for future linking
                self.active_spans.append(parent_span)
                yield parent_span, child_span  # Pass both spans to the context

            # Remove the span after it's completed
            self.active_spans.remove(parent_span)
