import discord
import asyncio
from discord.ext import commands
import urllib
import requests
from bs4 import BeautifulSoup
import json
import re
import random

class Funny(commands.Cog, name="Funny"):
    """검색 기능"""
    def __init__(self,bot):
        self.bot = bot

    @commands.command(aliases=['8ball','마법의고동'])
    async def _8ball(self, ctx, *, question):

        embed = discord.Embed(title = '마법의 고동', color = discord.Colour.green(), timestamp = ctx.message.created_at)

        embed.set_image(url="https://cdn.discordapp.com/attachments/653867722861445140/659276058507608084/08029efa49dec5e8.jpg")

        embed.set_thumbnail(url=bot.user.avatar_url)
        embed.set_footer(text = f'질문자 : {ctx.author}')

        responses = ['확실합니다.',
                     '100% 장담합니다.',
                     '물론!'
                     '저를 믿으세요, 맞습니다.',
                     '아마도 맞지 않을까요?'
                     '네.',
                     '아니요.',
                     '아닌거같아요',
                     '정확하지 않습니다',
                     '다시 한번 질문해주세요.',]

        embed.add_field(name= "질문: ", value = question, inline=False)

        embed.add_field(name= "답변: ", value = random.choice(responses), inline=False)

        await ctx.send(embed = embed)
        
    @commands.command()
    async def 끝말잇기(self, ctx):
        Search.is_wordend = True
        Search.firstTurn = True
        if Search.firstTurn:
            with open('dict.txt', 'r', encoding="utf-8") as f:
                s= f.read()
            pat = re.compile('^[ㄱ-ㅎ가-힣]+$')
            for i in sorted([i for i in s.split() if pat.match(i) and len(i)>=2], key = lambda x: -len(x)):
                if i[0] not in Search.wordDict:
                    Search.wordDict[i[0]] = set()
                Search.wordDict[i[0]].add(i)
            for i in Search.wordDict:
                for j in Search.wordDict[i]:
                    if j[-1] not in Search.wordDict:
                        Search.delList.append(j)
            for j in Search.delList:
                Search.onewords.add(j)
                Search.wordDict[j[0]].remove(j)
            await ctx.send('끝말잇기를 시작합니다')

    @commands.Cog.listener()
    async def on_message(self, message):
        if Search.is_wordend:
            if message.author.bot:
                pass
            else:
                firstLetter = message.content[0]

                if message.content == '포기한다':
                    await message.channel.send(f'이런 제가 이겼네요 ㅎㅎ')
                    Search.is_wordend = False
                    await message.channel.send(f"{message.author.display_name} 님의 점수: {Search.score}")
                else:    
                    if Search.firstTurn:
                        lastWord = random.choice(list(Search.wordDict[random.choice(list(Search.wordDict.keys()))]))
                        await message.channel.send(lastWord)
                        firstTurn = False
                    elif not firstTurn:
                        if firstLetter != lastWord[-1]:
                            await message.channel.send(lastWord[-1]+"(으)로 시작하는 단어를 입력하세요.")
                        elif message.content in Search.onewords:
                            await message.channel.send('한방단어는 사용할 수 없습니다')
                        elif message.content in Search.alreadySet:
                            await message.channel.send('이미 나온 단어입니다')
                        elif message.content not in Search.wordDict.get(firstLetter, set()):
                            await message.channel.send('사전에 없는단어 입니다')
                        else:
                            if Search.round >=20:
                                await message.channel.send("으앙 너무 잘하시네요 제가 졌어요")
                                await message.channel.send(Search.alreadySet)
                                await message.channel.send(f"{message.author.display_name} 님의 점수 : {Search.score}점")
                                Search.is_wordend = False
                            else:
                                Search.alreadySet.add(message.content)
                                lastWord = message.content
                                nextWords = sorted(filter(lambda x: x not in Search.alreadySet, Search.wordDict[message.content[-1]]), key=lambda x:-len(x))[:random.randint(20,50)]
                                lastWord = nextWords[random.randint(0, random.randrange(0, len(nextWords)))]
                                count = 0
                                while True:
                                    if len(lastWord) <= 5:
                                        break
                                    else:
                                        lastWord = nextWords[random.randint(0, random.randrange(0, len(nextWords)))]
                                    count += 1
                                    if count> 100:
                                        break
                                    print(lastWord)
                                    print(count)
                                await message.channel.send(lastWord)  
                                Search.alreadySet.add(lastWord)
                                Search.score += len(message.content)
                                Search.round +=1


def setup(bot):
    bot.add_cog(Funny(bot))
