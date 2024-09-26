# src/ticos_agent/base.py

import json
from abc import ABC, abstractmethod
from opentelemetry import trace
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import (
    BatchSpanProcessor,
    ConsoleSpanExporter,
    SpanExporter,
)
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter


class JSONFileExporter(SpanExporter):
    def __init__(self, file_path):
        self.file_path = file_path

    def export(self, spans):
        with open(self.file_path, "a") as f:
            for span in spans:
                json.dump(span.to_json(), f)
                f.write("\n")
        return SpanExporter.SUCCESS

    def shutdown(self):
        pass


class BaseDevice(ABC):
    def __init__(self, config):
        self.tracer_provider = TracerProvider(
            resource=Resource.create({"service.name": self.__class__.__name__})
        )
        self.tracer = self.tracer_provider.get_tracer(__name__)
        self.config = config
        self.setup_telemetry()

    @abstractmethod
    def get_device_info(self):
        pass

    @abstractmethod
    def collect_data(self):
        pass

    @abstractmethod
    def execute_command(self, command_name, **kwargs):
        pass

    def setup_telemetry(self):
        telemetry_config = self.config.get("telemetry", {})
        self.telemetry_exporter = telemetry_config.get("exporter", "console")
        self.telemetry_file = telemetry_config.get("file", "telemetry.json")

        if self.telemetry_exporter == "console":
            exporter = ConsoleSpanExporter()
        elif self.telemetry_exporter == "file":
            exporter = JSONFileExporter(self.telemetry_file)
        elif self.telemetry_exporter == "otlp":
            otlp_endpoint = telemetry_config.get(
                "otlp_endpoint", "http://localhost:4318/v1/traces"
            )
            exporter = OTLPSpanExporter(endpoint=otlp_endpoint)
        else:
            raise ValueError(f"Unknown exporter type: {self.telemetry_exporter}")

        span_processor = BatchSpanProcessor(exporter)
        self.tracer_provider.add_span_processor(span_processor)
        trace.set_tracer_provider(self.tracer_provider)

    def send_telemetry(self, data):
        with self.tracer.start_as_current_span("device_telemetry") as span:
            for key, value in data.items():
                span.set_attribute(key, str(value))
