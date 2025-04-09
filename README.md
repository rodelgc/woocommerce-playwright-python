# WooCommerce E2E & API Test Automation with Python Playwright

## Local machine dependencies

Make sure your local machine has the following dependencies installed:

- Python 3.9+
- [PDM](https://pdm-project.org)
- Docker

## Set up local development environment

1. Install project dependencies:
   ```bash
   pdm sync
   ```
1. Activate Python virtualenv:
   ```bash
   eval $(pdm venv activate)
   ```
1. Launch the local testing environment:
   ```bash
   pdm start
   ```
1. Open `http://localhost:8080` to verify if the local WordPress site was successfully launched.

## Other useful commands

| Command       | Description                                         |
| ------------- | --------------------------------------------------- |
| `pdm stop`    | Stop the test environment including docker volumes. |
| `pdm restart` | Do a clean restart the test environment.            |
