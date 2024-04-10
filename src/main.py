from models.discoBot import DiscoBot

from dotenv import load_dotenv
import os

load_dotenv()

TOKEN = os.getenv("TOKEN")

bot = DiscoBot()
bot.run(TOKEN)
