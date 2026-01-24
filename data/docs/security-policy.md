Identity and Encryption Aether enforces "Zero Trust" by default.

Certificate Rotation: The Control Plane issues short-lived SVIDs (SPIFFE Verifiable Identity Documents). These rotate every 24 hours. If a pod fails to rotate its cert, it will be "quarantined" and all ingress traffic will be rejected with a 403 Forbidden.
Manual Override: Do NOT attempt to manually delete certificates from the /etc/aether/certs volume. This will trigger a security alert in the SOC and page the on-call engineer.