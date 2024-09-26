import os
import inspect
from contextlib import contextmanager
from opentelemetry import trace
from opentelemetry.sdk.resources import SERVICE_NAME, Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.trace.export import BatchSpanProcessor

class TracingManager:
    def __init__(self, service_name: str):
        resource = Resource(attributes={SERVICE_NAME: service_name})
        otlp_endpoint = "http://localhost:4317"

        trace_provider = TracerProvider(resource=resource)
        otlp_exporter = OTLPSpanExporter(endpoint=otlp_endpoint)
        span_processor = BatchSpanProcessor(otlp_exporter)

        trace.set_tracer_provider(trace_provider)
        trace_provider.add_span_processor(span_processor)
        self.tracer = trace.get_tracer(__name__)

    @contextmanager
    def start_trace(self):
        """
        Context manager to create both parent and child spans.
        Automatically sets the parent span to the file name of the caller
        and the child span to the function name.
        """
        # Get the filename of the calling script, which is two frames back
        caller_frame = inspect.stack()[2]
        parent_span_name = os.path.basename(caller_frame.filename).replace('.py', '')

        # Start the parent span
        with self.tracer.start_as_current_span(parent_span_name) as parent_span:
            # Get the name of the calling function (child span)
            function_name = inspect.currentframe().f_back.f_back.f_code.co_name

            # Start the child span
            with self.tracer.start_as_current_span(function_name) as child_span:
                yield parent_span, child_span  # Pass both spans to the context
