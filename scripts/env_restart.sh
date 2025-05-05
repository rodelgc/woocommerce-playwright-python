#!/bin/bash

bash ./scripts/env_stop.sh

echo "Pausing 5 seconds..."
sleep 5

bash ./scripts/env_start.sh
