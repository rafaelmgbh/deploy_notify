import asyncio
import datetime

import discord
import psutil
from discord.ext import commands

from config import Config

intents = discord.Intents(members=True, guilds=True)
bot = commands.Bot(command_prefix="!", intents=intents)


def format_time(seconds):
    if seconds < 60:
        return f"{seconds:.2f} segundo(s)"
    elif seconds < 3600:
        return f"{seconds / 60:.2f} minuto(s)"
    else:
        return f"{seconds / 3600:.2f} hora(s)"


def get_process_running_time(process_name):
    for proc in psutil.process_iter(["name", "cmdline", "create_time"]):
        if process_name in " ".join(proc.info["cmdline"]):
            create_time = proc.info["create_time"]
            current_time = datetime.datetime.now().timestamp()
            running_time = current_time - create_time
            return running_time
    return None


async def check_processes(processes, channel):
    process_mapping = {
        "motbot.py": "Motbot-API",
        "main.py": "Notification-hub",
    }
    emojis = {
        True: "\U0001F604",  # Emoji feliz
        False: "\U0001F621",  # Emoji de raiva
    }

    while True:
        for process_name in processes:
            process_found = False
            for proc in psutil.process_iter(["name", "cmdline"]):
                if process_name in " ".join(proc.info["cmdline"]):
                    process_found = True
                    running_time = get_process_running_time(process_name)

                    if running_time is not None:
                        emoji = emojis[True]
                        message = (
                            " - O processo "
                            f"{process_mapping.get(process_name, process_name)}"  # noqa
                            "está em execução.\n"
                        )
                        message += (
                            "Tempo de execução:"
                            f"{format_time(running_time)}\n\n"
                        )
                        message += (
                            "********************************************"
                        )
                    else:
                        emoji = emojis[False]
                        message = " O processo "
                        f"{process_mapping.get(process_name, process_name)}"
                        "está em execução, mas não foi "
                        "possível obter o tempo de execução.\n"

                    await channel.send(f"{emoji} {message}\n")

                    break

            if not process_found:
                await channel.send(
                    f"{emojis[False]} - O processo "
                    f"{process_mapping.get(process_name, process_name)} "
                    "não está em execução.\n"
                )

        # Espera 1 hora antes de verificar novamente
        await asyncio.sleep(3600)


@bot.event
async def on_ready():
    print("BOT conectado com sucesso!")
    print("--------------------------")

    channel_id = (
        Config.CHANNEL_ID
    )  # Substitua pelo ID do canal que deseja enviar as mensagens
    channel = bot.get_channel(channel_id)
    if channel is None:
        channel = await bot.fetch_channel(channel_id)

    processes = ["motbot.py", "main.py"]
    await check_processes(processes, channel)


if __name__ == "__main__":
    bot.run(Config.TOKEN)  # Substitua pelo token do seu bot
