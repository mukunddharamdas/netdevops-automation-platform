
# Changelog

This file tracks significant changes to the NetDevOps Automation Platform.

## [Unreleased]

### Added

- Reusable device inventory validation module.
- 27 automated inventory validation tests.
- Pinned Ansible collection dependencies.
- Automatic creation of local pre-check report directories.
- Device-specific Ansible baseline report filenames.
- Optional configuration display using the --show-config argument.
- Project architecture diagram and comprehensive README documentation.
- Local secret scanning procedures using Gitleaks.

### Changed

- Expanded the local Python regression suite from 29 to 56 tests.
- Improved network connection exception handling.
- Improved validation result aggregation across multiple devices.
- Improved process exit codes for failed validation.
- Improved connection cleanup and failure handling.
- Updated the example Ansible inventory with network connection settings.
- Improved configuration generation output.

### Security

- Enabled SSH host key verification in Netmiko and ncclient.
- Enabled TLS certificate verification for RESTCONF requests.
- Reduced exposure of raw network output and exception details.
- Added Ansible task output suppression for sensitive operations.
- Configured restricted report directory and file permissions.
- Validated inventory structure before requesting device credentials.
- Performed local Git history and source secret scans.

### Validation

- 56 Python tests passed locally.
- 27 inventory validation tests passed.
- Ansible playbook syntax checks passed.
- Example Ansible inventory parsing passed.
- Initial Gitleaks scans reported no secret findings.

### Known Limitations

- Live verification of revised connection security remains pending.
- Revised Ansible pre-check runtime behavior requires live validation.
- Fresh dependency installation has not been independently tested.
- Expanded Python test suite awaits GitHub Actions verification.
- Automated configuration deployment and rollback are not yet implemented.

## Initial Platform Milestones

### Added

- Python network automation using Netmiko, ncclient, and Requests.
- Network interface state and configuration validation.
- YAML-driven configuration generation using Jinja2.
- Initial suite of 29 automated Python tests.
- Read-only Ansible network pre-change validation.
- Bash-based fail-closed deployment safety gate.
- GitHub Actions continuous integration workflow.
- Protected main branch with mandatory automated test checks.

### Validation

- Initial GitHub Actions workflow passed all 29 tests.
- Intentionally failing pull request was blocked from merging.
- Ansible pre-check positive and negative scenarios were verified.
- Deployment safety gate exit codes were verified.
