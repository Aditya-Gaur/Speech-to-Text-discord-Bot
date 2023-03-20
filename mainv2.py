import discord
from discord.ext import commands
import os
from pydub import AudioSegment

import speech_recognition as sr
# https://discord.com/api/oauth2/authorize?client_id=CLIENTID&permissions=2184184832&scope=bot

bot = commands.Bot(command_prefix=',', intents=discord.Intents.all())
connections = {}

async def once_done(sink: discord.sinks, channel: discord.TextChannel, *args):  # Our voice client already passes these in.
    recorded_users = [  # A list of recorded users
        f"<@{user_id}>"
        for user_id, audio in sink.audio_data.items()
    ]
    
    files = [discord.File(audio.file, f"{user_id}.{sink.encoding}") for user_id, audio in sink.audio_data.items()]  # List down the files.
    
    # Send audio recording in channel
#    await channel.send(f"finished recording audio for: {', '.join(recorded_users)}.", files=files)  # Send a message with the accumulated files.

    for user_id, audio in sink.audio_data.items():
        with open("audio.mp3", "wb") as file:
            file.write(audio.file.getbuffer())

        # Imports mp3 and converts it to wave
        sound = AudioSegment.from_mp3("audio.mp3")
        sound.export("audio.wav", format="wav")
        sound = AudioSegment.from_wav("audio.wav")
        sound = sound.set_channels(1)
        sound.export("audio.wav", format="wav")

        aud = sr.AudioFile('audio.wav')
        with aud as source:
            buff = sr.Recognizer().record(source)
        try:
            await channel.send(f"{user_id} said: {sr.Recognizer().recognize_google(buff)}")
        except sr.UnknownValueError:
            await channel.send("Could not understand audio")
        except sr.RequestError as e:
            await channel.send("Could not request results from Google Speech Recognition service; {0}".format(e))

        os.remove("audio.mp3")
        os.remove("audio.wav")

@bot.command()
async def start(ctx: discord.ApplicationContext):  # If you're using commands.Bot, this will also work.
    voice = ctx.author.voice

    if not voice:
        await ctx.channel.send("You aren't in a voice channel!")

    vc = await voice.channel.connect()  # Connect to the voice channel the author is in.


@bot.command()
async def stop(ctx: discord.ApplicationContext):
    flag = True
    for vc in bot.voice_clients:
        if ctx.guild.id == vc.guild.id:
            await vc.disconnect()
            flag = False
    if flag:
        await ctx.channel.send("I am currently not recording here.")  # Respond with this if we aren't recording.

@bot.event
async def on_voice_state_update(member, before, after):
    if after.self_mute and not before.self_mute: # Unmute > Mute
        for vc in bot.voice_clients:
            if member.voice.channel == vc.channel:
                vc.stop_recording()
    elif before.self_mute and not after.self_mute: # Mute > Unmute
        for vc in bot.voice_clients:
            if member.voice.channel == vc.channel:
                vc.start_recording(
                discord.sinks.MP3Sink(),  # The sink type to use.
                once_done,  # What to do once done.
                vc.channel  # The channel to disconnect from.
            )
                await vc.channel.send("Started!")



bot.run("Token")
