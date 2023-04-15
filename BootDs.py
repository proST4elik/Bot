import discord
from time import sleep
import random
import asyncio
import os
from youtube_dl import YoutubeDL
from discord.ext import commands
from discord import Activity, ActivityType

YDL_OPTIONS = {'format': 'worstaudio/best', 'noplaylist': 'False', 'simulate': 'True', 'key': 'FFmpegExtractAudio'}
FFMPEG_OPTIONS = {'before_options': '-reconcect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vh'}
intents = discord.Intents.default()
intents.members = True

token = 'MTA2NDIyMzAwNDgwMTkxMjkyMg.GGUdnV.LLV9XH2JeOV3fn25MalLIY6oS6yI7BJiOYOS4o'
prefix = ' '

iii = discord.Intents.all()
bot = commands.Bot(command_prefix='!', intents=iii)
bot.remove_command('help')

POST_ID = 1077661617589858344
ROLE = {
    'Verified': 1077663712476942466
}


@bot.command(name='ping')
async def pint(ctx):
    await ctx.send(f'{ctx.author.mention} pong! {ctx}')


# Очистка
@bot.command(pass_context=True)
async def clear(ctx, amount=1):
    await ctx.channel.purge(limit=amount + 1)
    channel = bot.get_channel(1077815431944994886)
    await channel.send(f'{ctx.author.mention} очистил чат на {amount} сообщений')


# Кик
@bot.command(pass_context=True)
@commands.has_permissions(administrator=True)
async def kick(ctx, member: discord.Member, *, reason):
    await ctx.channel.purge(limit=1)
    emb = discord.Embed(title=f'Вы были кикнуты с причиной {reason}!', color=0xFF0000)
    emb.add_field(name="Кик считается как предупреждение.",
                  value='После повторного вступления вы можете общаться как письменно и так в голосовом', inline=False)
    emb.add_field(name="Приятного пользования и впредь не нарушайте",
                  value='', inline=False)
    emb.set_author(name=f'{member.name}#{member.discriminator}')
    await member.send(embed=emb)
    await member.kick(reason=reason)
    await ctx.send(f'{ctx.author.mention} Выгнал {member.mention} причина: {reason}')
    channel = bot.get_channel(1077815431944994886)
    await channel.send(f'{ctx.author.mention} кикнул {member.mention} причина: {reason}')


# Бан
@bot.command(pass_context=True)
@commands.has_permissions(administrator=True)
async def ban(ctx, member: discord.Member, time, reason):
    await ctx.channel.purge(limit=1)
    emb = discord.Embed(title=f'Администратор выдал вам бан на {time} минут с причиной {reason}!', color=0xFF0000)
    emb.add_field(name="Пока не истечёт срок вы не сможете заходить в наш канал",
                  value='Если не согласны с нарушением то можете обсудить с модератором в лс', inline=False)
    emb.set_author(name=f'{member.name}#{member.discriminator}')
    await member.send(embed=emb)
    await member.ban(reason=reason)
    await ctx.send(f'{ctx.author.mention} забанил {member.mention} на {time} минут причина: {reason}')
    channel = bot.get_channel(1077815431944994886)
    await channel.send(f'{ctx.author.mention} забанил {member.mention} на {time} минут причина: {reason}')
    time = int(time)
    time = time * 60
    await asyncio.sleep(time)
    await member.unban()


# Мут
@bot.command(pass_context=True)
@commands.has_permissions(administrator=True)
async def mute(ctx, member: discord.Member, time, reason):
    await ctx.channel.purge(limit=1)
    guild = bot.get_guild(1039241319832358942)
    role = guild.get_role(1064258942886215750)
    await member.add_roles(role)
    channel = bot.get_channel(1077815431944994886)
    await channel.send(f'{ctx.author.mention} замутил {member.mention} на {time} минут причина: {reason}')
    await ctx.send(f'{ctx.author.mention} замутил {member.mention} на {time} минут причина: {reason}')
    emb = discord.Embed(title=f'Администратор выдал вам бан чата на {time} минут с причиной {reason}!', color=0xFF0000)
    emb.add_field(name="Пока не истечёт срок вы не сможете пистаь и общатся",
                  value='Если не согласны с нарушением то можете обратится в канала жалобы', inline=False)
    emb.set_author(name=f'{member.name}#{member.discriminator}')
    await member.send(embed=emb)
    time = int(time)
    time = time * 60
    await asyncio.sleep(time)
    await member.remove_roles(role)
    emb = discord.Embed(title='Ваш срок мута истёк!', color=0xFFD700)
    emb.add_field(name="Теперь вам доступен полный функционал",
                  value='Вы можете общатся как письменно и так в голосовом', inline=False)
    emb.add_field(name="Приятного пользования и впредь не нарушайте",
                  value='', inline=False)
    emb.set_author(name=f'{member.name}#{member.discriminator}')
    await member.send(embed=emb)


# АнМут
@bot.command(pass_context=True)
@commands.has_permissions(administrator=True)
async def unmute(ctx, member: discord.Member, *, reason):
    await ctx.channel.purge(limit=1)
    guild = bot.get_guild(1039241319832358942)
    role = guild.get_role(1064258942886215750)
    await member.remove_roles(role)
    await ctx.send(f'{ctx.author.mention} размутил {member.mention} причина: {reason}')
    emb = discord.Embed(title='Вы размучены!', color=0xFFD700)
    emb.add_field(name="Теперь вам доступен полный функционал",
                  value='Вы можете общатся как письменно и так в голосовом', inline=False)
    emb.add_field(name="Приятного пользования и впредь не нарушайте",
                  value='', inline=False)
    emb.set_author(name=f'{member.name}#{member.discriminator}')
    await member.send(embed=emb)
    channel = bot.get_channel(1077815431944994886)
    await channel.send(f'{ctx.author.mention} размутил {member} причина: {reason}')


# Хелп

@bot.command(name='help')
async def help(ctx, member: discord.Member = None):
    embed = discord.Embed(title=f">>  Команды пользователей  <<", color=0x00FFFF)

    embed.set_author(name=f"{ctx.author}")
    embed.add_field(name=f"***!кто*** --- бот выберите случайного человека",
                    value=f"Пример: !кто лучший", inline=False)
    embed.add_field(name=f"***!pay*** --- вы можете перевести кому-то свои накопления",
                    value=f"Пример: !pay @1234 100", inline=False)
    embed.add_field(name=f"***!khelp*** --- помощь по командам казино",
                    value=f"Пример: !khelp", inline=False)
    embed.add_field(name=f"***!balance*** --- вы можете посмотреть свой баланс",
                    value=f"Пример: !balance", inline=False)
    await ctx.channel.purge(limit=1)
    await ctx.send(embed=embed)


@bot.command(name='helpa')
@commands.has_permissions(administrator=True)
async def helpa(ctx, member: discord.Member = None):
    embed = discord.Embed(title=f">>  Команды модераторов  <<", color=0x9370DB)
    embed.set_author(name=f"{ctx.author}")
    embed.add_field(name=f"***!mute*** --- отключить возможность говорить и писать человеку",
                    value=f"Пример: !mute @1234 время причина", inline=False)
    embed.add_field(name=f"***!unmute*** --- вернуть все возможности человку", value=f"Пример: !unmute @1234 причина",
                    inline=False)
    embed.add_field(name=f"***!ban*** --- добавить человека в черный список и выгнать",
                    value=f"Пример: !ban @1234 время причина",
                    inline=False)
    embed.add_field(name=f"***!unban*** --- убрать человека из чероного списка", value=f"Пример: !unban @1234 причина",
                    inline=False)
    embed.add_field(name=f"***!kick*** --- выгнать человека", value=f"Пример: !kick @1234 причина", inline=False)
    embed.add_field(name=f"***!givemoney*** --- выдать деньги пользователю", value=f"Пример: !givemoney @1234 100",
                    inline=False)
    embed.add_field(name=f"***!clear*** --- удалить последние сообщения", value=f"Пример: !clear 40", inline=False)
    await ctx.channel.purge(limit=1)
    await ctx.send(embed=embed)


@bot.command(name='khelp')
async def khelp(ctx):
    embed = discord.Embed(title=f">>  Команды казино  <<", color=0x00FFFF)

    embed.set_author(name=f"{ctx.author.mention}")
    embed.add_field(name=f"***!orel*** --- вы подбросите монетку с крупье с выбранной стороной орел",
                    value=f"Пример: !orel 100", inline=False)
    embed.add_field(name=f"***!reshka*** --- вы подбросите монетку с крупье с выбранной стороной решкой",
                    value=f"Пример: !reshka 100", inline=False)
    embed.add_field(name=f"***!balance*** --- вы можете посмотреть свой баланс",
                    value=f"Пример: !balance", inline=False)
    await ctx.channel.purge(limit=1)
    await ctx.send(embed=embed)


@bot.command(name='orel')
async def orel(ctx, amount):
    file = open(str(ctx.author.id) + ".txt", "r")
    balance = file.read()
    file.close()
    balance = int(balance)
    amount = int(amount)

    if balance < amount:
        await ctx.send("У вас недостаточной средств")
    else:
        choice = random.randint(1, 2)
        if choice == 1:
            file = open(str(ctx.author.id) + ".txt", "r")
            balance = file.read()
            file.close()
            file = open(str(ctx.author.id) + ".txt", "w")
            balance = int(balance)
            amount = int(amount)
            balance = balance + amount
            file.write(str(balance))
            file.close()
            channel = bot.get_channel(1077815824863203358)

            embed = discord.Embed(title=f">>  {ctx.author.mention} вы выйграли  <<", color=0x00FF00)
            embed.add_field(name=f"💰 Вы выйграли: {amount} 💱",
                            value=f"💸 Ваш баланс: {balance} 💳", inline=False)
            await ctx.send(embed=embed)
            channel = bot.get_channel(1077815824863203358)

            await channel.send(f'{ctx.author.mention} выйграл {amount} и его баланс стал: {balance}')
        else:
            file = open(str(ctx.author.id) + ".txt", "r")
            balance = file.read()
            file.close()
            file = open(str(ctx.author.id) + ".txt", "w")
            balance = int(balance)
            amount = int(amount)
            balance = balance - amount
            file.write(str(balance))
            file.close()

            embed = discord.Embed(title=f">>  {ctx.author.mention} вы проиграли  <<", color=0xFF0000)
            embed.add_field(name=f"💰 Вы проиграли: {amount} 💱",
                            value=f"💸 Ваш баланс: {balance} 💳", inline=False)
            await ctx.send(embed=embed)

            channel = bot.get_channel(1077815824863203358)
            await channel.send(f'{ctx.author.mention} проиграл {amount} и его баланс стал: {balance}')


@bot.command(name='reshka')
async def reshka(ctx, amount):
    file = open(str(ctx.author.id) + ".txt", "r")
    balance = file.read()
    file.close()
    balance = int(balance)
    amount = int(amount)

    if balance < amount:
        await ctx.send("У вас недостаточной средств")
    else:
        choice = random.randint(1, 2)
        if choice == 1:
            file = open(str(ctx.author.id) + ".txt", "r")
            balance = file.read()
            file.close()
            file = open(str(ctx.author.id) + ".txt", "w")
            balance = int(balance)
            amount = int(amount)
            balance = balance + amount
            file.write(str(balance))
            file.close()

            channel = bot.get_channel(1077815824863203358)
            embed = discord.Embed(title=f">>  {ctx.author.mention} вы выйграли  <<", color=0x00FF00)
            embed.add_field(name=f"💰 Вы выйграли: {amount} 💱",
                            value=f"💸 Ваш баланс: {balance} 💳", inline=False)
            await ctx.send(embed=embed)
            await channel.send(f'{ctx.author.mention} выйграл {amount} и его баланс стал: {balance}')
        else:
            file = open(str(ctx.author.id) + ".txt", "r")
            balance = file.read()
            file.close()
            file = open(str(ctx.author.id) + ".txt", "w")
            balance = int(balance)
            amount = int(amount)
            balance = balance - amount
            file.write(str(balance))
            file.close()

            embed = discord.Embed(title=f">>  {ctx.author.mention} вы проиграли  <<", color=0xFF0000)
            embed.add_field(name=f"💰 Вы проиграли: {amount} 💱",
                            value=f"💸 Ваш баланс: {balance} 💳", inline=False)
            await ctx.send(embed=embed)

            channel = bot.get_channel(1077815824863203358)
            await channel.send(f'{ctx.author.mention} проиграл {amount} и его баланс стал: {balance}')


@bot.command(name='orelm')
async def orelm(ctx, amount):
    file = open(str(ctx.author.id) + ".txt", "r")
    balance1 = file.read()
    file.close()
    balance1 = int(balance1)
    amount = int(amount)
    if balance1 < amount:
        await ctx.send("У вас или недостаточной средств")
    else:
        file = open(str(ctx.author.id) + "k.txt", "w")
        file.write(str(amount))
        file = open(str(ctx.author.id) + "k.txt", "r")
        find = file.read()
        file.close()
        await ctx.send(
            f"{ctx.author.mention} ищет игру на  {amount}\nДля подтверждения напшиите !accept {ctx.author.mention}")
        await asyncio.sleep(60)
        if find != '1':
            await ctx.send("Прошло 60 секунд и никто не принял вашу игру,ваша игра отменена")
            file = open(str(ctx.author.id) + "k.txt", "w")
            file.write("1")


@bot.command(name='accept')
async def accept(ctx, member: discord.Member):
    file = open(str(member.id) + "k.txt", "r")
    amoant = file.read()
    file.close()
    file = open(str(ctx.author.id) + ".txt")
    balancef = file.read()
    balancef = int(balancef)
    file = open(str(member.id) + "k.txt", "r")
    find = file.read()
    file.close()
    amoant = int(amoant)
    if find != '1' and balancef > amoant:
        rand = random.randint(1, 2)
        if rand == 1:
            await ctx.send(f"{ctx.author.mention} Вы выйграли {amoant} у пользователя {member.mention}")

            file = open(str(ctx.author.id) + "k.txt", "w")
            file.write("1")
            file = open(str(member.id) + "k.txt", "w")
            file.write("1")

            file = open(str(ctx.author.id) + ".txt", "r")
            balance1 = file.read()
            balance1 = int(balance1)
            file.close()

            file = open(str(ctx.author.id) + ".txt", "w")
            balance1 = balance1 + int(amoant)
            file.write(str(balance1))
            file.close()

            file = open(str(member.id) + ".txt", "r")
            balance = file.read()
            balance = int(balance)
            file.close()

            file = open(str(member.id) + ".txt", "w")
            balance = balance - int(amoant)
            file.write(str(balance))
            file.close()
            channel = bot.get_channel(1077815824863203358)
            await channel.send(
                f'{ctx.author.mention} выйграл {amoant} у пользователя {member.mention} и его баланс стал: {balance1}. Баланс проигравшего: {balance}')
        else:
            await ctx.send(f"{member.mention} Вы выйграли {amoant} у пользователя {ctx.author.mention}")
            file = open(str(ctx.author.id) + "k.txt", "w")
            file.write("1")
            file = open(str(member.id) + "k.txt", "w")
            file.write("1")

            file = open(str(ctx.author.id) + ".txt", "r")
            balance1 = file.read()
            balance1 = int(balance1)
            file.close()

            file = open(str(ctx.author.id) + ".txt", "w")
            balance1 = balance1 - int(amoant)
            file.write(str(balance1))
            file.close()

            file = open(str(member.id) + ".txt", "r")
            balance = file.read()
            balance = int(balance)
            file.close()

            file = open(str(member.id) + ".txt", "w")
            balance = balance + int(amoant)
            file.write(str(balance))
            file.close()
            channel = bot.get_channel(1077815824863203358)
            await channel.send(
                f'{member.mention} выйграл {amoant} у пользователя {ctx.author.mention} и его баланс стал: {balance}. Баланс проигравшего: {balance1}')
    else:
        await ctx.send("Срок игры истёк или у вас недостаточно денег")


@bot.command(name='change')
async def change(ctx):
    file = open(str(ctx.message.author.id) + ".txt", "r")
    balance = file.read()
    file.close()
    file = open(str(ctx.message.author.id) + "d.txt", "r")
    balanced = file.read()
    file.close()
    emb = discord.Embed(title='Магазин', color=0xff0000)
    emb.add_field(name=f"На вашем счету: {balance} монет ",
                  value=f'На вашем счету: {balanced} дискорд коинов', inline=False)
    emb.add_field(name="Вирты на аризона",
                  value='Напишите !virt', inline=False)
    emb.add_field(name="Ширп в кс",
                  value='Напишите !shirp', inline=False)
    await ctx.send(embed=emb)


@bot.command(name='virt')
async def virt(ctx):
    file = open(str(ctx.message.author.id) + "d.txt", "r")
    balanced = file.read()
    file.close()
    emb = discord.Embed(title='Вирты самп', color=0xff0000)
    emb.add_field(name=f"На вашем счету: {balanced} дискорд коинов ",
                  value=f'', inline=False)
    emb.add_field(name="Стоимость:",
                  value='10.000 дискорд коинов - 100.000 вирт', inline=False)
    emb.add_field(name="напишите сколько хотите обменять через !v кол-во",
                  value='', inline=False)
    await ctx.send(embed=emb)


@bot.command()
async def play(ctx, url):
    pass


@bot.command()
async def stop(ctx):
    """Остановка воспроизведения музыки"""
    pass


@bot.command()
async def skip(ctx):
    """Пропустить текущий трек"""
    pass


rankroles = [1096429415614922883, 1096436790543515658, 1096482869356019793, 1096484527532159016, 1096491282622316544,
             1096491484158640148, 1096493389270225006, 1096499911387783298, 1096501535392927885]


@bot.command(pass_context=True)
async def кто(ctx, who):
    await ctx.send(f'{who} - {random.choice(ctx.guild.members).mention}')


# первый заход
@bot.event
async def on_member_join(member: discord.Member):
    emb = discord.Embed(title='Добро пожаловать в Логово', color=0xff0000)
    emb.add_field(name="Для получения полного функционала пройди верификацию",
                  value='Пройти её можно тут: <#1077656952802377870>.', inline=False)
    emb.add_field(name="Также чтоб не было притензий и разногласий",
                  value='Тебе необходимо прочитать правила <#1077660086769557636>', inline=False)
    emb.set_author(name=f'{member.name}#{member.discriminator}')
    await member.send(embed=emb)
    guild = bot.get_guild(1039241319832358942)
    role = guild.get_role(1077676330415562872)
    await member.add_roles(role)
    try:
        file = open(str(member.id) + ".txt", "r")
        file.close()
    except:
        file = open(str(member.id) + ".txt", "w")
        file.write("1000")
        file.close()
    try:
        file = open(str(member.id) + "k.txt", "r")
        file.close()
    except:
        file = open(str(member.id) + "k.txt", "w")
        file.write("0")
        file.close()

    try:
        file = open(str(member.id) + "rank.txt", "r")
        file.close()
    except:
        file = open(str(member.id) + "rank.txt", "w")
        file.write("0")
        file.close()

    try:
        file = open(str(member.id) + "d.txt", "r")
        file.close()
    except:
        file = open(str(member.id) + "d.txt", "w")
        file.write("0")
        file.close()
    try:
        file = open(str(member.id) + ".txt", "r")
        file.close()
    except:
        file = open(str(member.id) + ".txt", "w")
        file.write("0")
        file.close()


@bot.command(name='balance')
async def balance(ctx):
    file = open(str(ctx.message.author.id) + ".txt", "r")
    balance = file.read()
    file.close()
    file = open(str(ctx.message.author.id) + "d.txt", "r")
    balanced = file.read()
    file.close()
    embed = discord.Embed(title=f">>  Баланс  <<", color=0x20B2AA)
    embed.add_field(name=f"💰 {ctx.author} ваш баланс: {balance}",
                    value=f"", inline=False)
    embed.add_field(name=f"💰 Баланс Дискорд Коинов: {balanced}",
                    value=f"", inline=False)
    await ctx.send(embed=embed)


@bot.command(name='pay')
async def pay(ctx, member: discord.Member, amount):
    file = open(str(ctx.message.author.id) + ".txt", "r")
    balance = file.read()
    file.close()
    balance = int(balance)
    amount = int(amount)
    if balance > amount:
        balance = int(balance)
        amount = int(amount)
        balance = balance - amount
        file = open(str(ctx.message.author.id) + ".txt", "w")
        file.write(str(balance))
        file.close()

        file = open(str(member.id) + ".txt", "r")
        balance = file.read()
        file.close()
        file = open(str(member.id) + ".txt", "w")
        balance = int(balance)
        balance = balance + amount
        file.write(str(balance))
        file.close()
        await ctx.send(f"{ctx.author.mention} вы успешно перевели {amount} пользователю {member.mention}")
        channel = bot.get_channel(1077815824863203358)
        await channel.send(f'{ctx.author.mention} передал {amount} пользователю {member.mention}')
    else:
        await ctx.send("У вас не достаточно денег")


@bot.command(name='givemoney')
@commands.has_permissions(administrator=True)
async def givemoney(ctx, member: discord.Member, amount):
    file = open(str(member.id) + ".txt", "r")
    balance = file.read()
    file.close()
    file = open(str(member.id) + ".txt", "w")
    balance = int(balance)
    amount = int(amount)
    balance = balance + amount
    file.write(str(balance))
    file.close()
    channel = bot.get_channel(1077815431944994886)
    await channel.send(f'{ctx.author.mention} выдал {amount} пользователю {member.mention}')


@bot.command(name='setrank')
async def setrank(ctx, member: discord.Member, rank):
    file = open(str(member.id) + "rank.txt", 'w')
    file.write(str(rank))
    rank = str(rank)
    if rank == '1':
        guild = bot.get_guild(1039241319832358942)
        for role1 in rankroles:
            role2 = guild.get_role(role1)
            await member.remove_roles(role2)
        role = guild.get_role(rankroles[0])
        await member.add_roles(role)

        channel = bot.get_channel(1077815431944994886)
        await channel.send(f'{ctx.author.mention} выдал {rank} ранг игроку {member.mention}')
        await ctx.send(f'{ctx.author.mention} выдал {rank} ранг игроку {member.mention}')
    elif rank == '2':
        guild = bot.get_guild(1039241319832358942)
        for role1 in rankroles:
            role2 = guild.get_role(role1)
            await member.remove_roles(role2)
        role = guild.get_role(rankroles[1])
        await member.add_roles(role)
        channel = bot.get_channel(1077815431944994886)
        await channel.send(f'{ctx.author.mention} выдал {rank} ранг игроку {member.mention}')
        await ctx.send(f'{ctx.author.mention} выдал {rank} ранг игроку {member.mention}')
    elif rank == '3':
        guild = bot.get_guild(1039241319832358942)
        for role1 in rankroles:
            role2 = guild.get_role(role1)
            await member.remove_roles(role2)
        role = guild.get_role(rankroles[2])
        await member.add_roles(role)

        channel = bot.get_channel(1077815431944994886)
        await channel.send(f'{ctx.author.mention} выдал {rank} ранг игроку {member.mention}')
        await ctx.send(f'{ctx.author.mention} выдал {rank} ранг игроку {member.mention}')
    elif rank == '4':
        guild = bot.get_guild(1039241319832358942)
        for role1 in rankroles:
            role2 = guild.get_role(role1)
            await member.remove_roles(role2)
        role = guild.get_role(rankroles[3])
        await member.add_roles(role)
        channel = bot.get_channel(1077815431944994886)
        await channel.send(f'{ctx.author.mention} выдал {rank} ранг игроку {member.mention}')
        await ctx.send(f'{ctx.author.mention} выдал {rank} ранг игроку {member.mention}')
    elif rank == '5':
        guild = bot.get_guild(1039241319832358942)
        for role1 in rankroles:
            role2 = guild.get_role(role1)
            await member.remove_roles(role2)
        role = guild.get_role(rankroles[4])
        await member.add_roles(role)
        channel = bot.get_channel(1077815431944994886)
        await channel.send(f'{ctx.author.mention} выдал {rank} ранг игроку {member.mention}')
        await ctx.send(f'{ctx.author.mention} выдал {rank} ранг игроку {member.mention}')
    elif rank == '6':
        guild = bot.get_guild(1039241319832358942)
        for role1 in rankroles:
            role2 = guild.get_role(role1)
            await member.remove_roles(role2)
        role = guild.get_role(rankroles[5])
        await member.add_roles(role)
        channel = bot.get_channel(1077815431944994886)
        await channel.send(f'{ctx.author.mention} выдал {rank} ранг игроку {member.mention}')
        await ctx.send(f'{ctx.author.mention} выдал {rank} ранг игроку {member.mention}')
    elif rank == '7':
        guild = bot.get_guild(1039241319832358942)
        for role1 in rankroles:
            role2 = guild.get_role(role1)
            await member.remove_roles(role2)
        role = guild.get_role(rankroles[6])
        await member.add_roles(role)
        channel = bot.get_channel(1077815431944994886)
        await channel.send(f'{ctx.author.mention} выдал {rank} ранг игроку {member.mention}')
        await ctx.send(f'{ctx.author.mention} выдал {rank} ранг игроку {member.mention}')
    elif rank == '8':
        guild = bot.get_guild(1039241319832358942)
        for role1 in rankroles:
            role2 = guild.get_role(role1)
            await member.remove_roles(role2)
        role = guild.get_role(rankroles[7])
        await member.add_roles(role)
        channel = bot.get_channel(1077815431944994886)
        await channel.send(f'{ctx.author.mention} выдал {rank} ранг игроку {member.mention}')
        await ctx.send(f'{ctx.author.mention} выдал {rank} ранг игроку {member.mention}')
    elif rank == '9':
        guild = bot.get_guild(1039241319832358942)
        for role1 in rankroles:
            role2 = guild.get_role(role1)
            await member.remove_roles(role2)
        role = guild.get_role(rankroles[8])
        await member.add_roles(role)
        channel = bot.get_channel(1077815431944994886)
        await channel.send(f'{ctx.author.mention} выдал {rank} ранг игроку {member.mention}')
        await ctx.send(f'{ctx.author.mention} выдал {rank} ранг игроку {member.mention}')


@bot.command(name='ungivemoney')
@commands.has_permissions(administrator=True)
async def ungivemoney(ctx, member: discord.Member, amount):
    file = open(str(member.id) + ".txt", "r")
    balance = file.read()
    file.close()
    file = open(str(member.id) + ".txt", "w")
    balance = int(balance)
    amount = int(amount)
    balance = balance - amount
    file.write(str(balance))
    file.close()
    channel = bot.get_channel(1077815431944994886)
    await channel.send(f'{ctx.author.mention} забрал {amount} пользователю {member.mention}') \
 \
    @ bot.command(name='test')


async def test(ctx):
    emb = discord.Embed(title='Состояние бота:', color=0xff0000)
    emb.add_field(name="Пинг:",
                  value=f"{round(bot.latency * 1000)}мс", inline=False)
    emb.add_field(name="Настоящие имя: ",
                  value='{0.user.name}'.format(bot), inline=False)
    await ctx.send(embed=emb)


@bot.command(name='unban')
@commands.has_permissions(ban_members=True)
async def unban(ctx, member, reason):
    banned_users = ctx.guild.bans()
    member_name, member_discriminator = member.split('#')

    async for ban_entry in banned_users:
        user = ban_entry.user

        if (user.name, user.discriminator) == (member_name, member_discriminator):
            await ctx.guild.unban(user)
            await ctx.send(f'{ctx.author.mention} разбанил пользователя {user.mention} причина: {reason} ')
            channel = bot.get_channel(1077815431944994886)
            await channel.send(f'{ctx.author.mention} разбанил пользователя {user.mention} причина: {reason}')
            return


@bot.event
async def on_raw_reaction_add(payload):
    if payload.message_id == 1077661617589858344 and payload.emoji.name == "✅":
        guild = bot.get_guild(1039241319832358942)
        role = guild.get_role(1077663712476942466)
        role2 = guild.get_role(1096429415614922883)
        member = guild.get_member(payload.user_id)
        await member.add_roles(role)
        await member.add_roles(role2)
        role1 = guild.get_role(1077676330415562872)
        await member.remove_roles(role1)
        emb = discord.Embed(title='Вы верифицировались!', color=0xff0000)
        emb.add_field(name="Теперь вам доступен полный функционал",
                      value='Вы можете общатся как письменно и так в голосовом', inline=False)
        emb.add_field(name="Приятного пользования",
                      value='', inline=False)
        emb.set_author(name=f'{member.name}#{member.discriminator}')
        await member.send(embed=emb)


@bot.event
async def on_ready():
    print('Logged in as:\n{0.user.name}\n{0.user.id}'.format(bot))
    await bot.change_presence(activity=Activity(name="за LosDiablos.", type=ActivityType.watching))


bot.run(token)