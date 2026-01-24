Incident Report: The Great Latency Spike Date: 2025-11-12 Duration: 42 Minutes

The Root Cause: An engineer attempted to fix a "flaky" microservice by increasing the resiliency.retries value to 1,000,000. This created a "retry storm" that overwhelmed the aether-brain, causing a cascading failure across the entire us-east-1 cluster.
The Fix: A hard limit was added to the Aether source code. Any retry value over 10 is now automatically truncated to 10 with a warning log.