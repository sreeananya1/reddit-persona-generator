# reddit_persona_generator.py

import praw
import openai
import os
import re
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# OpenAI setup
openai.api_key = os.getenv("OPENAI_API_KEY")

# Reddit API setup
reddit = praw.Reddit(
    client_id=os.getenv("REDDIT_CLIENT_ID"),
    client_secret=os.getenv("REDDIT_CLIENT_SECRET"),
    user_agent="persona-generator-script"
)

def extract_username(url):
    match = re.search(r"reddit.com/user/([^/]+)/?", url)
    return match.group(1) if match else None

def fetch_user_content(username, limit=50):
    user = reddit.redditor(username)
    posts, comments = [], []
    try:
        for submission in user.submissions.new(limit=limit):
            posts.append(f"[POST] Title: {submission.title}\nText: {submission.selftext}\nSubreddit: {submission.subreddit}\n")
        for comment in user.comments.new(limit=limit):
            comments.append(f"[COMMENT] {comment.body}\nSubreddit: {comment.subreddit}\n")
    except Exception as e:
        print("Error fetching user data:", e)
    return posts, comments

def generate_persona(posts, comments):
    content = "\n".join(posts + comments)
    prompt = (
        "You are an AI that creates user personas from Reddit profiles. "
        "Analyze the following content (posts and comments) and infer a persona. "
        "Include attributes like age range, interests, writing tone, personality traits, values, activity frequency, etc. "
        "Also cite the post/comment excerpts that helped infer each trait.\n\n"
        f"Content:\n{content}\n\nPersona:\n"
    )
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7
    )
    return response.choices[0].message.content.strip()

def save_persona(username, persona_text):
    filename = f"{username}_persona.txt"
    with open(filename, "w", encoding="utf-8") as f:
        f.write(persona_text)
    print(f"Saved persona to {filename}")

def main():
    import argparse
    parser = argparse.ArgumentParser(description="Reddit User Persona Generator")
    parser.add_argument("--url", required=True, help="Reddit profile URL (e.g., https://www.reddit.com/user/kojied/)")
    args = parser.parse_args()

    username = extract_username(args.url)
    if not username:
        print("Invalid Reddit URL")
        return

    print(f"Fetching data for user: {username}")
    posts, comments = fetch_user_content(username)
    if not posts and not comments:
        print("No content found.")
        return

    print("Generating persona...")
    persona = generate_persona(posts, comments)
    save_persona(username, persona)

if __name__ == "__main__":
    main()