import os
import time
import logging
import requests
import docker

# Setup basic logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Configuration from environment variables
WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL")
MONITOR_CONTAINER_NAME = os.getenv("MONITOR_CONTAINER_NAME")
CHECK_INTERVAL = int(os.getenv("CHECK_INTERVAL", "60"))

def send_discord_alert(container_name):
    """Send an alert to the configured Discord webhook."""
    if not WEBHOOK_URL:
        logger.warning("DISCORD_WEBHOOK_URL not set! Cannot send alert.")
        return
        
    data = {
        "username": "Container Monitor",
        "embeds": [
            {
                "title": "🚨 Container Alert",
                "description": f"The container **`{container_name}`** is currently down or cannot be found!",
                "color": 16711680, # Red color
                "thumbnail": {
                    "url": "https://img.icons8.com/color/96/000000/docker.png"
                },
                "fields": [
                    {
                        "name": "Status",
                        "value": "🔴 Down / Error",
                        "inline": True
                    },
                    {
                        "name": "Time",
                        "value": f"<t:{int(time.time())}:R>",
                        "inline": True
                    }
                ],
                "footer": {
                    "text": "Container Health Monitor"
                }
            }
        ]
    }
    try:
        req = requests.post(WEBHOOK_URL, json=data, timeout=10)
        req.raise_for_status()
        logger.info("Discord alert sent successfully.")
    except Exception as e:
        logger.error(f"Failed to send alert: {e}")

def main():
    if not MONITOR_CONTAINER_NAME:
        logger.error("MONITOR_CONTAINER_NAME environment variable is not set. Exiting.")
        return

    logger.info(f"Starting monitor for container: '{MONITOR_CONTAINER_NAME}' every {CHECK_INTERVAL} seconds.")
    
    # Initialize docker client
    try:
        client = docker.from_env()
    except Exception as e:
        logger.error(f"Cannot connect to the Docker daemon: {e}")
        logger.error("Make sure you have mounted /var/run/docker.sock into this container.")
        return

    was_down = False

    while True:
        try:
            container = client.containers.get(MONITOR_CONTAINER_NAME)
            if container.status != "running":
                logger.warning(f"Container '{MONITOR_CONTAINER_NAME}' is {container.status}.")
                if not was_down:
                    send_discord_alert(MONITOR_CONTAINER_NAME)
                    was_down = True
            else:
                if was_down:
                    logger.info(f"Container '{MONITOR_CONTAINER_NAME}' is back online.")
                    was_down = False
                else:
                    logger.debug(f"Container '{MONITOR_CONTAINER_NAME}' is running.")
        except docker.errors.NotFound:
            logger.warning(f"Container '{MONITOR_CONTAINER_NAME}' not found.")
            if not was_down:
                send_discord_alert(MONITOR_CONTAINER_NAME)
                was_down = True
        except Exception as e:
            logger.error(f"Error checking container: {e}")

        time.sleep(CHECK_INTERVAL)

if __name__ == "__main__":
    main()
