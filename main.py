import sys

import discord
from discord.ext import commands
from dotenv import load_dotenv

from config import Config

load_dotenv()

CHANNEL_ID = Config.CHANNEL_ID

intents = discord.Intents(members=True, guilds=True)
bot = commands.Bot(command_prefix="!", intents=intents)


@bot.event
async def on_ready():
    print(f"BOT {bot.user.name} conectado com sucesso!")
    print("--------------------------")

    if len(sys.argv) < 3:
        print(
            "Argumentos insuficientes. Uso:  "
            "python nome_do_script.py ambiente stack branch "
        )
        await bot.close()
        return

    environment = sys.argv[1]
    stack = sys.argv[2]
    branch = sys.argv[3]

    channel = bot.get_channel(CHANNEL_ID)
    if channel is None:
        channel = await bot.fetch_channel(CHANNEL_ID)
    await channel.send(
        f"** Deploy realizado ** \n\n **Ambiente :** {environment} \n "
        f"**Aplicação :**  {stack}, \n **Branch :**  {branch}"
    )

    await bot.close()


bot.run(Config.TOKEN)
