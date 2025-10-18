import discord
from discord.ext import commands
import yt_dlp
import asyncio

FFMPEG_OPTIONS = {
    'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5',
    'options': '-vn'
}

YDL_OPTIONS = {'format': 'bestaudio/best', 'noplaylist': 'True', 'quiet': True, 'no_warnings': True}

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.voice_states = True

bot = commands.Bot(command_prefix="!", intents=intents)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")
    print("Bot is ready and connected to Discord.")

@bot.command()
async def play(ctx, *, search: str):
    if ctx.author.voice is None:
        await ctx.send("You need to join a voice channel first!")
        return

    voice_channel = ctx.author.voice.channel
    if ctx.voice_client is None:
        await voice_channel.connect()
    else:
        await ctx.voice_client.move_to(voice_channel)

    if ctx.voice_client.is_playing() or ctx.voice_client.is_paused():
        await ctx.send("I'm already playing or paused! 🎵")
        return

    await ctx.send(f"Preparing **{search}**... ⌛")
    
    entry = None 
    loop = asyncio.get_event_loop()

    with yt_dlp.YoutubeDL(YDL_OPTIONS) as ydl:
        try:
            if search.startswith("http://") or search.startswith("https://"):
                info_result = await loop.run_in_executor(None, lambda: ydl.extract_info(search, download=False))
                entry = info_result
            else:
                info_result = await loop.run_in_executor(None, lambda: ydl.extract_info(f"ytsearch:{search}", download=False))
                
                if 'entries' in info_result and len(info_result['entries']) > 0:
                    entry = info_result['entries'][0]
                else:
                    await ctx.send("No results found. Please try another keyword or link. 😔")
                    return

        except yt_dlp.utils.DownloadError as e:
            await ctx.send(f"There was an issue with the link: {e}")
            return
        except Exception as e:
            await ctx.send(f"An error occurred while trying to play the music: `{e}`")
            return
    
    if entry is None:
        await ctx.send("Could not retrieve song information. Please try again.")
        return
        
    url = entry['url']
    title = entry['title']
    
    ctx.voice_client.play(discord.FFmpegOpusAudio(url, **FFMPEG_OPTIONS))
    await ctx.send(f"🎶 Now playing: **{title}**")

@bot.command()
async def leave(ctx):
    if ctx.voice_client is not None:
        await ctx.voice_client.disconnect()
        await ctx.send("Goodbye! 👋")
    else:
        await ctx.send("I'm not connected to a voice channel.")

@bot.command()
async def stop(ctx):
    if ctx.voice_client and ctx.voice_client.is_playing():
        ctx.voice_client.stop()
        await ctx.send("Playback stopped. ⏹️")
    else:
        await ctx.send("There's no music playing to stop.")

@bot.command()
async def pause(ctx):
    if ctx.voice_client and ctx.voice_client.is_playing():
        ctx.voice_client.pause()
        await ctx.send("Playback paused. ⏸️")
    else:
        await ctx.send("There's no music playing to pause.")

@bot.command()
async def resume(ctx):
    if ctx.voice_client and ctx.voice_client.is_paused():
        ctx.voice_client.resume()
        await ctx.send("Resuming playback. ▶️")
    else:
        await ctx.send("There's no paused music to resume.")

bot.run("BOT_TOKEN")
