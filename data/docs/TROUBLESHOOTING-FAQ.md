"Help, nothing is working" — Start Here.

Q: My pod is running but I’m getting 503 errors on every request. 
: Check the aether-init logs. Usually, this means the iptables rules didn't apply correctly. If you see Permission Denied, your Kubernetes Namespace lacks the aether-privileged label.

Q: Why is my service-to-service latency over 200ms? 
: Check telemetry-and-metrics.md. Specifically, look at aether_proxy_buffer_overflows. If your pod is under heavy load, the Ghost proxy might be queuing packets. Increase the AE_CONCURRENCY_LIMIT in your env variables.

Q: I updated my AetherService YAML, but the changes aren't reflecting. 
: The Brain has a "Sync Latency" of about 30 seconds. If it takes longer, the Brain might be in a "Partial Partition" state. Check the TICKETS-KNOWN-ISSUES.txt regarding the K8s API sync bug (#405).

Q: The CLI says Unauthorized but I just logged in.
: The SSO tokens expire every 8 hours. Run aether auth login --force to clear your local cache and start a fresh session.