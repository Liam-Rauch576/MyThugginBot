import responses
import dbmanager
import thugginbot
import json
import datetime
import random
import csv
import pandas as pd
from collections import OrderedDict
import numpy as np
from csv import writer
import discord
import aiohttp


df=pd.read_csv("TimesUsed.csv")

devid=["superice0","darkdare0926","nokken29","brokenthunder", "limeranch"]



with open("words.json","r") as f:
    CurentWords=json.load(f)
with open("paramaters.json","r") as t:
    ThugginComplete=json.load(t)
    #print(ThugginComplete)

async def UpdateCurrentWords():
    CurentWords=json.load(f)
async def updateThugg():
    ThugginComplete=json.load(t)
async def process_msg(msg,token):
    #print(datetime.datetime.today().weekday())
    #print(ThugginComplete['thugginComplete'])
    # Get message text
    with open("words.json","r") as f:
        CurentWords=json.load(f)
    with open("paramaters.json","r") as t:
        ThugginComplete=json.load(t)
    if datetime.datetime.today().weekday()!=3 and ThugginComplete["thugginComplete"]:
        with open("paramaters.json","w") as q:
            #thugging={"thugginComplete": False,"thugginInProgress": False,"drinkWaterOdds":ThugginComplete["drinkWaterOdds"]}
            ThugginComplete['thugginComplete']=False
            json.dump(ThugginComplete,q)
    if datetime.datetime.today().weekday() == 6 and ThugginComplete['pickup'] and not ThugginComplete['pickupsent']:
        channelID = '1148302956559618098'
        HEADERS = {
            "Authorization": f"Bot {token}",
            "Content-Type": "application/json"
        }

        url = f"https://discord.com/api/v10/channels/{channelID}/messages"

        payload = {
            #"content": "📅 What day are you free this week?",
            "poll": {
                "question": {"text": "📅 What days are you free for pickup this week?"},
                "answers": [
                    {"poll_media": {"text": "Monday"}},
                    {"poll_media": {"text": "Tuesday"}},
                    {"poll_media": {"text": "Wednesday"}},
                    {"poll_media": {"text": "Thursday"}},
                    {"poll_media": {"text": "Friday"}},
                    {"poll_media": {"text": "Saturday"}},
                    {"poll_media": {"text": "Sunday"}}
                ],
                "allow_multiselect": True,
                "duration": 48  # in Hours 
            }
        }

        async with aiohttp.ClientSession() as session:
            async with session.post(url, headers=HEADERS, json=payload) as resp:
                print("Status:", resp.status)
                print("Response:", await resp.text())
        with open("paramaters.json","w") as q:
        #thugging={"thugginComplete": False,"thugginInProgress": False,"drinkWaterOdds":ThugginComplete["drinkWaterOdds"]}
            ThugginComplete['pickupsent']=True
            json.dump(ThugginComplete,q)
    if datetime.datetime.today().weekday() != 6:
        with open("paramaters.json","w") as q:
        #thugging={"thugginComplete": False,"thugginInProgress": False,"drinkWaterOdds":ThugginComplete["drinkWaterOdds"]}
            ThugginComplete['pickupsent']=False
            json.dump(ThugginComplete,q)

    water=random.randint(0,ThugginComplete["drinkWaterOdds"])
    if(water==13):
        #print(paramaters.ThugginComplete)
        #print(datetime.date.today().weekday())
        if  datetime.datetime.today().weekday()==3:
            #print('hi')
            #print(ThugginComplete)
            if ThugginComplete['thugginComplete']:
                #print(paramaters.ThugginComplete)
                await msg.channel.send('D R I N K  W A T E R')
        else:
            #print('why')
            await msg.channel.send('D R I N K  W A T E R')
    trueMsg=msg.content
    text = msg.content.lower()
    
    
    length=len(text)
    
    if text.startswith("!upload") and str(msg.author) in devid:
        temp=trueMsg.split()
        word=''
        link=''
        hold=temp[1]
        hold2=temp[2]

        if "http" in hold:
            link=hold
            word=hold2.lower()
        else:
            word=hold.lower()
            link=hold2

        if word in CurentWords.keys():
            temp=CurentWords[word]
            if isinstance(temp,list):
                temp.append(link)

                
            else:
                newList=[]
                newList.append(temp)
                newList.append(link)
                CurentWords[word]=newList
                

        else:
            CurentWords[word]=link
            NewRow=[word,0.0]
            with open('TimesUsed.csv','a') as U:
                WrittenObject=writer(U)
                WrittenObject.writerow(NewRow)
                U.close
        with open("words.json","w") as q:
            json.dump(CurentWords,q)
    elif text.startswith("!removeall") and str(msg.author) in devid:
        df=pd.read_csv("TimesUsed.csv")
        temp=text.split()
        toRemove=temp[1]
        check=CurentWords.pop(toRemove, None)
        if check is not None:
            df = df[df['Word'] != toRemove]
            df.to_csv("TimesUsed.csv", index=False)
            with open("words.json","w") as q:
                json.dump(CurentWords,q)
    elif text.startswith("!removespecific") and str(msg.author) in devid:
        temp=text.split(' ')
        toRemove=temp[1]
        index=int(temp[2])
        allWords={}
        with open("words.json","r") as f:
            allWords=json.load(f)
        hold=allWords[toRemove]
        if index >= len(hold):
            await msg.channel.send(f"{index} is too big, you're a programmer we start at 0 here :)")
        else:
            temp=hold.pop(index)
            with open("words.json","w") as q:
                    CurentWords=allWords
                    json.dump(allWords,q)
    elif text.startswith('!len') and str(msg.author) in devid:
        with open("words.json","r") as f:
            CurentWords=json.load(f)
        hold=text.split(' ',1)
        thugginWord=hold[1]
        try:
            img=CurentWords[thugginWord]
            if(type(img) is list):
                howMany=len(img)
            else:
                howMany=1
            
            if howMany==1:
                await msg.channel.send(f"{thugginWord} only has {howMany} photo")
            else:
                await msg.channel.send(f"{thugginWord} has {howMany} pictures associated with it")
                #print(img)
        except KeyError:
            await msg.channel.send(f"{thugginWord} isnt a word. Check your spelling Ethan")
            
        
    elif text.startswith('!specific') and str(msg.author) in devid:
        with open("words.json","r") as f:
            CurentWords=json.load(f)
        hold=text.split(' ',2)
        thugginWord=hold[1]
        num=int(hold[2])
        try:
            img=CurentWords[thugginWord]
            if(type(img) is list):
                howMany=len(img)
                picture=img[num]
                await msg.channel.send(picture)
                BotWord=''
                for letter in thugginWord:
                    
                    BotWord=BotWord+letter
                    
                await msg.channel.send(BotWord+' '+str(num))
            else:
                await msg.channel.send(img)
                BotWord=''
                for letter in thugginWord:

                    BotWord=BotWord+letter
                await msg.channel.send(BotWord)
                
        except KeyError:
            await msg.channel.send(f"{thugginWord} isnt a word. Check your spelling Ethan")

    elif text.startswith("!devhelp") and str(msg.author) in devid:
        message = "**--- __DevCommands:__ ---**\n**!upload+word+link: Uploads new command/photo**\n**!removeall+word: removes all photos with word**\n**!removespecific+word+num: remove a specific photo from a command**\n**!len+word: shows how many photos are associated with the word**\n**!specific+word+num: specific photo from word**\n**!changewater + num (>=13): changes the odds of drink water appearing**\n**!sendmsg +msg: sends a message as thugging bot to all-club-chat**\n**!enablepickup: enables the pickup poll to send every sunday**\n**!disablepickup: disables pickup poll from sending every sunday**"
        await msg.channel.send(message)
    elif text.startswith("!changewater") and str(msg.author) in devid:
        water=text.split(' ')
        water=int(water[1])
        if water >=13:
            with open("paramaters.json","r") as t:
                ThugginComplete=json.load(t)
            with open("paramaters.json","w") as q:
                #paramaters={"thugginComplete": ThugginComplete['thugginComplete'],"thugginInProgress": ThugginComplete['thugginInProgress'],"drinkWaterOdds":water}
                ThugginComplete['drinkWaterOdds']=water
                json.dump(ThugginComplete,q)
    elif text.startswith("!sendmsg ") and str(msg.author) in devid:
        message=trueMsg.split(' ',1)
        message=message[1]
        msg.channel = discord.utils.get(msg.guild.channels, name='all-club-chat')
        await(msg.channel.send(message))

    elif text.startswith('!enablepickup') and str(msg.author) in devid:
        with open("paramaters.json","r") as t:
                ThugginComplete=json.load(t)
        with open("paramaters.json","w") as q:
            #paramaters={"thugginComplete": ThugginComplete['thugginComplete'],"thugginInProgress": ThugginComplete['thugginInProgress'],"drinkWaterOdds":water}
            ThugginComplete['pickup']=True
            json.dump(ThugginComplete,q)
    elif text.startswith('!disablepickup') and str(msg.author) in devid:
        with open("paramaters.json","r") as t:
                ThugginComplete=json.load(t)
        with open("paramaters.json","w") as q:
            #paramaters={"thugginComplete": ThugginComplete['thugginComplete'],"thugginInProgress": ThugginComplete['thugginInProgress'],"drinkWaterOdds":water}
            ThugginComplete['pickup']=False
            json.dump(ThugginComplete,q)

    # --== ThugginBot Commands ==--
   
    elif datetime.datetime.today().weekday()==3 and ThugginComplete["thugginInProgress"] and len(text)>1 and not ThugginComplete["thugginComplete"]:
        
        author=msg.author
        newPerson={'DiscordID':author}
        tdf4=pd.DataFrame(newPerson,index=[0]) 
        tdf4.to_csv("timeOut.csv", mode='a', index=False,header=False)
        
        await msg.channel.send(f"{author.mention} This isnt very thuggin of you")
        duration = datetime.timedelta(hours=1)
        try:
            await author.timeout(duration, reason="not Thuggin")
        except discord.errors.Forbidden as e:
                    mods=1
    elif text[0]=='!' and   text[1:length] in CurentWords.keys():
        df=pd.read_csv("TimesUsed.csv")
        text=text[1:length]
        Img=CurentWords[text]
        #await thugginbot.checkThugginBotCommand(msg)
        if(type(Img) is list):
            hi=random.randint(0,len(Img)-1)
            Img=Img[hi]
            
        await msg.channel.send(Img)
        BotWord=''
        for letter in text:
            UpLetter=letter.upper()
            BotWord=BotWord+UpLetter
            BotWord=BotWord+' '
        await msg.channel.send(BotWord)
        Tempmsg=msg.content.lower()[1:len(msg.content)]
        mask = df['Word'] == Tempmsg
        result = df[df['Word'] == Tempmsg]
        temp=result['TimesUsed'].values[0]
        print(temp)
        print(Tempmsg)
        temp=temp+1
        df.loc[mask, 'TimesUsed'] = temp
        df.to_csv("TimesUsed.csv", index=False)

        #await thugginbot.checkThugginBotCommand(msg)
        


    #Command to send Gifs
    #elif text[0]=='!' and   text[1:length] in CurrentGifs.keys():
    #    text=text[1:length]
    #    await msg.channel.send(CurrentGifs.get(text))
    #elif text[0]=='!' and   text[1:length] in CurrentGifs.keys():
    #    text=text[1:length]
    #    await msg.channel.send(CurrentGifs.get(text))
    # --== ThugginThursday Command ==--
    elif len(text) == 1 and datetime.date.today().weekday()==3:
       await thugginbot.handle_thugginbot_message(msg)
    
    
    # --== General Commands ==--
    elif text.startswith('!random'):
        df=pd.read_csv("TimesUsed.csv")
        Keys=list(CurentWords.keys())
        RandomWord=random.randint(0,len(Keys)-1)
        Word=Keys[RandomWord]
        #print(Word)
        
        Img=Word
        Bannedwords=['patg','hbd']
        if(Img in Bannedwords):
            while Img in Bannedwords:
                RandomWord=random.randint(0,len(Keys)-1)
                Word=Keys[RandomWord]
                Img=Word
        #Img=CurentWords["mikeshoremonday"]
        sent=CurentWords[Img]
        if(type(sent) is list):
            hi=random.randint(0,len(sent)-1)
            sent=sent[hi]
        await msg.channel.send(sent)
        BotWord=''
        for letter in Word:
            BotWord=BotWord+letter.upper()
            BotWord=BotWord+' '
        await msg.channel.send(BotWord)
        Word = Word.lower()
        result = df[df['Word'] == Word]

        if not result.empty:
            # Word already exists → increment TimesUsed
            temp = result['TimesUsed'].values[0]
            df.loc[df['Word'] == Word, 'TimesUsed'] = temp + 1
        else:
            # Word doesn’t exist → add with TimesUsed = 1
            temp = 1
            new_row = {'Word': Word, 'TimesUsed': temp}
            df = df._append(new_row, ignore_index=True)  # .append() if pandas < 2.0

        # Save back to CSV
        
        df.to_csv("TimesUsed.csv", index=False)
        #print("random added to timesUsed",Word)

    elif text.startswith('!all '):
        attempt=text.split(' ')
        word=attempt[1]
        if word in CurentWords.keys():
            all=CurentWords[word]
            for pic in all:
                await msg.channel.send(pic)
            BotWord=''
            for letter in word:
                BotWord=BotWord+letter.upper()
                BotWord=BotWord+' '
            await msg.channel.send(BotWord + 'X '+str(len(all)))

            df=pd.read_csv("TimesUsed.csv")
            mask = df['Word'] == word
            result = df[df['Word'] == word]

            if not result.empty:
                temp = result['TimesUsed'].values[0]
                temp = temp + 1
                df.loc[mask, 'TimesUsed'] = temp
            else:
                temp = 1
                new_row = {'Word': word, 'TimesUsed': temp}
                df = df._append(new_row, ignore_index=True)  # or .append if pandas < 2.0

            df.to_csv("TimesUsed.csv", index=False)
            
    elif text.startswith('!wordlist'):
        dm='Current Words: '
        keylist=list(CurentWords.keys())
        keylist.sort()
        #print(keylist)
        for key in keylist:
            temp=CurentWords[key]
            if isinstance(temp,list):
                howMany=len(temp)
            else:
                howMany=1
            keyhold=str(key).capitalize()
            dm=dm+keyhold+f' [{howMany}], '
        length=len(dm) 
        dm=dm[0:length-2]
        user=msg.author
        await msg.delete()
        await user.send(dm)   
    elif text.startswith('!help'):
        await responses.post_help_command(msg)

        print('POST - HelpCommand')
    elif(text.startswith('!mostused')):

        #data=pd.read_csv("TimesUsed.csv")
        #dataDict=data.to_dict(orient='records')
        #print(dataDict)
        TimesUsedDict={}
        with open('TimesUsed.csv', 'r', newline='') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            #csv_reader=next(csv_reader)
            for row in csv_reader:
                Word=row['Word']
                TimesUsed=float(row['TimesUsed'])
                TimesUsedDict[Word]=TimesUsed
        #print(TimesUsedDict)
            
        keys = list(TimesUsedDict.keys())
        values = list(TimesUsedDict.values())
        sorted_value_index = np.argsort(values)
        sorted_dict = {keys[i]: values[i] for i in sorted_value_index}
        sorted_dict=dict(reversed(list(sorted_dict.items())))

        ListOfWords=list(sorted_dict)
        message='**1:** ' + str(ListOfWords[0]).upper() + ' at ' + str(int(sorted_dict[ListOfWords[0]])) + '\n**2:** ' + str(ListOfWords[1]).upper() + ' at ' + str(int(sorted_dict[ListOfWords[1]])) +'\n**3:** ' + str(ListOfWords[2]).upper() + ' at ' + str(int(sorted_dict[ListOfWords[2]])) +'\n**4:** ' + str(ListOfWords[3]).upper() + ' at ' + str(int(sorted_dict[ListOfWords[3]])) +'\n**5:** ' + str(ListOfWords[4]).upper() + ' at ' + str(int(sorted_dict[ListOfWords[4]]))
        await msg.channel.send(message)
    elif(text.startswith('!mostused')):

        #data=pd.read_csv("TimesUsed.csv")
        #dataDict=data.to_dict(orient='records')
        #print(dataDict)
        TimesUsedDict={}
        with open('TimesUsed.csv', 'r', newline='') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            #csv_reader=next(csv_reader)
            for row in csv_reader:
                Word=row['Word']
                TimesUsed=float(row['TimesUsed'])
                TimesUsedDict[Word]=TimesUsed
        #print(TimesUsedDict)
            
        keys = list(TimesUsedDict.keys())
        values = list(TimesUsedDict.values())
        sorted_value_index = np.argsort(values)
        sorted_dict = {keys[i]: values[i] for i in sorted_value_index}
        sorted_dict=dict(reversed(list(sorted_dict.items())))

        ListOfWords=list(sorted_dict)
        message='**1:** ' + str(ListOfWords[0]).upper() + ' at ' + str(int(sorted_dict[ListOfWords[0]])) + '\n**2:** ' + str(ListOfWords[1]).upper() + ' at ' + str(int(sorted_dict[ListOfWords[1]])) +'\n**3:** ' + str(ListOfWords[2]).upper() + ' at ' + str(int(sorted_dict[ListOfWords[2]])) +'\n**4:** ' + str(ListOfWords[3]).upper() + ' at ' + str(int(sorted_dict[ListOfWords[3]])) +'\n**5:** ' + str(ListOfWords[4]).upper() + ' at ' + str(int(sorted_dict[ListOfWords[4]]))
        await msg.channel.send(message)
    elif text.startswith('!haze '):
        if not msg.mentions:
            pass
        else:
            await responses.post_haze_command(msg)

        print('POST - Haze')

    elif text.startswith('!love '):
        if not msg.mentions:
            pass
        else:
            await responses.post_love_command(msg)

        print('POST - Haze')

    elif text.startswith('!tomatoes '):
        if msg.author.id == msg.mentions[0].id:
            await msg.channel.send("*STOOPID, I'M NOT GONNA LET YOU GET THE CHANCE*")
        else:
            await responses.post_tomatos_command(msg)

        print('POST - TomatoesCommand')
    
    elif text.startswith('!sawthat'):
        await responses.post_sawthat(msg)

        print('POST - SawThat') 


    # --== Like/Dislike Commands ==--
    elif text.startswith('!like '):

        target_user = msg.mentions[0]
        print (target_user)
        df2=pd.read_csv("Clout.csv")
        listOfNames= df2['Name'].values #makes a list of all names in the csv file 
        if msg.author.id == msg.mentions[0].id:
            await msg.channel.send('*STOOPID, I\'M NOT GONNA LET YOU GET THE CHANCE*')
        elif not msg.mentions:
            return
        elif bool(msg.mentions[0].bot):
            await msg.channel.send("**UHH... DON\'T CARE!!!** 😡")
        else:
            if(str(target_user) in listOfNames):
                mask = df2['Name'] == str(target_user)
                result = df2[df2['Name'] == str(target_user)] #gets the row with the target user
                Likes=result['Likes'].values[0]
                Clout=result['Clout'].values[0] #gets the vlues
                Likes=Likes+1
                Clout=Clout+1
                df2.loc[mask,'Likes']=Likes
                df2.loc[mask,'Clout']=Clout #finds locaton of values and updates them
                df2.to_csv("Clout.csv", index=False) #updates csv file
            else:
                newName={'Name': str(target_user),'Likes':1,'Dislikes':0,'Clout':1}
                tdf=pd.DataFrame(newName,index=[0]) 
                tdf.to_csv("Clout.csv", mode='a', index=False,header=False) #puts new Name in csv file

        print('ADD - Like')

    elif text.startswith('!dislike '):
        target_user = msg.mentions[0]
        df2=pd.read_csv("Clout.csv")
        listOfNames= df2['Name'].values #makes a list of all names in the csv file 
        if msg.author.id == msg.mentions[0].id:
            await msg.channel.send('*STOOPID, I\'M NOT GONNA LET YOU GET THE CHANCE*')
        elif not msg.mentions:
            return
        elif bool(msg.mentions[0].bot):
            await msg.channel.send('**LEAVE US ALONE!!!** 😡')
            return
        else:
            # Get first mention in list
            if(str(target_user) in listOfNames):
                mask = df2['Name'] == str(target_user)
                result = df2[df2['Name'] == str(target_user)] #gets the row with the target user
                Dislikes=result['Dislikes'].values[0]
                Clout=result['Clout'].values[0] #gets the vlues
                Dislikes=Dislikes+1
                Clout=Clout-1
                df2.loc[mask,'Dislikes']=Dislikes
                df2.loc[mask,'Clout']=Clout #finds locaton of values and updates them
                df2.to_csv("Clout.csv", index=False) #updates csv file
            else:
                newName={'Name': str(target_user),'Likes':0,'Dislikes':1,'Clout':-1}
                tdf=pd.DataFrame(newName,index=[0]) 
                tdf.to_csv("Clout.csv", mode='a', index=False,header=False) #puts new Name in csv file

        print('ADD - Dislike')

    elif text.startswith('!likeleaderboard'):
        #await responses.post_like_leaderboard(msg)
        TotalLikes={}
        with open('Clout.csv', 'r', newline='') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            #csv_reader=next(csv_reader)
            for row in csv_reader:
                #print(row)
                
                Name=row['Name']
                if Name.endswith('#0'):
                    Name=Name[:-2]
                Likes=float(row['Likes'])
                TotalLikes[Name]=Likes
                #print(TotalLikes)
                #print(temp)
                
        for member in msg.guild.members:
            if(str(member) in TotalLikes.keys()):
                if(member.nick !=None):
                    TotalLikes[str(member.nick)]=TotalLikes[str(member)]
                    del TotalLikes[str(member)]
                elif(member.global_name!=None):
                    TotalLikes[str(member.global_name)]=TotalLikes[str(member)]
                    del TotalLikes[str(member)]
 
        keys = list(TotalLikes.keys())
        values = list(TotalLikes.values())
        sorted_value_index = np.argsort(values)
        sorted_dict = {keys[i]: values[i] for i in sorted_value_index}
        sorted_dict=dict(reversed(list(sorted_dict.items())))
        #print(sorted_dict)
        ListOfLikes=list(sorted_dict)
        LikeLeader='-__**Like Leaderboard**__-\n'
        for x in range(0,10):
            if(x>=len(ListOfLikes)):
                break
            else:
                person=ListOfLikes[x]
                if(sorted_dict[person]==0):
                    break
                
                LikeLeader=LikeLeader+(str(x+1)+': '+person+" with "+ str(sorted_dict[person])+'\n')
        #print(ListOfLikes)
        print('POST - Like_leaderboard')
        await msg.channel.send(LikeLeader)

    elif text.startswith('!dislikeleaderboard'):
        TotalDislikes={}
        with open('Clout.csv', 'r', newline='') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            #csv_reader=next(csv_reader)
            for row in csv_reader:
                Name=row['Name']
                if Name.endswith('#0'):
                    Name=Name[:-2]
                Dislikes=float(row['Dislikes'])

                TotalDislikes[Name]=Dislikes
        print(TotalDislikes)
        for member in msg.guild.members:
            if(str(member) in TotalDislikes.keys()):
                if(member.nick !=None):
                    TotalDislikes[str(member.nick)]=TotalDislikes[str(member)]
                    del TotalDislikes[str(member)]
                elif(member.global_name!=None):
                    TotalDislikes[str(member.global_name)]=TotalDislikes[str(member)]
                    del TotalDislikes[str(member)]     
        keys = list(TotalDislikes.keys())
        values = list(TotalDislikes.values())
        sorted_value_index = np.argsort(values)
        sorted_dict = {keys[i]: values[i] for i in sorted_value_index}
        sorted_dict=dict(reversed(list(sorted_dict.items())))
        #print(sorted_dict)
        ListOfDislikes=list(sorted_dict)
        DislikeLeader='-__**Dislike Leaderboard**__-\n'
        for x in range(0,10):
            if(x>=len(ListOfDislikes)):
                break
            else:
                person=ListOfDislikes[x]
                print(person)
                if(sorted_dict[person]==0):
                    break
                DislikeLeader=DislikeLeader+(str(x+1)+': '+person+" with "+ str(sorted_dict[person])+'\n')
        #print(ListOfLikes)
        await msg.channel.send(DislikeLeader)
        print('POST - Disike_leaderboard')

    elif text.startswith('!cloutleaderboard'):
        TotalClout={}
        with open('Clout.csv', 'r', newline='') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            #csv_reader=next(csv_reader)
            for row in csv_reader:
                Name=row['Name']
                if Name.endswith('#0'):
                    Name=Name[:-2]
                Clout=float(row['Clout'])
                
                TotalClout[Name]=Clout
        print(TotalClout)
        for member in msg.guild.members:
            if(str(member) in TotalClout.keys()):
                if(member.nick !=None):
                    TotalClout[str(member.nick)]=TotalClout[str(member)]
                    del TotalClout[str(member)]
                elif(member.global_name!=None):
                    TotalClout[str(member.global_name)]=TotalClout[str(member)]
                    del TotalClout[str(member)]  
        keys = list(TotalClout.keys())
        values = list(TotalClout.values())
        sorted_value_index = np.argsort(values)
        sorted_dict = {keys[i]: values[i] for i in sorted_value_index}
        sorted_dict=dict(reversed(list(sorted_dict.items())))
        #print(sorted_dict)
        ListOfClout=list(sorted_dict)
        CloutLeader='-__**Clout Leaderboard**__-\n'
        for x in range(0,10):
            if(x>=len(ListOfClout)):
                break
            else:
                person=ListOfClout[x]
                CloutLeader=CloutLeader+(str(x+1)+': '+person+" with "+ str(sorted_dict[person])+'\n')
        #print(ListOfLikes)
        await msg.channel.send(CloutLeader)

        print('POST - Clout_leaderboard')




    # --== Sniped Commands ==--
    elif text.startswith('!sniped '):
        #print(msg.attachments)
        author=msg.author
        print(author)
        df3=pd.read_csv('snipe.csv')
        listOfNames= df3['Name'].values
        if msg.author == msg.mentions[0]:
            await msg.channel.send('Friendly Fire Warning')
            return
        elif bool(msg.mentions[0].bot):
            await msg.channel.send('**LEAVE US ALONE!!!** 😡')
            return
        elif not msg.mentions:
            await msg.channel.send("*STOoOoPID, DIDN\'T TAG \'EM*")
        #elif len(msg.attachments)==0:
        #    await msg.channel.send('**You Gotta Actually Fire the Shot!!**') Removed bc remixes are a thing
        else:
            if(str(author) not in listOfNames):
                newPerson={'Name': str(author),'Kills':0,'Deaths':0,'KDA':0}
                tdf=pd.DataFrame(newPerson,index=[0]) 
                tdf.to_csv("snipe.csv", mode='a', index=False,header=False)
                df3=pd.read_csv('snipe.csv')
            for target_user in msg.mentions:
                #print(target_user)
                mask = df3['Name'] == str(author)
                result = df3[df3['Name'] == str(author)] #gets the row with the target user
                Kills=result['Kills'].values[0] #gets the values
                Kills=Kills+1
                tDeaths=result['Deaths'].values[0]
                if(tDeaths==0):
                    tDeaths=1
                df3.loc[mask,'Kills']=Kills
                df3.loc[mask,'KDA']=float(Kills/tDeaths)
                df3.to_csv("snipe.csv", index=False)
                df3=pd.read_csv('snipe.csv')

                if(str(target_user) not in listOfNames):
                    print(target_user)
                    newPerson={'Name': str(target_user),'Kills':0,'Deaths':1,'KDA':0}
                    tdf=pd.DataFrame(newPerson,index=[0]) 
                    print(tdf)
                    tdf.to_csv('snipe.csv', mode='a', index=False,header=False)
                    df3=pd.read_csv('snipe.csv')
                else:
                    mask = df3['Name'] == str(target_user)
                    result = df3[df3['Name'] == str(target_user)] #gets the row with the target user
                    Deaths=result['Deaths'].values[0] #gets the values
                    Deaths=Deaths+1
                    tKills=result['Kills'].values[0]
                    df3.loc[mask,'Deaths']=Deaths
                    df3.loc[mask,'KDA']=float(tKills/Deaths)
                    df3.to_csv("snipe.csv", index=False) #updates csv file
                    df3=pd.read_csv('snipe.csv')       
            df3.to_csv("snipe.csv", index=False)

        print('ADD - Sniped')

    elif text.startswith('!killsleaderboard'):
        TotalKills={}
        with open('snipe.csv', 'r', newline='') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            #csv_reader=next(csv_reader)
            for row in csv_reader:
                Name=row['Name']
                if Name.endswith('#0'):
                    Name=Name[:-2]
                Kills=float(row['Kills'])


                TotalKills[Name]=Kills

        for member in msg.guild.members:
            if(str(member) in TotalKills.keys()):
                if(member.nick !=None):
                    TotalKills[str(member.nick)]=TotalKills[str(member)]
                    del TotalKills[str(member)]
                elif(member.global_name!=None):
                    TotalKills[str(member.global_name)]=TotalKills[str(member)]
                    del TotalKills[str(member)]   
        keys = list(TotalKills.keys())
        values = list(TotalKills.values())
        sorted_value_index = np.argsort(values)
        sorted_dict = {keys[i]: values[i] for i in sorted_value_index}
        sorted_dict=dict(reversed(list(sorted_dict.items())))
        #print(sorted_dict)
        ListOfKills=list(sorted_dict)
        KillLeader='-__**Kills Leaderboard**__-\n'
        for x in range(0,10):
            if(x>=len(ListOfKills)):
                break
            else:
                person=ListOfKills[x]
                if(sorted_dict[person]==0):
                    break
                KillLeader=KillLeader+(str(x+1)+': '+person+" with "+ str(sorted_dict[person])+'\n')
        #print(ListOfLikes)
        await msg.channel.send(KillLeader)


        print('POST - Kills_leaderboard')
    
    elif text.startswith('!snipedleaderboard'):
        TotalDeaths={}
        with open('snipe.csv', 'r', newline='') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            #csv_reader=next(csv_reader)
            for row in csv_reader:
                Name=row['Name']
                if Name.endswith('#0'):
                    Name=Name[:-2]
                Deaths=float(row['Deaths'])

                TotalDeaths[Name]=Deaths

        for member in msg.guild.members:
            #print(member.global_name)
            #print(member)
            #print(TotalDeaths.keys())
            #print(str(member) in TotalDeaths.keys())
            if(str(member) in TotalDeaths.keys()):
                if(member.nick !=None):
                    TotalDeaths[str(member.nick)]=TotalDeaths[str(member)]
                    del TotalDeaths[str(member)]
                elif(member.global_name!=None):
                    TotalDeaths[str(member.global_name)]=TotalDeaths[str(member)]
                    del TotalDeaths[str(member)]
        print(TotalDeaths)
        keys = list(TotalDeaths.keys())
        values = list(TotalDeaths.values())
        sorted_value_index = np.argsort(values)
        sorted_dict = {keys[i]: values[i] for i in sorted_value_index}
        sorted_dict=dict(reversed(list(sorted_dict.items())))
        #print(sorted_dict)
        ListOfDeaths=list(sorted_dict)
        SnipedLeader='-__**Sniped Leaderboard**__-\n'
        for x in range(0,10):
            if(x>=len(ListOfDeaths)):
                break
            else:
                person=ListOfDeaths[x]
                if(sorted_dict[person]==0):
                    break
                SnipedLeader=SnipedLeader+(str(x+1)+': '+person+" with "+ str(sorted_dict[person])+'\n')
        #print(ListOfLikes)
        await msg.channel.send(SnipedLeader)


        print('POST - Sniped_leaderboard')

    
    elif text.startswith('!kdaleaderboard'): #posts KDA leaderbaord
        TotalKDA={}
        with open('snipe.csv', 'r', newline='') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            #csv_reader=next(csv_reader)
            for row in csv_reader:
                Name=row['Name']
                if Name.endswith('#0'):
                    Name=Name[:-2]
                KDA=float(row['KDA'])

                TotalKDA[Name]=KDA

        for member in msg.guild.members:
            if(str(member) in TotalKDA.keys()):
                if(member.nick !=None):
                    TotalKDA[str(member.nick)]=TotalKDA[str(member)]
                    del TotalKDA[str(member)]
                elif(member.global_name!=None):
                    TotalKDA[str(member.global_name)]=TotalKDA[str(member)]
                    del TotalKDA[str(member)]     
        keys = list(TotalKDA.keys())
        values = list(TotalKDA.values())
        sorted_value_index = np.argsort(values)
        sorted_dict = {keys[i]: values[i] for i in sorted_value_index}
        sorted_dict=dict(reversed(list(sorted_dict.items())))
        #print(sorted_dict)
        ListOfKDA=list(sorted_dict)
        KDALeader='-__**KDA Leaderboard**__-\n'
        for x in range(0,10):
            if(x>=len(ListOfKDA)):
                break
            else:
                person=ListOfKDA[x]
                if(sorted_dict[person]==0):
                    break
                KDALeader=KDALeader+(str(x+1)+': '+person+" with "+ str(sorted_dict[person])+'\n')
        #print(ListOfLikes)
        await msg.channel.send(KDALeader)
        print('Post KDALeaderbaord')
        return 
    
    elif text.startswith('!kda'): #posts indivdual kda
        df3=pd.read_csv('snipe.csv')
        listOfNames= df3['Name'].values
        
        author =msg.author.nick
        if(author==None or str(author) not in listOfNames):
            author=msg.author
        if(str(author) not in listOfNames):
            await msg.channel.send("Try Sinping or being Sniped First")
            return
        mask = df3['Name'] == str(author)
        result = df3[df3['Name'] == str(author)] #gets the row with the target user
        KDA=result['KDA'].values[0] #gets the values
        
        await msg.channel.send(KDA)
        print('Post KDA')
        return
    
    elif "mine" in text:
        await msg.channel.send("W H O S E ?")
    
    
async def process_workout(msg):
    df4=pd.read_csv('workout.csv')
    author=str(msg.author)
    df4['Date'] = df4['Date'].astype(str)
    listOfNames= df4['Name'].values
    current_time = datetime.datetime.now()
    Date=str(current_time.month)+'/'+str(current_time.day)
    Hour=current_time.hour
    if len(msg.attachments)==0:
        return 
    else:
        if(author not in listOfNames):
                newPerson={'Name': author,'Workouts':1,'Date':Date,'Hour':Hour}
                tdf=pd.DataFrame(newPerson,index=[0]) 
                tdf.to_csv("workout.csv", mode='a', index=False,header=False)
                df4=pd.read_csv('snipe.csv')
        else:
            mask = df4['Name'] == author
            result = df4[df4['Name'] == author] #gets the row with the target user
            Day=result['Date'].values[0]
            Time=result['Hour'].values[0]
            print("Date",Day)
            print("Time",Time)
            if Day == Date and (Hour <= (Time+2)) :
                print("too soon")
            else:
                Workouts=result['Workouts'].values[0]
                Workouts=Workouts+1
                df4.loc[mask,'Workouts']=Workouts
                df4.loc[mask,'Date']=Date
                df4.loc[mask,'Hour']=Hour
                df4.to_csv("workout.csv", index=False) #updates csv file
    if  msg.mentions:
        for user in msg.mentions:
            user=str(user)
            if(user not in listOfNames):
                newPerson={'Name': user,'Workouts':1,'Date':Date,'Hour':Hour}
                tdf=pd.DataFrame(newPerson,index=[0]) 
                tdf.to_csv("workout.csv", mode='a', index=False,header=False)
                df4=pd.read_csv('snipe.csv')
            else:
                mask = df4['Name'] == user
                result = df4[df4['Name'] == user] #gets the row with the target user
                Day=result['Date'].values[0]
                Time=result['Hour'].values[0]
                if Day == Date and Hour <= (Time+2) :
                    print("Hi")
                else:
                    Workouts=result['Workouts'].values[0]
                    Workouts=Workouts+1
                    df4.loc[mask,'Workouts']=Workouts
                    df4.loc[mask,'Date']=Date
                    df4.loc[mask,'Hour']=Hour
                    df4.to_csv("workout.csv", index=False) #updates csv file


    



