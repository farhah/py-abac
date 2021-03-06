# v0.1.0 Pre-release

- Basic policy definition. Nested attribute not supported.
- Poor policy lookup performance in storage for large number of policies.

# v0.2.0

- Complete re-factor with better design. Derived from XACML and Vakt
- Powerful support for policy conditions on nested attributes.
- MongoDB policy storage with efficient lookup based on target IDs.
- Supports creation of custom policy storage.
- Supports creation of custom PIP.
- JSON based policy language.

# v0.3.0

- Added Sphinx documentation.
- Code quality checks performed.
- Security checks added.
- Added SQL storage.
- Refactored `Request` class name to `AccessRequest`. The name `Request` still supported for backward compatibility. 
