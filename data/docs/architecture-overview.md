System Design and Topology Aether operates on a split-plane architecture:

The Control Plane (The Brain): A centralized cluster of Go services that manage state, distribute certificates, and monitor health. It stores the source of truth in a dedicated etcd cluster.

The Data Plane (The Ghost): A high-performance proxy written in Rust that lives alongside your container. It intercepts all INBOUND and OUTBOUND traffic.

The "Ghost" Lifecycle: When a pod starts, the aether-init container modifies iptables rules to force traffic through the Ghost proxy. If the Ghost proxy fails, the pod is effectively isolated from the network.