import json
import re
import random

# List of filenames to read
FILENAMES = ["session_3_results.json", "session_4_results.json", "session_5_results.json"]

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

# Function to check if author_id is bot (alphanumeric) or real (numeric)
def is_bot(author_id):
    return any(char.isalpha() for char in author_id)

for post in all_posts:
    if is_bot(post['author_id']):
        bot_posts.append(post)
    else:
        real_posts.append(post)

random.shuffle(real_posts)

# Select a random sample of real tweets and return as json object, to be passed to GPT as a prompt
def getTweets(n=50):

    # Initialize dictionary of tweets
    tweets_dict = {"tweets":[]}

    # Take a random sample of n posts and append them to the dictionary
    selected_posts = random.sample(real_posts, min(n, len(real_posts))) # Use min to avoid IndexError if n > len(real_posts)
    for post in selected_posts:
        tweets_dict["tweets"].append(post['text'])

    # Convert dictionary to json
    tweets_json = json.dumps(tweets_dict)
    
    return tweets_json

# Parse the real users. Refactor this later.
# Dict
real_users = {'users':[]}
for user in all_users:
    if not user['is_bot']:
        real_users['users'].append(user)

random.shuffle(real_users['users'])

# Select a random sample of real users and return as json object, to be passed to GPT as a prompt
def getUsernames(n=50):

    users_dict = {'users':[]}
    # Take a random sample of n posts and append them to the dictionary
    selected_users = random.sample(real_users['users'], min(n, len(real_users['users'])))  # Avoid IndexError if n > len(real_posts)

    for user in selected_users:
        users_dict["users"].append(user)

    # Store in a file
    with open("random_sample_users.json", "w") as f:
        json.dump(users_dict, f)
    
    # Convert dictionary to json
    users_json = json.dumps(users_dict)
    
    return users_json
    
# print(getUsernames(50))