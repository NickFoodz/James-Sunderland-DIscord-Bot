import os
import random
import re
import time

import discord

TOKEN = "PASTE TOKEN HERE"

# Folder this script lives in, so the image is found no matter where you run it from
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Words/phrases that set James off. Matched as whole words, case-insensitive.
TRIGGER_WORDS = [
    "wife", "mary", "dead", "missing", "lost", "silent hill", "fog",
    "town", "letter", "lakeview", "hotel", "pyramid", "nurse",
    "radio", "static", "sorry", "alone", "help", "seen", "looking",
]

# Lines James might say. Add your own!
# A plain string sends text. An IMAGE: prefix sends an image from this folder.
RESPONSES = [
    "Mary said this once",
    "That sentence... it reminds me of my dead wife",
    "Mary? Is that you?",
    "I'm just looking for my wife",
    "Do you know where Mary is?",
    "Have you seen my dead wife?",
    "Ask me about my dead wife",
    #Custom images, just add lines with the name as a string with IMAGE: prefix, images must be in folder of script
    "IMAGE:james-sunderland.gif",
    "IMAGE:jamessmile.jpg",
    "IMAGE:jpeam.gif",
    "IMAGE:jhot.gif"
]

COOLDOWN_SECONDS = 1.5   # per-channel, so he doesn't spam
REPLY_CHANCE = 1.0      # 1.0 = always respond when triggered

pattern = re.compile(
    r"\b(" + "|".join(re.escape(w) for w in TRIGGER_WORDS) + r")\b",
    re.IGNORECASE,
)
last_reply = {}  # channel_id -> timestamp

intents = discord.Intents.default()
intents.message_content = True  # must also be enabled in the Developer Portal
client = discord.Client(intents=intents)


@client.event
async def on_ready():
    print(f"Logged in as {client.user}")


@client.event
async def on_message(message: discord.Message):
    if message.author.bot:
        return
    if not pattern.search(message.content):
        return

    now = time.time()
    if now - last_reply.get(message.channel.id, 0) < COOLDOWN_SECONDS:
        return
    if random.random() > REPLY_CHANCE:
        return

    last_reply[message.channel.id] = now

    choice = random.choice(RESPONSES)

    if choice.startswith("IMAGE:"):
        filename = choice[len("IMAGE:"):]
        path = os.path.join(BASE_DIR, filename)
        if os.path.isfile(path):
            await message.reply(
                file=discord.File(path),
                mention_author=False,
            )
        else:
            print(f"Image not found: {path}")
    else:
        await message.reply(choice, mention_author=False)


client.run(TOKEN)