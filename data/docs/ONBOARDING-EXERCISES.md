Welcome to the Team, Engineer. To get you up to speed with Project Aether, you are required to complete the following three "Live Fire" exercises in the staging environment. If you get stuck, refer to the existing .md files in this repo. Please do not ask in the #eng-general Slack channel until you have at least tried to find the answer here.

Task 1: The Ghost in the Machine Deploy a sample "Hello World" service using the AetherService manifest format.
Goal: Successfully route traffic from the Ingress to your pod.
The Catch: You will likely see a 403 Forbidden immediately upon deployment.
Hint: Check security-policy.md regarding mTLS and identity. You'll need to verify if your service account is actually authorized to receive traffic or if it’s being "quarantined."

Task 2: Tuning the Storm Your service is experiencing a simulated "Retry Storm."
Goal: Use the Aether SDK (refer to routing-logic.md) to implement a circuit breaker that trips after 3 consecutive failures.
The Catch: There is a discrepancy between the YAML manifest timeout and the SDK timeout behavior.
Challenge: Determine if the 300ms timeout in deployment-manifests.md is cumulative or per-attempt. Documentation is silent on this—you'll need to check the Prometheus metrics (see telemetry-and-metrics.md) to see the actual timing of the drops.

Task 3: The M4 Workaround Since you were likely issued a new company laptop with an M4 chip, you cannot use make fly directly.
Goal: Get a local proxy running that can talk to the staging Brain.
The Catch: The getting-started.md file tells you to use a Docker container but doesn't provide the image path.
Clue: Scan the env-variables.md file. There is a specific variable mentioned there that, if set incorrectly, will cause the proxy to "heartbeat" to the wrong IP. You'll need to find the AE_PORT and override it to bypass the local architectural conflict.

Completion Criteria Once finished, export your X-Aether-Trace-ID from a successful request and send it to your onboarding buddy. If your trace shows more than 2 retries, you have failed Task 2.