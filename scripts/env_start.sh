#!/bin/bash

# Start local dev env
docker compose up -d

# Set up store
bash "./scripts/store_setup.sh"

# Install Playwright Chromium browser
playwright install chromium
