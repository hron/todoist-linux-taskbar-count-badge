# Todoist Count Badge

This project updates the count badge on the Todoist desktop application via D-Bus, displaying the number of tasks scheduled for today or overdue. It is designed for Linux desktop environments that support Unity LauncherEntry signals.

## Features
- Fetches tasks from the Todoist API
- Counts tasks due today or overdue
- Updates the badge on the Todoist desktop launcher using D-Bus
- Configurable update interval
- Supports environment variables for API token and desktop ID
- Systemd service integration for background operation

## Requirements
- Python 3
- `requests` library
- `dbus` library

Install dependencies:

```bash
pip install -r requirements.txt
```

## Usage

### Run Manually

```bash
export TODOIST_API_TOKEN="<your_token>"
export TODOIST_DESKTOP_ID="application://todoist.desktop"  # Optional
python3 todoist_badge.py --interval 300
```

#### Options
- `--token` Todoist API token (or use `TODOIST_API_TOKEN` env var)
- `--interval` Update interval in seconds (default: 300)
- `--verbose` Enable debug logging

### Systemd Service

A sample user service file is provided:

- Path: `~/.config/systemd/user/todoist-badge.service`

#### Example
```
[Unit]
Description=Todoist Count Badge Updater
After=network-online.target
Wants=network-online.target

[Service]
Type=simple
ExecStart=/usr/bin/env python3 %h/src/todoist-count-badge/todoist_badge.py --interval 300
Environment="TODOIST_API_TOKEN=<your_token>"
Environment="TODOIST_DESKTOP_ID=application://todoist.desktop"
Restart=on-failure
RestartSec=10
StandardOutput=journal
StandardError=journal

[Install]
WantedBy=default.target
```

#### Enable and Start
```bash
systemctl --user daemon-reload
systemctl --user enable todoist-badge.service
systemctl --user start todoist-badge.service
```

## Logging
- Set `LOG_LEVEL` environment variable to control log verbosity (e.g., `DEBUG`, `INFO`)

## License
MIT
