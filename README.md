# WooCommerce E2E & API Test Automation with Python Playwright

## Local machine dependencies

Make sure your local machine has the following dependencies installed:

- Python 3.9+
- [PDM](https://pdm-project.org)
- Docker

## Set up local development environment

1. Install project dependencies:
   ```bash
   pdm install
   ```
1. Activate Python virtualenv:
   ```bash
   eval $(pdm venv activate)
   ```
1. Launch the local testing environment:
   ```bash
   pdm run start
   ```
1. Open `http://localhost:8080` to verify if the local WordPress site was successfully launched. To log in to WP Admin, use `user` and `bitnami` as username and password, respectively.

## Other useful commands

| Command           | Description                                         |
| ----------------- | --------------------------------------------------- |
| `pdm run stop`    | Stop the test environment including docker volumes. |
| `pdm run restart` | Do a clean restart of the test environment.         |
