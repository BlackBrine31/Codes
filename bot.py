import discord
import os
import requests
import json
import random
from replit import db
from keep_alive import keep_alive
from discord.ext import commands
import openai

intents = discord.Intents.all()
bot = commands.Bot(command_prefix='/', intents=intents)


sad_words = ["sad", "depressed", "unhappy", "angry", "miserable"]
starter_encouragements = ["Cheer up!", "Hang in there.", "You are a great person!"]
SYSTEM_PROMPT = """You are ChatGPT, a friendly and helpful AI assistant in a Discord server. 
You have a playful personality but are always professional when needed. 
You can make jokes but avoid offensive content. 
Keep your responses concise but informative when needed."""

if "encouragements" not in db.keys():
    db["encouragements"] = starter_encouragements.copy()
if "responding" not in db.keys():
    db["responding"] = True
if "conversations" not in db.keys():
    db["conversations"] = {}


openai.api_key = os.getenv('OPENAI_API_KEY')

def get_quote():
    response = requests.get("https://zenquotes.io/api/random")
    json_data = json.loads(response.text)
    return f"{json_data[0]['q']} -{json_data[0]['a']}"

def update_encouragements(message):
    if "encouragements" not in db.keys():
        db["encouragements"] = starter_encouragements.copy()
    encouragements = db["encouragements"].copy()
    encouragements.append(message)
    db["encouragements"] = encouragements

def delete_encouragement(index):
    if "encouragements" not in db.keys():
        db["encouragements"] = starter_encouragements.copy()
    encouragements = db["encouragements"].copy()
    if len(encouragements) > index:
        encouragements.pop(index)
        db["encouragements"] = encouragements

@bot.event
async def on_ready():
    await bot.tree.sync()
    print(f'{bot.user} has connected to Discord!')


@bot.hybrid_command(description="Chat with the AI")
async def chat(ctx, *, message: str):
    try:
        async with ctx.typing():
            response = openai.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": message}
                ]
            )
            ai_response = response.choices[0].message['content']

            if len(ai_response) > 2000:
                chunks = [ai_response[i:i+2000] for i in range(0, len(ai_response), 2000)]
                for chunk in chunks:
                    await ctx.send(chunk)
            else:
                await ctx.send(ai_response)
    except Exception as e:
        await ctx.send(f"An error occurred: {e}")

@bot.hybrid_command(description="Continue conversation with AI")
async def continue_chat(ctx, *, message: str):
    user_id = str(ctx.author.id)

    if user_id not in db["conversations"]:
        db["conversations"][user_id] = [
            {"role": "system", "content": SYSTEM_PROMPT}
        ]

    db["conversations"][user_id].append({"role": "user", "content": message})

    try:
        async with ctx.typing():
            response = openai.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=db["conversations"][user_id]
            )
            ai_message = response.choices[0].message
            ai_response = ai_message['content']

            db["conversations"][user_id].append(ai_message)

            if len(ai_response) > 2000:
                chunks = [ai_response[i:i+2000] for i in range(0, len(ai_response), 2000)]
                for chunk in chunks:
                    await ctx.send(chunk)
            else:
                await ctx.send(ai_response)
    except Exception as e:
        await ctx.send(f"An error occurred: {e}")

@bot.hybrid_command(description="Reset conversation with AI")
async def reset_chat(ctx):
    user_id = str(ctx.author.id)
    if user_id in db["conversations"]:
        del db["conversations"][user_id]
    await ctx.send("Conversation history cleared!")


@bot.hybrid_command(description="Greet the bot")
async def hello(ctx):
    await ctx.send(f"Hello {ctx.author.mention}!")

@bot.hybrid_command(description="Muting someone in the server")
@commands.has_permissions(manage_roles=True)
async def mute(ctx, member: discord.Member, *, reason=None):
    muted_role = await get_muted_role(ctx.guild)

    if muted_role in member.roles:
        await ctx.send(f"{member.mention} is already muted!")
        return

    try:
        await member.add_roles(muted_role, reason=reason)
        await ctx.send(f"{member.mention} has been muted. Reason: {reason}")
    except discord.Forbidden:
        await ctx.send("I don't have permission to mute this user!")

async def get_muted_role(guild):
    muted_role = discord.utils.get(guild.roles, name="Muted")

    if not muted_role:
        try:
            muted_role = await guild.create_role(name="Muted")
            for channel in guild.channels:
                await channel.set_permissions(muted_role,
                    send_messages=False,
                    speak=False,
                    add_reactions=False)
        except discord.Forbidden:
            raise commands.CommandError("I don't have permission to create the Muted role!")

    return muted_role

@bot.hybrid_command(description="Ban a user from the server")
@commands.has_permissions(ban_members=True)  
async def ban(ctx, user: discord.Member, *, reason=None):
    try:
        await user.ban(reason=reason)  
        await ctx.send(f"Banned {user.mention} for: {reason}")  
    except:
        await ctx.channel.send("I don't have permission to ban this user!")

@bot.hybrid_command(description="Unban a user from the server")
@commands.has_permissions(ban_members=True)  
async def unban(ctx, user: discord.Member, *, reason=None):
    try:
        await user.unban(reason=reason)  
        await ctx.send(f"Unbanned {user.mention}")  
    except:
        await ctx.channel.send("I don't have permission to unban this user!")


active_games = {}
EMPTY = "⬜"
X = "❌"
O = "⭕"

@bot.hybrid_command(description="Start a game of Tic Tac Toe")
async def tictactoe(ctx, opponent: discord.Member):
    if ctx.author == opponent:
        await ctx.send("You can't play against yourself!")
        return

    board = [[EMPTY for _ in range(3)] for _ in range(3)]
    players = {ctx.author.id: X, opponent.id: O}
    current_player = ctx.author.id

    active_games[ctx.channel.id] = {
        "board": board,
        "players": players,
        "current_player": current_player
    }

    await display_board(ctx, board)

@bot.command(name="place", aliases=["p"])
async def place(ctx, row: int, col: int):
    game = active_games.get(ctx.channel.id)
    if not game:
        await ctx.send("No active game in this channel. Start one with `/tictactoe @opponent`")
        return

    if ctx.author.id != game["current_player"]:
        await ctx.send("It's not your turn!")
        return

    row -= 1  
    col -= 1

    if row < 0 or row > 2 or col < 0 or col > 2:
        await ctx.send("Row and column must be between 1 and 3!")
        return

    if game["board"][row][col] != EMPTY:
        await ctx.send("That spot is already taken!")
        return

    game["board"][row][col] = game["players"][ctx.author.id]

    winner = check_winner(game["board"])
    if winner:
        await display_board(ctx, game["board"])
        await ctx.send(f"🎉 **{winner} wins!** 🎉")
        del active_games[ctx.channel.id]
        return

    if all(cell != EMPTY for row in game["board"] for cell in row):
        await display_board(ctx, game["board"])
        await ctx.send("🤝 **It's a tie!** 🤝")
        del active_games[ctx.channel.id]
        return

    game["current_player"] = next(
        player_id for player_id in game["players"] 
        if player_id != ctx.author.id
    )

    await display_board(ctx, game["board"])

async def display_board(ctx, board):
    board_str = "\n".join("".join(row) for row in board)
    await ctx.send(f"```\n{board_str}\n```")

def check_winner(board):
    for row in board:
        if row[0] == row[1] == row[2] != EMPTY:
            return row[0]

    for col in range(3):
        if board[0][col] == board[1][col] == board[2][col] != EMPTY:
            return board[0][col]

    if board[0][0] == board[1][1] == board[2][2] != EMPTY:
        return board[0][0]
    if board[0][2] == board[1][1] == board[2][0] != EMPTY:
        return board[0][2]

    return None

@bot.hybrid_command(description="Kick a user from the server")
@commands.has_permissions(kick_members=True)
async def kick(ctx, member: discord.Member, *, reason="No reason provided"):
    if not ctx.guild:
        await ctx.send("This command can only be used in a server!")
        return

    if not ctx.guild.me.guild_permissions.kick_members:
        await ctx.send("I don't have permission to kick members!")
        return

    if ctx.author == member:
        await ctx.send("You cannot kick yourself!")
        return

    if ctx.author.top_role <= member.top_role:
        await ctx.send("You cannot kick someone with a higher or equal role!")
        return

    try:
        await member.kick(reason=reason)
        embed = discord.Embed(
            title="Member Kicked",
            description=f"{member.mention} has been kicked by {ctx.author.mention}",
            color=discord.Color.red()
        )
        embed.add_field(name="Reason", value=reason, inline=False)
        await ctx.send(embed=embed)
    except discord.Forbidden:
        await ctx.send("I don't have permission to kick this member!")
    except Exception as e:
        await ctx.send(f"An error occurred: {e}")

@bot.hybrid_command(description="Get inspirational quote")
async def inspire(ctx):
    await ctx.send(get_quote())

@bot.hybrid_command(description="Add new encouragement")
async def add(ctx, *, message: str):
    update_encouragements(message)
    await ctx.send(f"Added new encouragement: {message}")

@bot.hybrid_command(description="List all encouragements")
async def list(ctx):
    encouragements = db["encouragements"] if "encouragements" in db.keys() else starter_encouragements.copy()
    await ctx.send("Current encouragements:\n" + "\n".join(f"{i}. {msg}" for i, msg in enumerate(encouragements)))

@bot.hybrid_command(description="Delete encouragement by index")
async def delete(ctx, index: int):
    delete_encouragement(index)
    await ctx.send(f"Removed encouragement at index {index}")

@bot.hybrid_command(description="Toggle auto-responses")
async def toggle(ctx):
    db["responding"] = not db["responding"]
    await ctx.send(f"Auto-responses {'enabled' if db['responding'] else 'disabled'}")

@bot.hybrid_command(description="Sync commands")
async def sync(ctx):
    if ctx.author.id == ctx.guild.owner_id:
        await bot.tree.sync()
        await ctx.send("Commands synced!")
    else:
        await ctx.send("Only server owner can sync commands")

@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if isinstance(message.channel, discord.DMChannel) or ("responding" in db.keys() and db["responding"]):
        if any(word in message.content.lower() for word in sad_words):
            encouragements = db["encouragements"] if "encouragements" in db.keys() else starter_encouragements.copy()
            await message.channel.send(random.choice(encouragements))

    await bot.process_commands(message)

keep_alive()
bot.run(os.getenv('TOKEN'))
