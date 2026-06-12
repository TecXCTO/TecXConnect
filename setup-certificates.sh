#!/bin/bash

# Define deployment domain targets
DOMAIN="://tecx.ai"
EMAIL="admin@tecx.ai"

echo "=== Step 1: Requesting SSL Certificates from Let's Encrypt ==="

# Launch a temporary Certbot container to handle verification and generation
docker run -it --rm --name production_certbot \
  -v "/etc/letsencrypt:/etc/letsencrypt" \
  -v "/var/lib/letsencrypt:/var/lib/letsencrypt" \
  -p 80:80 \
  certbot/certbot certonly --standalone \
  -d $DOMAIN --email $EMAIL --agree-tos --no-eff-email

echo "=== Step 2: Certificates received successfully ==="

# Reload Nginx inside your running Docker Compose stack to read the new files
if [ -d "/etc/letsencrypt/live/$DOMAIN" ]; then
    echo "Reloading Nginx proxy system infrastructure..."
    docker compose exec web-proxy nginx -s reload
else
    echo "CRITICAL: Certificate generation sequence failed."
fi

