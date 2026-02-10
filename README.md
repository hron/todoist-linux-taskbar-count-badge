# Todoist Count Badge

Updates the count badge on `todoist.desktop` via D-Bus by consuming the Todoist API. The badge displays the number of tasks scheduled for today or overdue.

## Features

- Fetches tasks from Todoist API with filtering for today and overdue tasks
- Updates application badge via D-Bus (supports GNOME and Unity desktops)
- Configurable via command-line arguments or environment variables
- Comprehensive logging and error handling
- Lightweight and fast

## Requirements

- Python 3.6+
- D-Bus session bus
- Todoist application with D-Bus support (todoist.desktop)

## Installation

1. Clone or download this repository:
```bash
cd /home/algus/src/todoist-count-badge
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Configuration

### Get Your Todoist API Token

1. Go to [Todoist Settings](https://todoist.com/app/settings/account)
2. Scroll to "API token"
3. Copy your token

## Usage

### Command Line

Run with explicit token:
```bash
python3 todoist_badge.py --token YOUR_API_TOKEN
```

Run with token from environment variable:
```bash
export TODOIST_API_TOKEN=YOUR_API_TOKEN
python3 todoist_badge.py
```

Enable verbose logging:
```bash
python3 todoist_badge.py --verbose
```

### Scheduling Updates

#### Option 1: Cron Job

Edit your crontab to run every 5 minutes:
```bash
crontab -e
```

Add this line:
```cron
*/5 * * * * export TODOIST_API_TOKEN=YOUR_API_TOKEN && /usr/bin/python3 /home/algus/src/todoist-count-badge/todoist_badge.py
```

#### Option 2: Systemd Timer

Create `~/.config/systemd/user/todoist-badge.service`:
```ini
[Unit]
Description=Todoist Count Badge Updater
After=network-online.target
Wants=network-online.target

[Service]
Type=oneshot
ExecStart=%h/src/todoist-count-badge/todoist_badge.py
Environment="TODOIST_API_TOKEN=YOUR_API_TOKEN"
StandardOutput=journal
StandardError=journal
```

Create `~/.config/systemd/user/todoist-badge.timer`:
```ini
[Unit]
Description=Todoist Count Badge Updater Timer
Requires=todoist-badge.service

[Timer]
OnBootSec=1min
OnUnitActiveSec=5min
Persistent=true

[Install]
WantedBy=timers.target
```

Enable and start:
```bash
systemctl --user daemon-reload
systemctl --user enable todoist-badge.timer
systemctl --user start todoist-badge.timer
```

Check status:
```bash
systemctl --user status todoist-badge.timer
journalctl --user -u todoist-badge.service -f
```

## How It Works

1. **Fetches Tasks**: Connects to the Todoist API v2 using your API token
2. **Filters Tasks**: Retrieves only tasks scheduled for today or overdue using the built-in Todoist filter
3. **Counts Tasks**: Counts the total number of matching tasks
4. **Updates Badge**: Uses D-Bus to communicate with `todoist.desktop` and update the application launcher badge

## D-Bus Implementation Details

The script attempts to update the badge using multiple methods:

1. **GNOME/FreeDesktop Method**: Uses `org.freedesktop.Application` interface
2. **Unity Fallback**: Falls back to `com.canonical.Unity.LauncherEntry` if available

This ensures compatibility across different desktop environments.

## Troubleshooting

### "No module named 'dbus'"

Install dbus-python:
```bash
pip install dbus-python
```

On Fedora/RHEL:
```bash
sudo dnf install dbus-python
```

On Debian/Ubuntu:
```bash
sudo apt-get install python3-dbus
```

### "Failed to connect to D-Bus"

- Ensure D-Bus session is running: `echo $DBUS_SESSION_BUS_ADDRESS`
- If running via cron/timer, ensure proper environment variables are set
- For systemd service, add: `Environment="DISPLAY=:0"`

### Badge not updating

- Verify Todoist application is running
- Check that the application desktop file uses `todoist.desktop`
- View logs: `journalctl --user -u todoist-badge.service -n 50`
- Run with `--verbose` flag for debug output

### API token errors

- Verify token is correct and has not been revoked
- Check API status at [Todoist API Status](https://status.todoist.com/)
- Test token manually: `curl -H "Authorization: Bearer YOUR_TOKEN" https://api.todoist.com/rest/v2/tasks`

## License

MIT

## Contributing

Feel free to submit issues and enhancement requests!
