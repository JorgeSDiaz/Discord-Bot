import discord
import discord.context_managers
from discord.ext import commands
from discord.utils import get

from dotenv import load_dotenv
import os

load_dotenv()

TOKEN = os.getenv("TOKEN")

intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(intents=intents, description="Bot Music Sam",
                   command_prefix=commands.when_mentioned_or("!d "))


@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Game(name="Usar comandos con el prefijo '!d'."))
    print(f"Conectado a {bot.guilds[0]}")


@bot.command(pass_context=True)
async def ping(ctx):
    await ctx.send("Pong!")


@bot.command(pass_context=True)
async def join(ctx):
    channel = ctx.message.author.voice.channel

    if not channel:
        await ctx.send(f"{ctx.author} no esta conectado a un canal de voz")
        return

    voice = get(bot.voice_clients, guild=ctx.guild)
    if voice and voice.is_connected():
        await voice.move_to(channel)
    else:
        voice = await channel.connect()


@bot.command(pass_context=True)
async def off(ctx):
    channel = ctx.message.author.voice.channel
    voice = get(bot.voice_clients, guild=ctx.guild)
    await voice.disconnect()


bot.run(TOKEN)
