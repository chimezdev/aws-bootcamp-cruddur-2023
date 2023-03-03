# Week 2 — Distributed Tracing

## Honeycomb setup
Honeycomb is an observability tool that allow you gain insight into performance of your solution.
Honeycomb offers free-tier pricing option. To setup a Honeycomb account:
- Go to ***honeycomb.io***
- click on the **Pricing**, the **Get Started** to create a free account.
- follow the steps in this [Honeycomb](https://www.youtube.com/watch?v=2GD9xCzRId4&list=PLBfufR7vyJJ7k25byhRXJldB5AiwgNnWv&index=31) to create environment and copy your API-Key.
- Run the command, `export HONEYCOMB_API_KEY="wWxmjac8EHWONJnQE6xIxD"` to set it as environment variable
- Run, `gp env HONEYCOMB_API_KEY="wWxmjac8EHWONJnQE6xIxD"` to allow gitpod to grab it when next it loaded.
- Install these Honeycomb packages by running:
    ```
        pip install opentelemetry-api \
        opentelemetry-sdk \
        opentelemetry-exporter-otlp-proto-http \
        opentelemetry-instrumentation-flask \
        opentelemetry-instrumentation-requests
    ```
- Next, add the following to the **app.py** file
    ```
    from opentelemetry import trace
    from opentelemetry.instrumentation.flask import FlaskInstrumentor
    from opentelemetry.instrumentation.requests import RequestsInstrumentor
    from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
    from opentelemetry.sdk.trace import TracerProvider
    from opentelemetry.sdk.trace.export import BatchSpanProcessor
    ```
    ```
        # Initialize tracing and an exporter that can send data to Honeycomb
        provider = TracerProvider()
        processor = BatchSpanProcessor(OTLPSpanExporter())
        provider.add_span_processor(processor)
        trace.set_tracer_provider(provider)
        tracer = trace.get_tracer(__name__)
    ```
    ```
        # Initialize automatic instrumentation with Flask
        app = Flask(__name__)
        FlaskInstrumentor().instrument_app(app)
        RequestsInstrumentor().instrument()
    ```
- Configure OpenTelemetry, OTEL to send events to Honeycomb by setting some env variables to the docker-compose file. 
```
    OTEL_SERVICE_NAME: "your-service-name"
    OTEL_EXPORTER_OTLP_ENDPOINT: "https://api.honeycomb.io"
    OTEL_EXPORTER_OTLP_HEADERS: "x-honeycomb-team=${HONEYCOMB_API_KEY}"
    python app.py
```