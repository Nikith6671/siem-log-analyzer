import logging
import os
import random

# Ensure logs folder exists
if not os.path.exists("logs"):
    os.makedirs("logs")

log_file = os.path.join("logs", "system.log")

logging.basicConfig(
    filename=log_file,
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def generate_logs():
    events = [
        "User login successful",
        "User login failed",
        "File accessed",
        "Unauthorized access attempt",
        "System error occurred"
    ]

    for _ in range(20):
        event = random.choice(events)

        if "failed" in event or "Unauthorized" in event:
            logging.warning(event)
        else:
            logging.info(event)

if __name__ == "__main__":
    generate_logs()
    print("Logs generated successfully!")