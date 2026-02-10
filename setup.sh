#!/bin/bash
# Setup script for Todoist Count Badge

set -e

echo "Setting up Todoist Count Badge..."

# Check Python version
PYTHON_VERSION=$(python3 --version | cut -d' ' -f2)
echo "✓ Python version: $PYTHON_VERSION"

# Install dependencies
echo "Installing dependencies..."
pip install -q -r requirements.txt
echo "✓ Dependencies installed"

# Make script executable
chmod +x todoist_badge.py
echo "✓ Script made executable"

echo ""
echo "Setup complete!"
echo ""
echo "Next steps:"
echo "1. Get your Todoist API token from: https://todoist.com/app/settings/account"
echo "2. Run with: ./todoist_badge.py --token YOUR_TOKEN"
echo "3. Or set TODOIST_API_TOKEN environment variable"
echo ""
echo "To schedule updates, see README.md for cron or systemd timer setup"
echo ""
