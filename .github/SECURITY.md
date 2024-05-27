# SelfScape Insight Security Policy

Given the sensitive nature of the Facebook data handled by **SelfScape Insight**, maintaining stringent security standards in our codebase is paramount. This document delineates our security policies, which encompass repository standards, third-party dependencies, and internal coding practices.

## Definitions
The keywords "MUST", "MUST NOT", "REQUIRED", "SHALL", "SHALL NOT", "SHOULD", "SHOULD NOT", "RECOMMENDED", "MAY", and "OPTIONAL" in this document are defined as per [RFC 2119](https://www.ietf.org/rfc/rfc2119.txt). These terms represent the compliance levels required by our security protocols.

## Repository & General Standards
- **Airgap Compliance**: Core functionality MUST NOT be compromised when run in an environment without internet access (airgap). Some features MAY be unavailable under these conditions.
- **Dependency Management**: The dependency list in [pyconfig.toml](../pyconfig.toml) MUST be regularly updated to ensure security.

## Logging
Effective logging is crucial for security and auditing:
- Use `logger.use_inet()` for all internet requests or API calls.
- Use `logger.use_file()` when accessing any files.
- After writing any file, including temporary files, use `logger.wrote_file()`.

## Third-party Dependencies
- All imported packages MUST be free of known vulnerabilities, verified by regular checks using [pip-audit](https://pypi.org/project/pip-audit/).
- Contributors are encouraged to report any dependency issues through our specified channels.

## Codebase Integrity
- **Simplicity**: Favor simple, understandable solutions over complex ones. See [contribution guidelines](CONTRIBUTING.md) for coding standards.
- **Avoid Trivial Imports**: Directly implement simple functionalities in the [core](../selfscape-insight/core) directory instead of using external libraries for basic tasks.

## Reporting Security Vulnerabilities

For secure and efficient handling of security vulnerabilities, we utilize GitHub's built-in security features.

- **How to Report**: Please use the [Security Advisories page](https://github.com/your-repository/selfscape-insight/security/advisories) to report a security vulnerability. Follow the provided guidelines to create a security advisory.
- **Procedure**: Provide a clear description of the issue, including steps to reproduce it or a proof of concept.
- **Response**: We strive to assess and respond to valid reports within 48 hours.

This process ensures that security issues are managed responsibly and transparently.

By adhering to these guidelines, we safeguard the integrity and privacy of user data processed by SelfScape Insight.
