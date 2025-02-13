#!/bin/bash

# From competition to testing

# bot.py
sed -i "/^session_id = int(os.getenv('SESSION_ID'))/s/^/# /" BotTemplate/main_bot.py
sed -i "/^code_max_time = int(os.getenv('MAX_TIME'))/s/^/# /" BotTemplate/main_bot.py

sed -i '/^# session_id = [0-9]\+/s/^# //' BotTemplate/main_bot.py
sed -i '/^# code_max_time = [0-9]\+/s/^# //' BotTemplate/main_bot.py


# api_requests.py
sed -i "/^base_url = os.getenv('BASE_URL')/s/^/# /" api_requests.py
sed -i "/^authentication_token = os.getenv('AUTH_TOKEN')/s/^/# /" api_requests.py
sed -i "/^session_id = os.getenv('SESSION_ID')/s/^/# /" api_requests.py

sed -i '/^# base_url = ['\''"]/s/^# //' api_requests.py
sed -i '/^# authentication_token = ['\''"]/s/^# //' api_requests.py
sed -i '/^# session_id = [0-9]\+/s/^# //' api_requests.py

# run.sh
sed -i "/^python3 email_results.py/s/^/# /" run.sh

