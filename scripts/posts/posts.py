import os
import requests
import csv
from datetime import datetime

api_url = os.getenv("API_URL")
if not api_url:
    raise ValueError("Environment variable API_URL is not set")

headers = {
    "Content-Type": "application/json"
}

def create_post(author, title, body):
    data = {
        "author": author,
        "title": title,
        "body": body,
        "date": datetime.now().isoformat()
    }
    response = requests.post(api_url, json=data, headers=headers)
    if response.status_code == 200:
        print(f"Post created: {response.status_code}, {response.text}")
    else:
        print(f"Error creating post: {response.status_code}, {response.text}")

def list_and_save_posts():
    params = {"all": "true"}
    response = requests.get(api_url, params=params, headers=headers)
    
    if response.status_code == 200:
        posts = response.json()
        print(f"{len(posts)} posts received")

        if not posts:
            print("No data to save")
            return

        fieldnames = list(posts[0].keys()) 
        with open("/app/data/posts.csv", "w", newline="", encoding="utf-8") as file:
            writer = csv.DictWriter(file, fieldnames=fieldnames, quotechar='"', quoting=csv.QUOTE_ALL)
            writer.writeheader()
            for post in posts:
                writer.writerow(post)

        print("Posts saved to posts.csv")
    else:
        print(f"Error getting posts: {response.status_code}, {response.text}")

create_post("Steve Blinski", "New Post", "This is a new post.")
list_and_save_posts()
