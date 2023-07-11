import locale
import sys

import discord
from discord.ext import commands
from dotenv import load_dotenv

from config import Config
from services.formatted_date import FormattedDate
from services.github import get_branch_info
from utils.enumEnvironment import enumEnvironment

load_dotenv()

CHANNEL_ID = Config.CHANNEL_ID
ROLE_NAME = Config.ROLE_NAME
USER_ID = Config.USER_ID


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

    environment = Config.ENVIRONMENT
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

    user = None
    if environment == enumEnvironment.Production.value:
        user = await bot.fetch_user(USER_ID)

    if role is not None:
        mention_string = role.mention
        mensagem = FormattedDate.get_formatted_datetime()
        info = get_branch_info(repo, branch)

        if user is not None:
            message_content = (
                f"** ##############    Deploy    ############## **"
                f"\n\n**Ambiente :** {environment} \n "
                f"**Autor :** {info['author']}\n"
                f"**Descrição**: \n\n {info['description']} \n\n"
                f"**Aplicação :**  {stack} \n**Branch :**  {branch}\n\n"
                f"**{mensagem}**"
                f"\n\n{mention_string} {user.mention}"
            )
            await channel.send(message_content)
        else:
            message_content = (
                f"** ##############    Deploy    ############## **"
                f"\n\n**Ambiente :** {environment} \n "
                f"**Autor :** {info['author']}\n"
                f"**Descrição**: \n\n {info['description']} \n\n"
                f"**Aplicação :**  {stack} \n**Branch :**  {branch}\n\n"
                f"**{mensagem}**"
                f"\n\n{mention_string}"
            )

            await channel.send(message_content)

        await bot.close()


bot.run(Config.TOKEN)
