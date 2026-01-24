Upgrading from v0.x to v1.0 The jump to v1.0 introduces breaking changes in how the AetherService YAML is structured.

1. Rename spec.proxy_settings to spec.runtime.
2. Update your SDK version to ^1.0.0.
3. Deploy a "Canary Brain" to test the migration.

Warning: During migration, there is a 50ms "blind spot" where mTLS handshakes might fail while the new certificates are being propagated. We recommend doing this during low-traffic windows.