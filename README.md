# WooCommerce E2E & API Test Automation with Python Playwright

This is a portfolio project featuring an end-to-end and API test suite built with the Python implementation of Playwright.
The local development environment uses a WooCommerce online store powered by the `bitnami/wordpress` Docker image.
To see this test suite running in CI via GitHub Actions, check out the [Daily Test Runs](https://github.com/rodelgc/woocommerce-playwright-python/actions/workflows/daily-test-run.yml), which execute every day at 22:00 UTC.


## Instructions to run the test suite

The following will guide you through setting up your WooCommerce local development environment and running the tests.

## Local machine dependencies

First of all, make sure your local machine has the following dependencies installed:

- Python 3.13+
- [PDM](https://pdm-project.org)
- Docker and Docker compose v2

## Set up local development environment

After setting up the local machine dependencies, follow the steps below to launch the test environment and run the tests against it.

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
1. Open `http://localhost:8080` to verify if the local WordPress site was successfully launched.
2. Run the tests:
   ```bash
   pdm run test # run tests in headless mode
   pdm run test-headed # run tests in UI mode
   ```

## Other useful commands

| Command           | Description                                         |
| ----------------- | --------------------------------------------------- |
| `pdm run stop`    | Stop the test environment including docker volumes. |
| `pdm run restart` | Do a clean restart of the test environment.         |
