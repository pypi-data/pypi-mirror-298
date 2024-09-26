from setuptools import setup, find_packages

setup(
    name="tia_otel_observability_tracer",
    version="0.1.0",
    description="A Python library for managing OpenTelemetry tracing",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Tia Cloud",
    author_email="francis.poku@tiacloud.io",
    url="https://github.com/tiacloudconsult/observability.git",
    packages=find_packages(),
    install_requires=[
        "opentelemetry-distro>=0.48b0",
        "opentelemetry-exporter-otlp>=1.27.0",
        "opentelemetry-api>=1.27.0",
        "opentelemetry-sdk>=1.27.0",
        "opentelemetry-exporter-otlp-proto-http>=1.27.0",
        "opentelemetry-exporter-otlp-proto-grpc>=1.27.0",
        "opentelemetry-exporter-jaeger>=1.21.0",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.12",
)
