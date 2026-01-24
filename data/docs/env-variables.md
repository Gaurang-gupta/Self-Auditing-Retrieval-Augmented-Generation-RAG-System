Configuration Parameters Aether configuration is driven by environment variables injected at runtime.

1. AE_LOG_LEVEL: Set to debug for verbose output. Warning: This will generate gigabytes of logs in seconds.
2. AE_PORT: The internal listener for the proxy. Default is 8080.
3. AE_SECRET: Used for signing internal telemetry packets. This is supposed to be managed by Vault, but some legacy services still have it hardcoded as REPLACE_ME_IN_PROD.
4. AE_CONCURRENCY_LIMIT: Caps the number of simultaneous streams. Default is 1024.