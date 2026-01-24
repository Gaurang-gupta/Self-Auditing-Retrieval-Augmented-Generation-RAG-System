Local Development Setup To simulate the mesh on your local machine, follow these steps:

1. Ensure you have the aether-cli installed via Homebrew.
2. Run the bootstrap script: ./scripts/bootstrap.sh --env=dev.
3. Mount your local configuration: export AETHER_CONFIG_PATH=$HOME/.aether/config.yaml.
4. Launch the local plane: make fly.

Known Issue: Users on macOS M1/M2/M3/M4 chips will see a SIGSEGV during the make fly process. This is due to an architectural mismatch in the aether-init binary. Currently, the workaround is to run the entire stack inside a Linux VM or use the remote dev-cluster.