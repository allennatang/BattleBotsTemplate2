#imports
from abc_classes import ABot
from teams_classes import NewUser, NewPost
from chat_gpt import generateTweets, generateUsers
from getTime import sample_time
from div_array import divide_into_random_subarrays
from generateTypos import augmentTweets
import os
import random
import json

#defines
NUM_USERS=1

class Bot(ABot):
    def get_normal_subset(self, ap, sd_ap, minsize, totTweets, tweets):
        # Generate a normal sample
        n = int(random.gauss(ap, sd_ap))
        
        # Ensure n is within bounds
        n = max(minsize, min(n, totTweets))
        
        # Get a random subset of size n
        subset = random.sample(tweets, n)
        
        return subset

    def create_user(self, session_info):
        # todo logic

        output = vars(session_info).copy()  # Convert object to dictionary
        output["usernames"] = list(session_info.usernames)  # Convert set to list

        # Example:
        self.session_info = session_info
        # session_info

        #to model normal dist
        self.aP=session_info.metadata['users_average_amount_posts']
        self.sd_aP=self.aP/4

        #get user info
        prompt = "Make the user a teenage girl. Use only lowercase, and make her live somewhere trendy."
        users=generateUsers(prompt)

        # add user info
        new_users=[]
        for i in range(min(len(users),NUM_USERS)):
            new_users.append(NewUser(username=users[i]['username'],name=users[i]['name'],description=users[i]['description'],location=users[i]['location']   ))

        self.users_post_info = {}

        # Fix later
        tweet_prompt = "Use only lowercase, and talk like a teenager girl. Be sarcastic and sassy."
        # Populate the dictionary with data from each user's file
        for user in new_users:
            tweets=generateTweets(tweet_prompt)

            # I don't want to include typos
            #tweets=augmentTweets(tweets)
            totSessions=len(self.session_info.sub_sessions_info)
            # print(self.session_info)
            totTweets=len(tweets)
            desiredTweets=self.get_normal_subset(self.aP, self.sd_aP, 10, totTweets, tweets)
            # print(len(desiredTweets))
            # print(desiredTweets)

            # Simulating how users post tweets over different time periods.
            self.users_post_info[user.username] = divide_into_random_subarrays(desiredTweets,totSessions)

        # print(self.users_post_info)

        # GENERATE 2nd USER
        prompt = "Create a user that is white man in his early 30's. He lives somewhere suburban."
        users=generateUsers(prompt)
        new_users.append(NewUser(username=users[0]['username'],name=users[0]['name'],description=users[0]['description'],location=users[0]['location']   ))

        # Fix later
        tweet_prompt = "Act like a white man in his early 30's who is strongly opinionated. Your tone should be serious."
        # Populate the dictionary with data from each user's file
        user = new_users[1]
        tweets=generateTweets(tweet_prompt)
        #tweets=augmentTweets(tweets)
        totSessions=len(self.session_info.sub_sessions_info)
        # print(self.session_info)
        totTweets=len(tweets)
        desiredTweets=self.get_normal_subset(self.aP, self.sd_aP, 10, totTweets, tweets)
        # print(len(desiredTweets))
        # print(desiredTweets)

        # Simulating how users post tweets over different time periods.
        self.users_post_info[user.username] = divide_into_random_subarrays(desiredTweets,totSessions)

        # GENERATE 3rd USER

        prompt = "Create a user that is an old, British man in his 70's."
        users=generateUsers(prompt)
        new_users.append(NewUser(username=users[0]['username'],name=users[0]['name'],description=users[0]['description'],location=users[0]['location']   ))

        # Fix later
        tweet_prompt = "Act like a old, British man in his 70's. You are very confused about technology, and ask many questions, not quite understanding how Twitter works and if anyone else can see what you post."
        # Populate the dictionary with data from each user's file
        user = new_users[2]
        tweets=generateTweets(tweet_prompt)
        #tweets=augmentTweets(tweets)
        totSessions=len(self.session_info.sub_sessions_info)
        # print(self.session_info)
        totTweets=len(tweets)
        desiredTweets=self.get_normal_subset(self.aP, self.sd_aP, 10, totTweets, tweets)
        # print(len(desiredTweets))
        # print(desiredTweets)

        # Simulating how users post tweets over different time periods.
        self.users_post_info[user.username] = divide_into_random_subarrays(desiredTweets,totSessions)

        # GENERATE 4TH USER

        prompt = "Create a user that is a high-powered career woman, working as the CEO of a large company"
        users=generateUsers(prompt)
        new_users.append(NewUser(username=users[0]['username'],name=users[0]['name'],description=users[0]['description'],location=users[0]['location']   ))

        # Fix later
        tweet_prompt = "Act like a a high-powered career woman, working as the CEO of a large company. You like to use Twitter to connect with and expand your network. You often post about career openings at your company, as well as initiatives you or your company are doing."
        # Populate the dictionary with data from each user's file
        user = new_users[3]
        tweets=generateTweets(tweet_prompt)
        #tweets=augmentTweets(tweets)
        totSessions=len(self.session_info.sub_sessions_info)
        # print(self.session_info)
        totTweets=len(tweets)
        desiredTweets=self.get_normal_subset(self.aP, self.sd_aP, 10, totTweets, tweets)
        # print(len(desiredTweets))
        # print(desiredTweets)

        # Simulating how users post tweets over different time periods.
        self.users_post_info[user.username] = divide_into_random_subarrays(desiredTweets,totSessions)


        return new_users

    def generate_content(self, datasets_json, users_list):
        # todo logic

        output = datasets_json.__dict__

        # with open("generate.txt", "a") as file:
        #     json.dump(output, file, indent=4)

        # It needs to return json with the users and their description and the posts to be inserted.
        # Example:
        sessionNum=datasets_json.sub_session_id
        # print("SESSION:",sessionNum,"\n")
        # print(self.session_info.sub_sessions_info)
        
        sessionStartTime=self.session_info.sub_sessions_info[sessionNum-1]["start_time"]
        sessionEndTime=self.session_info.sub_sessions_info[sessionNum-1]["end_time"]

        posts = []

        for j in range(len(users_list)):
            username=users_list[j].username
            curUser=users_list[j]
            userId=users_list[j].user_id

            try:
                subsesh_tweets_by_user=self.users_post_info[username][sessionNum-1]
            except IndexError:
                subsesh_tweets_by_user=[]

        
            totTweets=len(subsesh_tweets_by_user)

            # allTimes=select_random_time(self.session_info.sub_sessions_info,sessionNum,totTweets)
            # allTimes=getProbTime(self.timeDistribution)
            # print("TIMES",allTimes,"\n")

            for i in range(totTweets):
                tweetTime=sample_time(self.session_info.metadata["user_distribution_across_time"], sessionStartTime, sessionEndTime)
                posts.append(NewPost(text=subsesh_tweets_by_user[i], author_id=userId, created_at=tweetTime, user=curUser))
            # posts.append(NewPost(text="Pandas are amazing!", author_id=users_list[j].user_id, created_at='2024-08-18T00:20:30.000Z',user=users_list[j]))
        return posts
        
        
        