import argparse
import os
from random import randint
from collections import defaultdict

import discord
from PIL import Image

parser = argparse.ArgumentParser(
    description="league of legends discord bot")
parser.add_argument('-t', '--token',
                    type=str, help='discord bot token')
parser.add_argument('-id', '--guild_id',
                    type=str, help='guild ID')
args = parser.parse_args()

if not os.path.exists('components'):
    os.mkdir('components')

def Crop(path):
    im = Image.open(path)
    im.save("components/original.png")

    # Size of the image in pixels (size of original image)
    # (This is not mandatory)
    width, height = im.size

    # Setting the points for cropped image
    left = randint(0, int(width * 0.7))
    top = randint(0, int(height * 0.7))

    right = left + int(width * 0.3)
    bottom = top + int(height * 0.3)

    # Cropped image of above dimension
    # (It will not change original image)
    im1 = im.crop((left, top, right, bottom))

    im1 = im1.save("components/result.png")


def generate(genre, path):
    dataset = os.listdir(path)
    for i in ['ability', 'passive', 'spell', 'splash']:
        if i in genre:
            rand = randint(0, len(dataset)-1)
            new_path = os.path.join(path, dataset[rand], genre)
            imgs = os.listdir(new_path)
            new_rand = randint(0, len(imgs)-1)
            if i == 'ability' or i == 'splash':
                Crop(os.path.join(new_path, imgs[new_rand]))
                return dataset[rand]

            else:
                im = Image.open(os.path.join(new_path, imgs[new_rand]))
                im.save("components/original.png")
                im.save("components/result.png")
                return dataset[rand]


TOKEN = args.token
GUILD_ID = args.guild_id

intents = discord.Intents.all()
client = discord.Client(intents=intents)
tree = discord.app_commands.CommandTree(client)

champ = ""
start = False
score = defaultdict(lambda: 0)
index = 1
emoji_up = '\N{THUMBS UP SIGN}'
emoji_down = "❌"


@tree.command(
    name="gen",
    description="generating",
    guild=discord.Object(id=GUILD_ID)
)
@discord.app_commands.choices(
    type=[discord.app_commands.Choice(name="splash", value="splash"),
          discord.app_commands.Choice(name="passive", value="passive"),
          discord.app_commands.Choice(name="spell", value="spell"),
          discord.app_commands.Choice(name="ability", value="ability")]
)
async def on_interaction(interaction: discord.Interaction, type: str):
    await interaction.response.defer()
    global start, champ
    champ = generate(type, 'dataset')
    embed = discord.Embed(
        title="Guess The Champ",
        url="https://www.youtube.com/watch?v=dQw4w9WgXcQ",
        description="\n\n- Type hint for hints\n\n- Type give up to end game",
        color=discord.Color.random()
    )
    file = discord.File("components/result.png", filename="result.png")
    embed.set_image(url="attachment://result.png")
    await interaction.followup.send(
        file=file,
        embed=embed
    )
    start = True


@client.event
async def on_ready():
    await tree.sync(guild=discord.Object(id=GUILD_ID))
    print("Ready!")


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    global start, score, index
    if start:
        print(champ)
        if message.content == champ:
            score[message.author] += 1
            await message.add_reaction(emoji_up)
            await message.channel.send(f"{message.author.mention} score is: {score[message.author]}")
            start = False
            index = 1
        elif message.content == "hint":
            await message.channel.send(f"name starts with {champ[0:0+index]}")
            if index < len(champ)/2:
                index += 1
        elif message.content == "give up":
            start = False
            await message.channel.send("Please wait...")
            await message.channel.send(file=discord.File("components/original.png", filename="components/original.png", spoiler=True))
            await message.channel.send(f"The answer is ||{champ}||")
        else:
            await message.add_reaction(emoji_down)

client.run(TOKEN)
