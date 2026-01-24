Observability and The Golden Signals Aether automatically exports Prometheus metrics on :9090/metrics.

Key Metrics to Watch:

1. aether_proxy_request_duration_seconds: The total time a request spends within the proxy.
2. aether_proxy_upstream_cx_total: Total connections to upstream services.
3. aether_proxy_buffer_overflows: If this is non-zero, your sidecar is memory-constrained and will start dropping packets.

Missing Documentation: We currently do not have a documented way to filter metrics by "User-Agent" without manually editing the Envoy filter templates.