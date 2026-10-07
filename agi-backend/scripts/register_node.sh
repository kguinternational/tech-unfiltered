#!/bin/bash
set -e

echo "Generating Headscale Auth Key..."
AUTH_KEY=$(docker exec agi_headscale headscale preauthkeys create -e 24h)

echo "Auth Key Generated: $AUTH_KEY"
echo ""
echo "To register a new edge node (like the LiteRT machine) to this AGI network, run:"
echo "sudo tailscale up --login-server=http://<THIS_MACHINE_IP>:8080 --authkey=$AUTH_KEY"
