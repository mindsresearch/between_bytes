# SelfScape Insight Security Policy

Due to the nature of the data that this project handles, codebase security is critical. This document outlines the policies of this project repo to maintain a secure environment. The policy is comprised of three parts: general policies for the repo, third-party dependency policies, and policies for the code within this project.

## Definitions
The key words "MUST", "MUST NOT", "REQUIRED", "SHALL", "SHALL NOT", "SHOULD", "SHOULD NOT", "RECOMMENDED",  "MAY", and "OPTIONAL" in this document are to be interpreted as described in [RFC 2119](https://www.ietf.org/rfc/rfc2119.txt).

## Repository & General Standards
- Core functionality MUST NOT be impeded if run in an airgap environment, even though some feature modules MAY not function correctly.
- The dependency list in [pyconfig.toml](../pyconfig.toml) MUST remain up-to-date. 

## Third-party Dependencies
- Imported packages MUST NOT have any known vulnerabilities as indicated by [pip-audit](https://pypi.org/project/pip-audit/)

> [!IMPORTANT]
> Coming soon: A pip-audit GitHub Action wil be set up to verify dependency integrity in CI/CD

## Codebase Integrity
This section refers to the code written explicitly within the scope of this project.

- **Favor simplicity over complexity.** Refer to the [contribution guidelines](CONTRIBUTING.md) for more information on coding standards.
- **Avoid trivial imports.** Libraries that are being used solely to preform simple operations should be avoided in favor of directly implementing that functionality in the [core](../selfscape-insight/core) directory and importing from there instead.