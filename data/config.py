"""Config for bot"""

import os

from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
MONGODB_STRING = os.getenv("MONGODB_STRING")

ADMIN_ID = 730338848
