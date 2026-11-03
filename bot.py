import discord
import os
import helper
from keep_alive import keep_alive
from dotenv import load_dotenv
import pandas as pd
import random
import odds
load_dotenv()

# Initalize bot
intents = discord.Intents.all() # discord.Intents.all()
intents.messages = True
bot = discord.Client(intents = intents)


# Bot Login Confirmation
@bot.event
async def on_ready():
    print(f'Logged in as {bot.user}')


# Message Handling
@bot.event
async def on_message(msg):
    
    # TODO: check for the thursday thugginmessage not sent
    df=pd.read_csv("messagecount.csv")
    user=str(msg.author)
    if df.empty:
        df=pd.DataFrame({'User':[user],'MessageCount':[1.0]})
    elif user in df["User"].values:
       df.loc[df["User"]==user,'MessageCount']+=1
    else:
        temp=pd.DataFrame({'User':[user],'MessageCount':[1.0]})
        if not temp.isnull().all().all():
            df = pd.concat([df, temp], ignore_index=True)
    # Ignore Bot messages 
    df.to_csv('messagecount.csv',index=False)
    if msg.author == bot.user:
        return
    
    # Process main chat
    elif msg.channel.name in ('all-club-chat', 'bot-testing') :
        if msg.content.lower().startswith('!odds'):
            await odds.start_odds(bot, msg)
        elif msg.author.id in odds.active_players:
            return
        else: 
            await helper.process_msg(msg,token)
    elif msg.channel.name in ('workouts-and-fitness', 'grinch-workout-and-fitness','geh-workout-and-conditioning'):
        await helper.process_workout(msg,token)
    elif msg.channel.name in ('grinch-team-chat'):
        temp=random.randint(1,199)
        if temp==52:
            await msg.channel.send('https://imgur.com/oWX9OtO')
        


# Keep Bot alive by pinging flask server 
# keep_alive()

# Run bot
#bot.run(os.getenv('BOT_TOKEN'))
token = os.getenv('BOT_TOKEN')
#print(token)
bot.run(token)

