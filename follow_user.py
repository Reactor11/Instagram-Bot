import os
import sys
from instabot import Bot

bot = Bot(filter_users=True)
users_to_follow = bot.read_list_from_file('followers.txt')
if not users_to_follow:
    exit()
else:
    print("Found %d users in file." % len(users_to_follow))

bot.login(username=str(sys.argv[1]), password=str(sys.argv[2]))

bot.follow_users(users_to_follow)
