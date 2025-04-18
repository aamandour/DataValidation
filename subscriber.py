from google.cloud import pubsub_v1
import json
from datetime import datetime

# ✅ Correct project and subscription info
project_id = "dataengr-dataguru"
subscription_id = "my-topic-sub"

subscriber = pubsub_v1.SubscriberClient()
subscription_path = subscriber.subscription_path(project_id, subscription_id)

def callback(message):
    data = json.loads(message.data.decode("utf-8"))
    print("✅ Received:", data)

    # Append a timestamp to a log file
    with open("/home/amandour/timestamp.txt", "a") as f:
        f.write(f"{datetime.now()} - Received message\n")

    message.ack()

# Start listening
streaming_pull_future = subscriber.subscribe(subscription_path, callback=callback)
print(f"✅ Listening on {subscription_path}...")

try:
    streaming_pull_future.result()
except KeyboardInterrupt:
    streaming_pull_future.cancel()
