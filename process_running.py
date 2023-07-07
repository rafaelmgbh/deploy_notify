import asyncio

import discord
from discord.ext import commands

from config import Config
from services.process_checker import check_processes
from services.schedule import should_send_message

intents = discord.Intents(members=True, guilds=True)
bot = commands.Bot(command_prefix="!", intents=intents)

interval_minutes = int(Config.INTERVAL_MINUTES)


async def main():
    await bot.start(Config.TOKEN)


@bot.event
async def on_ready():
    print("BOT conectado com sucesso!")
    print("--------------------------")

    channel_id = Config.CHANNEL_ID
    channel = bot.get_channel(channel_id)
    if channel is None:
        channel = await bot.fetch_channel(channel_id)

    processes = ["motbot.py", "main.py"]
    while True:
        result = check_processes(processes)
        title = (
            f"** ##############    Monitoramento Aplicações"
            "############## **\n\n"
            f"```    Ambiente : {Config.ENVIRONMENT} ```"
            "```    Intervalo de Verificação : "
            f"{Config.INTERVAL_MINUTES} minutos ``` \n "
        )
        for process in result:
            title += process

        if should_send_message():
            await channel.send(title)

        await asyncio.sleep(int(interval_minutes) * 10)


if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.create_task(main())
    loop.run_forever()
