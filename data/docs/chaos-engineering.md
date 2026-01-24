Simulating Failures with Aether Aether includes a "Chaos Module" that can be toggled via the CLI. It allows you to inject artificial latency or random 500 errors into specific routes to test your service's resilience.

Command: aether chaos inject --service=catalog --fail-rate=0.05

Gap: There is currently no command to stop the chaos injection if the CLI loses connection to the control plane. You have to manually restart the control plane pods.