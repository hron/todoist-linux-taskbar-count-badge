#!/usr/bin/env python3
"""
Todoist Count Badge - Updates the count badge on todoist.desktop via D-Bus
This script fetches tasks from Todoist API and displays the count of tasks
scheduled for today or overdue.
"""

import requests
import dbus
from datetime import datetime, date
from typing import Optional, List, Dict
import argparse
import sys
import logging
import os

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
log_level = os.getenv("LOG_LEVEL", "INFO")
logging.basicConfig(level=getattr(logging, log_level))
logger = logging.getLogger(__name__)
logger.setLevel(log_level)

class TodoistBadgeUpdater:
    """Updates Todoist count badge via D-Bus using Todoist API."""
    
    TODOIST_API_URL = "https://api.todoist.com/rest/v2"
    FREEDESKTOP_APP_ID = "org.gnome.Todoist"
    
    def __init__(self, api_token: str):
        """
        Initialize the updater with a Todoist API token.
        
        Args:
            api_token: Your Todoist API token
        """
        self.api_token = api_token
        self.session = requests.Session()
        self.session.headers.update({
            "Authorization": f"Bearer {api_token}",
            "Content-Type": "application/json"
        })
    
    def get_active_tasks(self) -> List[Dict]:
        """
        Fetch all active tasks from Todoist.
        
        Returns:
            List of task dictionaries from the API
            
        Raises:
            requests.RequestException: If API call fails
        """
        try:
            response = self.session.get(
                f"{self.TODOIST_API_URL}/tasks",
                params={"filter": "today | overdue"}
            )
            response.raise_for_status()
            logger.debug(f"API response: {response.json()}")
            return response.json()
        except requests.RequestException as e:
            logger.error(f"Failed to fetch tasks from Todoist API: {e}")
            raise
    
    def count_todays_tasks(self) -> int:
        """
        Count tasks scheduled for today or overdue.
        
        Returns:
            Number of tasks due today or overdue
        """
        try:
            tasks = self.get_active_tasks()
            logger.error(f"Fetched {len(tasks)} tasks from Todoist API")
            return len(tasks)
        except Exception as e:
            logger.error(f"Error counting tasks: {e}")
            return 0
    
    def update_badge_dbus(self, count: int) -> bool:
        """
        Update the count badge on todoist.desktop via D-Bus.
        
        Args:
            count: The count to display on the badge
            
        Returns:
            True if successful, False otherwise
        """
        try:
            bus = dbus.SessionBus()
            
            # Get the application object
            app_object = bus.get_object(
                'org.freedesktop.DBus',
                '/org/freedesktop/DBus'
            )
            
            # Try to update the badge using the standard D-Bus interface
            # This uses the org.freedesktop.Application interface
            todoist_app = bus.get_object(
                'org.gnome.Todoist',
                '/org/gnome/Todoist'
            )
            
            # Set the badge count using the UnityLauncherEntry interface
            # or org.freedesktop.Application.SetProperty
            properties_iface = dbus.Interface(
                todoist_app,
                'org.freedesktop.DBus.Properties'
            )
    
            # Update the badge count
            properties_iface.Set(
                'org.freedesktop.Application',
                'badge',
                dbus.UInt32(count)
            )
            
            logger.info(f"Badge updated to {count} via D-Bus")
            return True
            
        except dbus.DBusException as e:
            logger.warning(f"D-Bus error (trying alternative method): {e}")
            return self._update_badge_unity(count)
        except Exception as e:
            logger.error(f"Failed to update badge via D-Bus: {e}")
            return False
    
    def _update_badge_unity(self, count: int) -> bool:
        """
        Alternative method using Unity LauncherEntry for badge updates.
        
        Args:
            count: The count to display on the badge
            
        Returns:
            True if successful, False otherwise
        """
        try:
            bus = dbus.SessionBus()
            
            # Use Unity LauncherEntry interface
            launcher_entry = bus.get_object(
                'com.canonical.Unity.LauncherEntry',
                '/com/canonical/unity/launcher/entry/0'
            )
            
            properties = dbus.Interface(
                launcher_entry,
                'org.freedesktop.DBus.Properties'
            )
            
            # Set badge count
            properties.Set(
                'com.canonical.Unity.LauncherEntry',
                'count',
                dbus.Int64(count)
            )
            
            logger.info(f"Badge updated to {count} via Unity LauncherEntry")
            return True
            
        except Exception as e:
            logger.error(f"Failed to update badge via Unity LauncherEntry: {e}")
            return False
    
    def update(self) -> Optional[int]:
        """
        Perform the complete update: fetch tasks and update badge.
        
        Returns:
            The count of tasks, or None if update failed
        """
        try:
            count = self.count_todays_tasks()
            self.update_badge_dbus(count)
            return count
        except Exception as e:
            logger.error(f"Update failed: {e}")
            return None


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Update Todoist count badge via D-Bus"
    )
    parser.add_argument(
        "--token",
        required=False,
        help="Todoist API token (defaults to TODOIST_API_TOKEN env var)"
    )
    parser.add_argument(
        "--verbose",
        "-v",
        action="store_true",
        help="Enable verbose logging"
    )
    
    args = parser.parse_args()
    
    if args.verbose:
        logger.setLevel(logging.DEBUG)
    
    # Get API token from argument or environment variable
    api_token = args.token
    if not api_token:
        import os
        api_token = os.getenv("TODOIST_API_TOKEN")
    
    if not api_token:
        logger.error(
            "Todoist API token required. "
            "Provide via --token or TODOIST_API_TOKEN environment variable"
        )
        sys.exit(1)
    
    # Create updater and run
    updater = TodoistBadgeUpdater(api_token)
    count = updater.update()
    
    if count is not None:
        logger.info(f"Successfully updated badge with {count} tasks")
        sys.exit(0)
    else:
        logger.error("Failed to update badge")
        sys.exit(1)


if __name__ == "__main__":
    main()
