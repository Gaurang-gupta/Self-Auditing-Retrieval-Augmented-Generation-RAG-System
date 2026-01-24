Project Aether Internal Terminology To maintain consistency across squads, please use the following definitions.

The Brain (Control Plane): The central nervous system of Aether. It is responsible for the distribution of routing tables and mTLS certificates. If the Brain is unreachable, the mesh enters "Stateless Mode," where existing routes persist but no new services can join.
The Ghost (Data Plane): The sidecar proxy process. It is called a "Ghost" because it should be invisible to the application logic, but its presence is felt in every millisecond of latency.
SVID (SPIFFE Verifiable Identity Document): The X.509 certificate used for peer-to-peer authentication. In Aether, these are automatically rotated; manual rotation is a "Break Glass" procedure.
Quarantine: A network state where a pod's proxy rejects all traffic with a 403. Usually happens due to expired SVIDs or a failure to pass the pulse check.
Warp vs. Tunnel: Warp was our legacy UDP-based routing. Tunnel is the new TCP-over-mTLS standard. If you see warp in a legacy config, it is a high-priority tech-debt item.