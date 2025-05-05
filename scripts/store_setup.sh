#!/bin/bash

source ./local.env

wait_site_up() {
    MAX_RETRIES=10
    RETRY_DELAY=5
    attempt=1

    echo "Waiting for the site to be up..."

    while [ $attempt -le $MAX_RETRIES ]; do
        echo "Attempt $attempt of $MAX_RETRIES..."

        if curl -fs -o /dev/null http://localhost:8080; then
            echo "Site is up!"
            return
        else
            echo "Site is still down. Retrying in $RETRY_DELAY seconds..."
            sleep $RETRY_DELAY
        fi

        # Increment retry counter
        attempt=$((attempt + 1))
    done

    echo "Site still down after $MAX_RETRIES attempts."
    exit 1
}

skip_onboarding() {
    echo "Skipping onboarding..."
    docker compose exec wordpress bash -c "wp option update woocommerce_onboarding_profile '{\"skipped\": true}' --format=json"
}

create_customer() {
    echo "Creating customer fixture..."
    docker compose exec wordpress bash -c "wp user create $WORDPRESS_CUSTOMER_USERNAME $WORDPRESS_CUSTOMER_EMAIL --role=customer --user_pass=$WORDPRESS_CUSTOMER_PASSWORD"
}

launch_store() {
    echo "Launching store..."
    docker compose exec wordpress bash -c "wp option update woocommerce_coming_soon no"
}

wait_site_up
skip_onboarding
create_customer
launch_store
