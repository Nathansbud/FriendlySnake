import discord
import os
import json
from string import punctuation

with open(os.path.join(os.path.dirname(__file__), "credentials" + os.sep + "discord.json")) as jf:
    creds = json.load(jf)

client = discord.Client()

@client.event
async def on_ready():
    print(str(client.user) + " has logged in")

@client.event
async def on_message(message):
    message.content = message.content.lower()

    if message.author == client.user:
        return

    #Dad Bot
    if message.content.startswith("$reactwith "):
        react_content = message.content[len("$reactwith "):]
        alphabet = ["🇦", "🇧", "🇨", "🇩", "🇪", "🇫", "🇬", "🇭", "🇮", "🇯", "🇰", "🇱", "🇲", "🇳", "🇴", "🇵", "🇶", "🇷", "🇸", "🇹", "🇺", "🇻", "🇼", "🇽", "🇾", "🇿"]
        numbers = ["0️⃣", "1️⃣", "2️⃣", "3️⃣", "4️⃣", "5️⃣", "6️⃣", "7️⃣", "8️⃣", "9️⃣"]

        reacted = []

        reacts = {
            "I":0,
            "O":0,
            "A":0,
            "B":0,
            "E":0,
            "X":0
        }

        i_sub = "ℹ"

        o_sub = "🅾"
        o_sub_2 = "⭕"

        b_sub = "🅱"
        a_sub = "🅰"
        e_sub = "📧"

        x_sub = "✖"
        x_sub_2 = "❌"
        x_sub_3 = "❎"

        react_message = (await message.channel.history(limit=2).flatten())[1]

        for char in react_content.upper():
            if char not in reacted:
                if char.isalpha():
                    await react_message.add_reaction(alphabet[ord(char)-65])
                elif char.isdigit():
                    await react_message.add_reaction(numbers[ord(char)-48])
                reacted.append(char)
            else:
                react_sub = None
                if char == "I":
                    if reacts["I"] == 0: react_sub = i_sub
                    reacts["I"] += 1
                elif char == "O":
                    if reacts["O"] == 0: react_sub = o_sub
                    elif reacts["O"] == 1: react_sub = o_sub_2
                    reacts["O"] += 1
                elif char == "B":
                    if reacts["B"] == 0: react_sub = b_sub
                    reacts["B"]+=1
                elif char == "A":
                    if reacts["A"] == 0: react_sub = a_sub
                    reacts["A"] += 1
                elif char == "E":
                    if reacts["E"] == 0: react_sub = e_sub
                    reacts["E"]+=1
                elif char == "X":
                    if reacts["X"] == 0: react_sub = x_sub
                    elif reacts["X"] == 1: react_sub = x_sub_2
                    elif reacts["X"] == 2: react_sub = x_sub_3
                    reacts["X"]+=1
                if react_sub is not None:
                    await react_message.add_reaction(react_sub)
        return

    if message.content.startswith("I'm "):
        if len(message.content.strip()) > 3:
            address_as = str(message.content)[3:].strip().strip(punctuation)

            await message.channel.send("Hi, " + address_as + ", I'm dad-bot!")



    if " dick " in message.content or message.content.endswith(" dick") or message.content == "dick":
        await message.add_reaction("🍆")

    if " butt " in message.content or message.content.endswith(" butt") or message.content == "butt":
        await message.add_reaction("🍑")

    if " owo " in message.content or message.content.endswith(" owo") or message.content == "owo":
        react_emoji = ["🇳", "🇴", "🇹", "🇮", "🇨", "🇪", "🇸", "🇺", "🇷", "🍆"]
        for emoji in react_emoji:
            await message.add_reaction(emoji)




client.run(creds['FriendlySnake']['bot_token'])


if __name__ == '__main__':
    pass
