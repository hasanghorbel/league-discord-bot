from random import randint

import discord
from discord import app_commands

from cropper import Crop
from scraper import Scrape

TOKEN = ""  # insert token
GUILD_ID = ""  # insert guild id

intents = discord.Intents.all()
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

guess = ""
score = 0
fails = 0
hint = False
start = False
champ = None


@tree.command(
    name="gen",
    description="generating",
    guild=discord.Object(id=GUILD_ID))
@app_commands.choices(
    type=[app_commands.Choice(name="skin", value=0),
          app_commands.Choice(name="passive", value=1),
          app_commands.Choice(name="spell", value=2),
          app_commands.Choice(name="ability", value=3)]
)
async def generate(interaction: discord.Interaction, type: int):
    await interaction.response.defer()
    global guess, start, champ
    champ = Scrape()
    guess = champ[0]
    embed = discord.Embed(
        title="Guess the sauce",
        url="https://www.youtube.com/watch?v=dQw4w9WgXcQ",
        description="you might not get it!\n#type hint for hints!\n#type give up to end game!",
        color=discord.Color.random()
    )
    if type == 0:
        Crop(champ[1][type][randint(0, len(champ[1][type])-1)])
        file = discord.File("file.png", filename="image.png")
        embed.set_image(url="attachment://image.png")
        await interaction.followup.send(
            file=file,
            embed=embed
        )
        start = True
    else:
        embed.set_image(url=champ[1][type][randint(0, len(champ[1][type])-1)])
        await interaction.followup.send(embed=embed)
        start = True


@client.event
async def on_ready():
    await tree.sync(guild=discord.Object(id=GUILD_ID))
    print("Ready!")


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    global guess, score, fails, hint, start
    if start:
        if message.content == guess:
            await message.channel.send('you guessed it!')
            guess = ""
            score += 1
            start = False
        elif message.content == "hint":
            new_champ = champ[1][randint(0, 3)]
            embed = discord.Embed(
                title="Guess the sauce",
                url="https://www.youtube.com/watch?v=dQw4w9WgXcQ",
                description="you might not get it!\n(type hint for hints)\n(type give up to end game)",
                color=discord.Color.random()
            )
            embed.set_image(
                url=new_champ[randint(0, len(new_champ)-1)])
            await message.channel.send(embed=embed)
        elif message.content == "give up":
            await message.channel.send(f'True answer : {guess}\ngame over\nyour score is : {score}')
            guess = ""
            score = 0
            fails = 0
            start = False
        elif fails == 2:
            await message.channel.send('need a hint?')
            fails += 1
        elif fails == 3:
            await message.channel.send(f'True answer : {guess}\ngame over\nyour score is : {score}')
            guess = ""
            score = 0
            fails = 0
            start = False
        else:
            fails += 1

client.run(TOKEN)
