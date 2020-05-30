"""
    instabot example
    Workflow:
        Get total or filtered followers or followings to file.
"""

import argparse
import os
import sys

sys.path.append(os.path.join(sys.path[0], "../"))
from instabot import Bot  # noqa: E402


bot = Bot()
bot.login(username=sys.argv[1], password=sys.argv[2])

try:
    user_id = bot.get_user_id_from_username("jenniferaniston")
except Exception as e:
    bot.logger.error("{}".format(e))
    exit()

bot.api.get_total_followers_or_followings(
    user_id=user_id,
    amount=3300000,
    which="followers",
    to_file="temp.txt",
    overwrite=True,
    usernames="jenniferaniston",
)
