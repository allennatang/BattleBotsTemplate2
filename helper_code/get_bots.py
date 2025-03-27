import json
import re
import random

# List of filenames to read
FILENAMES = ["data/session_13_results.json"]

# Is this being used??
# Function to clean and load JSON data
def load_and_clean_json(filename):
    with open(filename, 'r', encoding='utf-8') as f:
        raw_data = f.read()
    # Clean improperly escaped emojis
    cleaned_data = re.sub(r'\\([^n"\\\s])\\?', r'\1', raw_data)
    # Validate and return the JSON data
    try:
        return json.loads(cleaned_data)
    except json.JSONDecodeError as e:
        print(f"JSONDecodeError in {filename}: {e}")
        return {"posts": []}  # Return empty structure if there's an error



# Function to check if author_id is bot (alphanumeric) or real (numeric)
def is_bot(author_id):
    return any(char.isalpha() for char in author_id)

def main():
    # Combine all posts from multiple files
    all_posts = []
    all_users=[]
    for filename in FILENAMES:
        data = load_and_clean_json(filename)
        all_posts.extend(data.get('posts', []))
        all_users.extend(data.get('users', []))

    # print(all_users[0])

    # Separate posts by bots (alphanumeric) vs real accounts (numeric)
    bot_posts = []
    real_posts = []

    for post in all_posts:
        if is_bot(post['author_id']):
            bot_posts.append(post)
        else:
            real_posts.append(post)

    print(real_posts)
if __name__ == "__main__":
    main()

