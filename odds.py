import asyncio
import datetime
import random
import discord

active_players = set()

def odds_helper (oddsLength):
    if oddsLength == 2: 
        return 2
    elif 3 <= oddsLength <= 10: 
        return 5
    elif 10 < oddsLength <= 20: 
        return 10
    else: 
        return 15

async def start_odds(bot, msg):
    parts = msg.content.split()
    if len(parts) < 2 or not parts[1].isdigit():
        await msg.channel.send("Please provide a number")
        return
    maxNum = int(parts[1])

    if maxNum < 2:
        await msg.channel.send("Number too low")
        return

    bot_number = random.randint(1, maxNum)
    if msg.author.id in active_players:
        await msg.channel.send(f"{msg.author.mention}, you are already playing!")
        return
    
    active_players.add(msg.author.id)
    await msg.channel.send(f"{msg.author.mention}, N U M B E R ?")

    def check(reply):
        return (reply.author == msg.author 
                and reply.channel == msg.channel 
                and reply.content.strip().isdigit())

    try: 
        reply = await bot.wait_for('message', check=check, timeout=30.0)
    except asyncio.TimeoutError:
        await msg.channel.send(f"T O O L A T E {msg.author.mention}, Y O U L O S E")
        await msg.author.timeout(datetime.timedelta(seconds = 30))
        return
    finally: 
        active_players.discard(msg.author.id)

    guess = int(reply.content)

    if not (1 <= guess <= maxNum):
        await msg.channel.send(f"D U M B A S S")
        return

    if bot_number == guess: 
        timeoutValue = odds_helper(maxNum)
        try:
            await msg.channel.send(f"D A M N {bot_number} = {guess}")
            await msg.author.timeout(datetime.timedelta(minutes=timeoutValue), reason = "B A D A T O D D S")
        except discord.errors.Forbidden:
            pass
    else: 
        await msg.channel.send(f"{msg.author.mention} - S A F E")
        return