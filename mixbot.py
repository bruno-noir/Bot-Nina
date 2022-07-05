import discord
from discord.ext import commands
import random
import requests
import json

client = discord.Client()

client = commands.Bot(command_prefix="!")

@client.command()
async def tell_me_about_yourself(ctx):
    text = "My name is Nina!\n Owner: Pratyush/noir. At present I have limited features(find out more by typing !help)\n :)"
    await ctx.send(text)

@client.command()
async def hello(ctx):
    text = "Hi:)"
    await ctx.send(text)

@client.command()
async def ping(ctx):
    text = "pong!"
    await ctx.send(text)

@client.command()
async def server(ctx):
    name = str(ctx.guild.name)
    description = str(ctx.guild.description)
    owner = str(ctx.guild.owner)
    id = str(ctx.guild.id)
    region = str(ctx.guild.region)
    memberCount = str(ctx.guild.member_count)
    icon = str(ctx.guild.icon_url)

    embed = discord.Embed(
        title=name + " Server Information",
        description=description,
        color=discord.Color.blue()
    )
    embed.set_thumbnail(url=icon)
    embed.add_field(name="Owner", value=owner, inline=True)
    embed.add_field(name="Server ID", value=id, inline=True)
    embed.add_field(name="Region", value=region, inline=True)
    embed.add_field(name="Member Count", value=memberCount, inline=True)

    await ctx.send(embed=embed)
    members=[]
    async for member in ctx.guild.fetch_members(limit=150) :
        await ctx.send('Name : {}\t Status : {}\n Joined at {}'.format(member.display_name,str(member.status),str(member.joined_at)))

#3 !single sends the message in chat

@client.command()
async def single(ctx):
    embed = discord.Embed(title="", description="") #You can add a text in there if you want
    color = 0x9b59b6
#embed.add_field(name="**Add something**", value="Or delete this.", inline=False) 
    embed.set_image(url="https://media.giphy.com/media/4ftxO9bk1OJgI/giphy.gif")
    embed.set_footer(text="Hehe, how's she? ^^")
    await ctx.send(embed=embed) #"ctx.author.send" sends the message in the DMs change to "ctx.send" to send it in chat

#2 !tictactoe @player1 @player2 to play tictactoe with a friend

player1 = ""
player2 = ""
turn = ""
gameOver = True

board = []

winningConditions = [
    [0, 1, 2],
    [3, 4, 5],
    [6, 7, 8],
    [0, 3, 6],
    [1, 4, 7],
    [2, 5, 8],
    [0, 4, 8],
    [2, 4, 6]
]

@client.command()
async def tictactoe(ctx, p1: discord.Member, p2: discord.Member):
    global count
    global player1
    global player2
    global turn
    global gameOver

    if gameOver:
        global board
        board = [":white_large_square:", ":white_large_square:", ":white_large_square:",
                 ":white_large_square:", ":white_large_square:", ":white_large_square:",
                 ":white_large_square:", ":white_large_square:", ":white_large_square:",]
        turn = ""
        gameOver = False
        count = 0

        player1 = p1
        player2 = p2

        # print the board
        line = ""
        for x in range(len(board)):
            if x == 2 or x == 5 or x == 8:
                line += " " + board[x]
                await ctx.send(line)
                line = ""
            else:
                line += " " + board[x]

        # determine who goes first
        num = random.randint(1, 2)
        if num == 1:
            turn = player1
            await ctx.send("It is <@" + str(player1.id) + ">'s turn.")
        elif num == 2:
            turn = player2
            await ctx.send("It is <@" + str(player2.id) + ">'s turn.")
    else:
        await ctx.send("A game is already in progress! Finish it before starting a new one.")

@client.command()
async def place(ctx, pos: int):
    global turn
    global player1
    global player2
    global board
    global count
    global gameOver

    if not gameOver:
        mark = ""
        if turn == ctx.author:
            if turn == player1:
                mark = ":regional_indicator_x:"
            elif turn == player2:
                mark = ":o2:"
            if 0 < pos < 10 and board[pos - 1] == ":white_large_square:" :
                board[pos - 1] = mark
                count += 1

                # print the board
                line = ""
                for x in range(len(board)):
                    if x == 2 or x == 5 or x == 8:
                        line += " " + board[x]
                        await ctx.send(line)
                        line = ""
                    else:
                        line += " " + board[x]

                checkWinner(winningConditions, mark)
                print(count)
                if gameOver == True:
                    await ctx.send(mark + " wins!")
                elif count >= 9:
                    gameOver = True
                    await ctx.send("It's a tie!")

                # switch turns
                if turn == player1:
                    turn = player2
                elif turn == player2:
                    turn = player1
            else:
                await ctx.send("Be sure to choose an integer between 1 and 9 (inclusive) and an unmarked tile.")
        else:
            await ctx.send("It is not your turn.")
    else:
        await ctx.send("Please start a new game using the !tictactoe command.")


def checkWinner(winningConditions, mark):
    global gameOver
    for condition in winningConditions:
        if board[condition[0]] == mark and board[condition[1]] == mark and board[condition[2]] == mark:
            gameOver = True

@tictactoe.error
async def tictactoe_error(ctx, error):
    print(error)
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Please mention 2 players for this command.")
    elif isinstance(error, commands.BadArgument):
        await ctx.send("Please make sure to mention/ping players (ie. <@688534433879556134>).")

@place.error
async def place_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send("Please enter a position you would like to mark.")
    elif isinstance(error, commands.BadArgument):
        await ctx.send("Please make sure to enter an integer.")

# 4. !insire to get motivational quotes
def get_quote():
  response = requests.get("https://zenquotes.io/api/random")
  json_data = json.loads(response.text)
  quote = json_data[0]['q'] + " -" + json_data[0]['a']
  # q for quote and a for author
  return(quote)

sad_words = ["cdc", "kgp", "society", "love", "cheer bot"]
starter_encouragements = [
  "lol;)", "Need a rope?", "Have fun. ^^", "You're the worst."
]
@client.event
async def on_message(message):
    if message.author == client.user:
        return
    msg = message.content
    if msg.startswith('!inspire'):
        quote = get_quote()
        await message.channel.send(quote)
    if any(word in msg for word in sad_words):
      await message.channel.send(random.choice(starter_encouragements))

#to get random gifs

punch_gifs = ['https://c.tenor.com/UH8Jnl1W3CYAAAAC/anime-punch-anime.gif', 'https://c.tenor.com/6a42QlkVsCEAAAAd/anime-punch.gif',
              'https://c.tenor.com/uaoyO8y01vMAAAAC/naruto-sasuke.gif', 'https://c.tenor.com/tlgJzKeIlJkAAAAC/anya-forger-spy-x-family.gif']
slap_gifs = ['https://c.tenor.com/FJsjk_9b_XgAAAAC/anime-hit.gif', 'https://c.tenor.com/eU5H6GbVjrcAAAAC/slap-jjk.gif',
             'https://c.tenor.com/ra17G61QRQQAAAAC/tapa-slap.gif', 'https://c.tenor.com/ILl8K-ur6iEAAAAC/baka-anime.gif',
             'https://c.tenor.com/yl9kMAB2pHYAAAAC/slap.gif', 'https://c.tenor.com/h_qFkmXJnYQAAAAC/cat-attack.gif']
react_gifs = ['https://c.tenor.com/3y749BALx1IAAAAd/nod-anime-anime.gif', 'https://c.tenor.com/PZlhV5eKTiMAAAAC/good-night.gif',
             'https://c.tenor.com/4g4c7CE1jkIAAAAd/eat-eats.gif', 'https://c.tenor.com/MWpSpZnhk2sAAAAd/eat-anime.gif', 'https://c.tenor.com/Y-9-VTaDbQMAAAAC/anime-anime-shy.gif']
kick_gifs = ['https://c.tenor.com/ZRJrwIlTqYAAAAAd/life-wasted.gif', 'https://c.tenor.com/k9QsoTYjJSUAAAAC/kick-anime.gif'
             'https://c.tenor.com/KBo6zdxSC3MAAAAd/spy-x-family-loid-forger.gif', 'https://c.tenor.com/lxd8SO_uRIYAAAAC/anime-kick.gif' ]

punch_names = ['Punches You!']
slap_names = ['Slapes You!']
react_names = ['Reacted to You!']
kick_names = ['Strike 1!']

@client.command()
async def punch(ctx):
    embed = discord.Embed(
        colour=(discord.Colour.random()),
        description = f"{ctx.author.mention} {(random.choice(punch_names))}"
    )
    embed.set_image(url=(random.choice(punch_gifs)))

    await ctx.send(embed=embed)

@client.command()
async def slap(ctx):
    embed = discord.Embed(
        colour=(discord.Colour.random()),
        description = f"{ctx.author.mention} {(random.choice(slap_names))}"
    )
    embed.set_image(url=(random.choice(slap_gifs)))

    await ctx.send(embed=embed)

@client.command()
async def react(ctx):
    embed = discord.Embed(
        colour=(discord.Colour.random()),
        description = f"{ctx.author.mention} {(random.choice(react_names))}"
    )
    embed.set_image(url=(random.choice(react_gifs)))

    await ctx.send(embed=embed)

@client.command()
async def kick(ctx):
    embed = discord.Embed(
        colour=(discord.Colour.random()),
        description = f"{ctx.author.mention} {(random.choice(kick_names))}"
    )
    embed.set_image(url=(random.choice(kick_gifs)))

    await ctx.send(embed=embed)

#-----------------------------------------------------------------------------------------#


# keep_alive()
client.run('OTkyODY3NDU4OTI5MTM1NjY2.GA19l0.RX5Z77xKsZUcj_oOpMn5UbHd5ZJQmdwgW5RBe0')