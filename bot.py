import asyncio
import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
import main

true_emoji = "✅"
false_emoji = "❌"

load_dotenv()
TOKEN = os.getenv("DISCORD_TOKEN")

bot = commands.Bot(command_prefix=commands.when_mentioned_or("!"))

def check_if_it_is_me(ctx):
  return bot.is_owner(ctx.message.author)

@bot.event
async def on_ready():
  game = discord.Game("call me with !florida")
  await bot.change_presence(status=discord.Status.idle, activity=game)

  print(f'{bot.user} has connected to Discord!')

@commands.cooldown(1, 30, commands.BucketType.channel)
@bot.command(name="florida", help="HIT ME!")
async def florida(ctx):
  (response, is_real) = main.main()
  # if is_real:
  #   await asyncio.sleep(3)  # real messages are too quick versus generation
  message = await ctx.send(f"Real {true_emoji} or fake {false_emoji} ? Vote for what you think! \n{response}")
  await message.add_reaction(true_emoji)
  await message.add_reaction(false_emoji)
  correct_emoji = true_emoji if is_real else false_emoji
  await asyncio.sleep(30)
  print("timer done, checking reacts")
  message = await ctx.channel.fetch_message(message.id)
  correct_users = set()
  incorrect_users = set()
  for reaction in [reaction for reaction in message.reactions if reaction.emoji in [true_emoji, false_emoji]]:
    async for user in reaction.users():
      if (user != bot.user) and (user not in incorrect_users):
        user_correct = reaction.emoji == correct_emoji
        if user_correct:
          correct_users.add(user)
        else:
          if user in correct_users:
            correct_users.remove(user)
          incorrect_users.add(user)
        print(f'{user} has reacted with {reaction.emoji}!')
  if len(correct_users) == 0:
    result_msg = f"No one got it correct! The answer was: {correct_emoji} ."
  else:
    result_msg = f"The answer was: {correct_emoji} , congrats {' '.join([user.mention for user in correct_users])}"
  await ctx.send(result_msg)

@bot.command(name="bye")
@commands.check(check_if_it_is_me)
async def bye(ctx):
  await ctx.guild.leave()

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.errors.CheckFailure):
        await ctx.send('You do not have the correct role for this command.')
    else:
      print(ctx, error)

bot.run(TOKEN)
