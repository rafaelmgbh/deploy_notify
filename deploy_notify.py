import locale
import sys
from datetime import datetime

import discord
import pytz as pytz
from discord.ext import commands
from dotenv import load_dotenv

from config import Config

load_dotenv()

CHANNEL_ID = Config.CHANNEL_ID

intents = discord.Intents(members=True, guilds=True)
bot = commands.Bot(command_prefix="!", intents=intents)

locale.setlocale(locale.LC_ALL, "pt_BR.utf8")
fuso_horario_brasil = pytz.timezone("America/Sao_Paulo")
data_hora_local = datetime.now(fuso_horario_brasil)
data_hora_utc = datetime.now(pytz.utc)
dia_semana_local = data_hora_local.strftime("%A").capitalize()
data_hora_formatada_local = data_hora_local.strftime("%d de %B de %Y %H:%M:%S")
data_hora_formatada_utc = data_hora_utc.strftime("%d de %B de %Y %H:%M:%S")

mensagem = (
    f"Horário local (Brasil):  **{data_hora_formatada_local}"
    + f"**\n\n Horário do servidor (UTC):  **{data_hora_formatada_utc}"
)


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
    await channel.send(
        f"** ##############    Deploy    ############## **"
        f"\n\n **Ambiente :** {environment} \n "
        f"**Aplicação :**  {stack}, \n **Branch :**  {branch}"
        f"\n\n **{mensagem}**"
        "\n\n ** #######   **Deploy realizado com sucesso!**  ########    "
    )

    await bot.close()


bot.run(Config.TOKEN)
