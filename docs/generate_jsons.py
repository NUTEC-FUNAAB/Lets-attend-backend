#!/usr/bin/env python3
""" generates a dictionary pf users and events """
import random
import uuid
from datetime import datetime

# Sample list of user first names, last names, and emails
first_names = ["John", "Alice", "Bob", "Eva", "David", "Linda", "Mike", "Sarah", "Chris", "Emily"]
last_names = ["Smith", "Johnson", "Brown", "Davis", "Wilson", "Lee", "Harris", "Clark", "Anderson", "Thomas"]
emails = ["john@example.com", "alice@example.com", "bob@example.com", "eva@example.com", "david@example.com",
          "linda@example.com", "mike@example.com", "sarah@example.com", "chris@example.com", "emily@example.com"]

# Generate 10 users
users = []
for i in range(10):
    user = {
        "id": str(uuid.uuid4()),
        "created_at": datetime.utcnow().isoformat(),
        "first_name": random.choice(first_names),
        "last_name": random.choice(last_names),
        "gender": random.choice(["male", "female"]),
        "date_of_birth": "1990-01-01",
        "email": emails[i],
        "phone": f"+123456789{i}",
        "password": "hashed_password_here",  # You should hash the actual password
    }
    users.append(user)

# Sample list of event names and descriptions
event_names = ["Birthday Party", "Conference", "Music Festival", "Wedding", "Product Launch", "Charity Event", "Workshop", "Sports Event", "Art Exhibition", "Food Festival"]
event_descriptions = ["Join us for a fun-filled evening!", "Learn from industry experts.", "Enjoy live music performances.", "A celebration of love.", "Introducing our latest product.", "Support a good cause.", "Hands-on learning experience.", "Cheer for your favorite team.", "Explore amazing artworks.", "Delicious food from around the world."]

# Generate 10 events with random hosts from the users
events = []
for i in range(10):
    event = {
        "id": str(uuid.uuid4()),
        "created_at": datetime.utcnow().isoformat(),
        "name": random.choice(event_names),
        "description": random.choice(event_descriptions),
        "event_type": random.choice(["public", "private"]),
        "start_time": "2023-09-01T10:00:00",
        "end_time": "2023-09-01T18:00:00",
        "location": f"Location {i+1}",
        "host": random.choice(users)["id"],
        "price": round(random.uniform(0, 100), 2),
    }
    events.append(event)

# Print the JSON dictionaries for users and events
print("Users:")
for user in users:
    print(user)

print("\nEvents:")
for event in events:
    print(event)
