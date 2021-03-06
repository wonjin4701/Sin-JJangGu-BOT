import discord
import asyncio
import datetime
from discord.ext import commands

class Welcome(commands.Cog):

    def __init__(self, bot):
        self.bot = bot


    @commands.Cog.listener()
    async def on_member_join(self, member):

        guild = member.guild
        channel = discord.utils.get(member.guild.channels, id=int("703107735100850277"))
      
        em = discord.Embed(description = f'{member}님 {guild}에 오신것을 진심으로 환영합니다. :wave: :tada:\n<#685107380043907097> 한번 확인해 주시고 활동해 주세요.',colour = discord.Colour.blue())
        em.timestamp = datetime.datetime.utcnow()

        await channel.send(embed = em)
        role = discord.utils.get(member.guild.roles, id=int("684940280667045897"))
        await member.add_roles(role)


    @commands.Cog.listener()
    async def on_member_remove(self, member):

        guild = member.guild
        channel = discord.utils.get(member.guild.channels, id=int("703107735100850277"))

        em = discord.Embed(description = f'{member}님 {guild}에서 나가셨습니다.', colour = discord.Colour.red())
        em.timestamp = datetime.datetime.utcnow()

        await channel.send(embed = em)

def setup(bot):
    bot.add_cog(Welcome(bot))
