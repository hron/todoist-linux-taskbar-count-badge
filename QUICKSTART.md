# Quick Start Guide

## 1. Get Your Todoist API Token

1. Open https://todoist.com/app/settings/account
2. Scroll down to find "API token"
3. Copy your token

## 2. Install Dependencies

```bash
cd $HOME/src/todoist-count-badge
bash setup.sh
```

Or manually:
```bash
pip install -r requirements.txt
```

## 3. Test the Script

```bash
./todoist_badge.py --token YOUR_API_TOKEN --verbose
```

You should see output like:
```
2026-02-10 14:20:00,123 - INFO - Badge updated to 3 via D-Bus
2026-02-10 14:20:00,124 - INFO - Successfully updated badge with 3 tasks
```

## 4. Set Up Automatic Updates

Choose one of these methods:

### Option A: Cron Job (every 5 minutes)

```bash
crontab -e
```

Add this line:
```cron
*/5 * * * * export TODOIST_API_TOKEN=YOUR_API_TOKEN && $HOME/src/todoist-count-badge/todoist_badge.py
```

### Option B: Systemd User Timer (Recommended)

Copy the service template:
```bash
mkdir -p ~/.config/systemd/user
cp .config/systemd-user-service.template ~/.config/systemd/user/todoist-badge.service
cp .config/systemd-user-timer.template ~/.config/systemd/user/todoist-badge.timer
```

Edit `~/.config/systemd/user/todoist-badge.service` and replace `YOUR_API_TOKEN_HERE` with your actual token.

Enable and start:
```bash
systemctl --user daemon-reload
systemctl --user enable --now todoist-badge.timer
```

Check status:
```bash
systemctl --user status todoist-badge.timer
journalctl --user -u todoist-badge.service -f
```

## 5. Verify It's Working

- Open your Todoist application
- The launcher badge should now show the number of tasks due today or overdue
- Updates will run automatically every 5 minutes

## Environment Variables

Instead of passing `--token` each time, you can set:
```bash
export TODOIST_API_TOKEN=YOUR_API_TOKEN
```

Then simply run:
```bash
./todoist_badge.py
```

## Troubleshooting

### Script shows "Failed to connect to D-Bus"

This is normal if:
- You're running via SSH without X11 forwarding
- The D-Bus session isn't available
- The Todoist application isn't running

The API will still be queried successfully.

### Badge not appearing

1. Make sure Todoist is installed and running
2. Check your desktop launcher configuration
3. Some desktop environments may require the app to be added to favorites first

### Check if Todoist D-Bus is available

```bash
dbus-send --session --print-reply --dest=org.freedesktop.DBus /org/freedesktop/DBus org.freedesktop.DBus.ListNames
```

Look for entries like `org.gnome.Todoist`, `com.canonical.Unity.LauncherEntry`, etc.

## What This Script Does

1. Fetches all your tasks from Todoist using the official API
2. Filters for tasks due today or overdue
3. Counts them
4. Updates the application launcher badge via D-Bus

The entire operation typically takes 1-2 seconds.

## Security Notes

- Your API token is sensitive! Don't commit it to git.
- The `.gitignore` file is configured to help prevent accidental commits.
- If you think your token was exposed, revoke it in Todoist settings and generate a new one.

## More Information

See `README.md` for detailed documentation and troubleshooting.
