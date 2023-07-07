import locale
import sys

import discord
from discord.ext import commands
from dotenv import load_dotenv

from config import Config
from services.formatted_date import FormattedDate
from services.github import get_branch_info

load_dotenv()

CHANNEL_ID = Config.CHANNEL_ID
ROLE_NAME = Config.ROLE_NAME


intents = discord.Intents(members=True, guilds=True)
bot = commands.Bot(command_prefix="!", intents=intents)

locale.setlocale(locale.LC_ALL, "pt_BR.utf8")


@bot.event
async def on_ready():
    print("BOT conectado com sucesso!")
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

    guild = channel.guild
    role = discord.utils.get(guild.roles, name=ROLE_NAME)
    repo = ""
    if stack == "API":
        repo = "motbot-api"
    elif stack == "Ruby":
        repo = "sistema_motbot"
    elif stack == "React":
        repo = "motbot"

    get_branch_info(repo, branch)

    if role is not None:
        mention_string = role.mention
        mensagem = FormattedDate.get_formatted_datetime()

        await channel.send(
            f"** ##############    Deploy    ############## **"
            f"\n\n**Ambiente :** {environment} \n "
            f"\n\n**Autor :** {get_branch_info(repo, branch)} \n"
            f"**Aplicação :**  {stack} \n**Branch :**  {branch}\n\n"
            f"**{mensagem}**"
            f"\n\n{mention_string}"
        )

    await bot.close()


bot.run(Config.TOKEN)
