import discord
import discord.context_managers
from discord.ext import commands
from discord.utils import get

from pytube import YouTube
import moviepy.editor as mp

from dotenv import load_dotenv
import os

load_dotenv()

TOKEN = os.getenv("TOKEN")

intents = discord.Intents.default()
intents.message_content = True
intents.voice_states = True

bot = commands.Bot(intents=intents, description="Bot Music",
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


def download_video(url: str) -> str:
    yt = YouTube(url)
    video = yt.streams.filter(progressive=True).order_by(
        "resolution").asc().first()

    try:
        message = video.download(output_path="downloads/")
    except Exception as e:
        print(f"Error: {e}")
    finally:
        return message


def audio_extraction(path: str):
    video_clip = mp.AudioFileClip(path)
    video_clip.write_audiofile("downloads/song.mp3")


def get_song(url: str) -> str:
    path = download_video(url)
    print(f"Video downloaded on '{path}'")
    file_name = os.path.basename(path)
    name = os.path.splitext(file_name)[0]

    audio_extraction(path)
    os.remove(path)

    return name


@bot.command(pass_context=True)
async def play(ctx, url: str):
    songPlaying = os.path.isfile("../downloads/song.mp3")

    try:
        if songPlaying:
            os.remove("../downloads/song.mp3")
            print("Song was removed")
    except PermissionError:
        print("A song is playing")
        await ctx.send("E: A song is playing")
        return

    await ctx.send("Ok!!")

    voice = get(bot.voice_clients, guild=ctx.guild)
    song_name = get_song(url)

    voice.play(discord.FFmpegPCMAudio("downloads/song.mp3"),
               after=lambda e: print("Finish"))
    voice.source = discord.PCMVolumeTransformer(voice.source)
    voice.source.volume = 0.04

    await ctx.send(f"Playing: {song_name}")


@bot.command(pass_context=True)
async def pause(ctx):
    voice = get(bot.voice_clients, guild=ctx.guild)

    if not (voice and voice.is_playing()):
        print("E: Music is not playing")
        await ctx.send("Music is not playing")
        return

    print(f"Music was paused by {ctx.author}")
    voice.pause()
    await ctx.send(f"Music was paused by {ctx.author}")


@bot.command(pass_context=True)
async def resume(ctx):
    voice = get(bot.voice_clients, guild=ctx.guild)

    if not (voice and voice.is_paused()):
        print("E: Music is not paused")
        await ctx.send("Music is not paused")
        return

    print("Music was resume")
    voice.resume()
    await ctx.send("Music was resume")


@bot.command(pass_context=True)
async def skip(ctx):
    voice = get(bot.voice_clients, guild=ctx.guild)

    if not (voice and voice.is_playing()):
        print("E: Music is not playing")
        await ctx.send("Music is not playing")
        return

    print(f"Music was skipped by {ctx.author}")
    voice.stop()
    await ctx.send(f"Music was skipped by {ctx.author}")


bot.run(TOKEN)
