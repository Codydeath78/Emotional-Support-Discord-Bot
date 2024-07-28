import os
import requests
import discord
import json
import random
from replit import db
from keep_alive import keep_alive

intents = discord.Intents.default()
intents.message_content = True

client = discord.Client(intents=intents)
sad_words = ["sad", "depressed", "unhappy", "angry", "miserable"]
achievement_words = ["first", "high", "it", "award"]
encouraging_words = ["Cheer Up", "Hang in there!", "You are a good person!"]
celebration_words = [
    "Congrats!", "Great job, Sport!", "This calls for a celebration!"
]

if "celebration_responding" not in db:
    db["celebration_responding"] = True

if "encouragement_responding" not in db:
    db["encouragement_responding"] = True


def get_quote():
    response = requests.get("https://zenquotes.io/api/random")
    json_data = json.loads(response.text)
    quote = json_data[0]['q'] + " -" + json_data[0]['a']
    return (quote)


#####################################################################


def update_celebration(celebration_message):
    if "celebrations" in db:
        celebrations = db["celebrations"]
        celebrations.append(celebration_message)
        db["celebrations"] = celebrations
    else:
        db["celebrations"] = [celebration_message]


def delete_celebration(index):
    celebrations = db["celebrations"]
    if len(celebrations) > index:
        del celebrations[index]
    db["celebrations"] = celebrations


#####################################################################


def update_encouragements(encouraging_message):
    if "encouragements" in db:
        encouragements = db["encouragements"]
        encouragements.append(encouraging_message)
        db["encouragements"] = encouragements
    else:
        db["encouragements"] = [encouraging_message]


def delete_encouragment(index):
    encouragements = db["encouragements"]
    if len(encouragements) > index:
        del encouragements[index]
    db["encouragements"] = encouragements


#####################################################################


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('$hello'):
        await message.channel.send('Hello!')
    if message.content.startswith('$Hello_Bro'):
        await message.channel.send('𝓗𝓮𝔂 𝓑𝓻𝓸')
    if message.content.startswith('$inspire'):
        quote = get_quote()
        await message.channel.send(quote)

    ##########################celebration_words##########################

    celebration_options = celebration_words
    if "celebrations" in db:
        celebration_options = celebration_options + list(db["celebrations"])

    if db["celebration_responding"] and any(word in message.content
                                            for word in achievement_words):
        await message.channel.send(random.choice(celebration_options))

    if message.content.startswith("$new_celebration"):
        celebration_parts = message.content.split("$new_celebration", 1)
        if len(celebration_parts) == 2:  # Check if there are two elements
            celebration_message = celebration_parts[1]
            update_celebration(celebration_message)
            await message.channel.send("New celebration message added.")
        else:
            await message.channel.send(
                "Invalid command format. Use '$new_celebration <message>'")

    if message.content.startswith("$del_celebration"):
        try:
            celebrations = []
            index = int(message.content.split("$del_celebration", 1)[1])
            if "celebrations" in db:
                #index = int(message.content.split("$del_celebration", 1)[1])
                #delete_celebration(index)
                celebrations = list(db["celebrations"])
                if 0 <= index < len(celebrations):
                    del celebrations[index]
                    db["celebrations"] = celebrations
                    await message.channel.send(
                        f"Celebration message at index {index} deleted.")
                else:
                    await message.channel.send(
                        f"Invalid index. Current celebration messages: {celebrations}. Try again."
                    )
            if len(celebrations) == 0:
                await message.channel.send("No celebration messages to delete."
                                           )
                #await message.channel.send(celebrations)
        except (IndexError, ValueError):
            await message.channel.send(
                "Invalid command format. Use '$del_celebration <index>' where <index> is the number of the celebration message to delete."
            )

    if message.content.startswith("$list_celebration"):
        celebrations = []
        if "celebrations" in db:
            celebrations = list(db["celebrations"])
        await message.channel.send(celebrations)

#####################end of celebration_words########################
#####################################################################
##########################encouraging_words##########################

    encouragement_options = encouraging_words
    if "encouragements" in db:
        encouragement_options = encouragement_options + list(
            db["encouragements"])

    if db["encouragement_responding"] and any(word in message.content
                                              for word in sad_words):
        await message.channel.send(random.choice(encouragement_options))

    if message.content.startswith("$new_encouragement"):
        encouragement_parts = message.content.split("$new_encouragement", 1)
        if len(encouragement_parts) == 2:
            encouraging_message = encouragement_parts[1]
            update_encouragements(encouraging_message)
            await message.channel.send("New encouraging message added.")
        else:
            await message.channel.send(
                "Invalid command format. Use '$new_encouragement <message>'")

    if message.content.startswith("$del_encouragement"):
        try:
            encouragements = []
            index = int(message.content.split("$del_encouragement", 1)[1])
            if "encouragements" in db:
                #index = int(message.content.split("$del_encouragement", 1[1])
                #delete_encouragment(index)
                encouragements = list(db["encouragements"])
                if 0 <= index < len(encouragements):
                    del encouragements[index]
                    db["encouragements"] = encouragements
                    await message.channel.send(f"Encouragement message at index {index} deleted.")
                else:
                    await message.channel.send(f"Invalid index. Current encouragement messages: {encouragements}. Try again.")
            if len(encouragements) == 0:
                await message.channel.send("No encouragement messages to delete.")
                #await message.channel.send(encouragements)
        except (IndexError, ValueError):
            await message.channel.send(
                "Invalid command format. Use '$del_encouragement <index>' where <index> is the number of the encouragement message to delete."
            )

    if message.content.startswith("$list_encouragement"):
        encouragements = []
        if "encouragements" in db:
            encouragements = list(db["encouragements"])
        await message.channel.send(encouragements)


#####################end of encouraging_words########################

    if message.content.startswith("$celebration_responding"):
        value = message.content.split("$celebration_responding ", 1)[1]

        if value.lower() == "true":
            db["celebration_responding"] = True
            await message.channel.send("Responding is on.")
        else:
            db["celebration_responding"] = False
            await message.channel.send("Responding is off.")

    if message.content.startswith("$encouragement_responding"):
        value = message.content.split("$encouragement_responding ", 1)[1]

        if value.lower() == "true":
            db["encouragement_responding"] = True
            await message.channel.send("Responding is on.")
        else:
            db["encouragement_responding"] = False
            await message.channel.send("Responding is off.")

keep_alive()

###############################TRY###################################
try:
    token = os.getenv("TOKEN") or ""
    if token == "":
        raise Exception("Please add your token to the Secrets pane.")
    client.run(token)
except discord.HTTPException as e:
    if e.status == 429:
        print(
            "The Discord servers denied the connection for making too many requests"
        )
        print(
            "Get help from https://stackoverflow.com/questions/66724687/in-discord-py-how-to-solve-the-error-for-toomanyrequests"
        )
    else:
        raise e
#########################end of TRY##################################