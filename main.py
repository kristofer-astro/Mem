import nextcord
from nextcord import Intents
from nextcord.ext import commands
from dataclasses import dataclass
from bot_token import TOKEN
import gacha


# BOT SETUP
intents = Intents.default()
intents.message_content = True
mem = commands.Bot(command_prefix=">", intents=intents)


# MAIN BOT FUNCTIONALITY
mem.remove_command('help')

# Ping Command
@mem.slash_command(name='ping')
async def ping(interaction: nextcord.Interaction):
    await interaction.response.send_message(f'Mem! :ping_pong:: {round(mem.latency * 1000)} ms ')

# Help Command
@mem.slash_command(name='help', description='List of commands')
async def help(interaction: nextcord.Interaction):

    help_embed = nextcord.Embed(
        title='Hi~!! Mem-chan here >w<',
        description='Mem-chan is a HSR discord bot!',
        colour=nextcord.Colour.from_rgb(230, 150, 230)
    )

    help_embed.add_field(name=':wrench: Utility Commands', value='`/help` - Displays this message \n'
                                                                 '`/ping` - Returns the latency of the bot',
                         inline=False)
    help_embed.add_field(name=':slot_machine: Gacha Commands', value='`/pull` - Do a single pull \n'
                                                                '`/multipull` - Do 10 pulls',
                         inline=False)
    help_embed.add_field(name=':bulb: More Features Coming Soon!', value='', inline=False)

    await interaction.response.send_message(embed=help_embed)


# GLOBAL STATS
class GachaState:
    four_pity: int = 0
    five_pity: int = 0
    four_guaranteed: bool = False
    five_guaranteed: bool = False

g = GachaState()

# Pull Command
@mem.slash_command(name='pull', description='Do a single pull')
async def pull(interaction: nextcord.Interaction):

    p = gacha.pull(g.four_pity, g.five_pity, ['Pela', 'Lynx', 'Gallagher'], 'Castorice', g.four_guaranteed, g.five_guaranteed)
    rgb = [224, 181, 70] if p[1] == 5 else [175, 89, 212] if p[1] == 4 else [89, 153, 212]

    g.four_pity, g.five_pity, g.four_guaranteed, g.five_guaranteed = p[2], p[3], p[4],p[5]

    pull_outcome = nextcord.Embed(
        title='Pull Result',
        description=f'4* PITY: {p[2]}/10 | 50/50? {'NO' if p[4] else 'YES'}\n'
                    f'5* PITY: {p[3]}/90 | 50/50? {'NO' if p[5] else 'YES'}',
        colour=nextcord.Colour.from_rgb(rgb[0], rgb[1], rgb[2])
    )

    pull_outcome.add_field(
        name=f'PITY {p[3] - 1}',
        value=f'{':star:' * p[1]} | {p[0]}',
        inline=False
    )

    await interaction.response.send_message(embed=pull_outcome)

# 10-PullCommand
@mem.slash_command(name='multipull', description='Do 10 pulls')
async def multipull(interaction: nextcord.Interaction):

    pulls = [None for _ in range(10)]

    for i in range(10):
        outcome = gacha.pull(g.four_pity, g.five_pity, ['Pela', 'Lynx', 'Gallagher'], 'Castorice', g.four_guaranteed, g.five_guaranteed)
        pulls[i] = outcome
        g.four_pity, g.five_pity, g.four_guaranteed, g.five_guaranteed = outcome[2], outcome[3], outcome[4], outcome[5]

    rgb = [89, 153, 212]

    for pull in pulls:
        if pull[1] == 4:
            rgb = [175, 89, 212]
        elif pull[1] == 5:
            rgb = [224, 181, 70]
            break


    pull_outcome = nextcord.Embed(
        title='Pull Result',
        description=f'4* PITY: {pulls[9][2]}/10 | 50/50? {'NO' if pulls[9][4] else 'YES'}\n'
                    f'5* PITY: {pulls[9][3]}/90 | 50/50? {'NO' if pulls[9][5] else 'YES'}',
        colour=nextcord.Colour.from_rgb(rgb[0], rgb[1], rgb[2])
    )

    for i in range(len(pulls)):
        pull_outcome.add_field(
            name=f'PITY {pulls[i][3]-1}',
            value=f'{':star:' * pulls[i][1]} | {pulls[i][0]}',
            inline=False
        )

    await interaction.response.send_message(embed=pull_outcome)

'''
=================================================== WORDLE GAME ========================================================
'''
#
# logo = 'https://static01.nyt.com/images/2022/03/02/crosswords/alpha-wordle-icon-new/alpha-wordle-icon-new-square320-v3.png'
#
# @mem.slash_command(name='tutorial', description='Wordle rules and how to play!')
# async def tutorial(interaction: nextcord.Interaction):
#     tuto_embed = nextcord.Embed(
#         title='Welcome to Wordle!',
#         color=nextcord.Color.brand_green()
#     )
#
#     tuto_embed.add_field(name=':question: What is Wordle?',
#                          value='Wordle is a *word-based puzzle game* that asks you to guess a 5-letter word. You are '
#                                'given **6 attempts** to guess the mystery word!\n\nThere will also be clues that will '
#                                'guide you through the puzzle!\n\n',
#                          inline=False)
#
#     tuto_embed.add_field(name=':question: What do the colors of the blocks mean?',
#                          value='🟩 A green block means that the current letter of the word is **CORRECT** and'
#                                'is in the **RIGHT** position!\n\n🟨 A yellow block means that the current'
#                                'letter **EXISTS** within the word, it\'s just *not in the right* position!\n\n'
#                                '⬜ A white block means that the current letter does **NOT** exist within'
#                                'the word.\n\n',
#                          inline=False)
#     tuto_embed.add_field(name=':bulb: More info regarding duplicate letters',
#                          value='At times, there might be words that have duplicate letters; e.g "TEETH" and "AORTA"\n\n'
#                                'Worry not! as Wordle do take account of the letter counts in the words. This means that'
#                                'if say the mystery word is "TEETH", and you inputted "EATEN" as a guess, then both E\'s'
#                                'will be highlighted yellow, indicating that there are 2 E\'s in the mystery word.\n\n'
#                                'It works the other way around, too! e.g Inputting "MELEE" as a guess for "SPEED" will'
#                                'have the first 2 E\'s highlighted, ignoring the third E in MELEE.',
#                          inline=False)
#     tuto_embed.set_thumbnail(url=logo)
#
#     await interaction.response.send_message(embed=tuto_embed)
#
# # initializing global variables
# player = ''
# game_over = True
# is_solved = False
# wordle_embed = nextcord.Embed(title='Wordle', color=nextcord.Color.green())
# wordle_embed.set_thumbnail(url=logo)
# attempts = 0
# white = ':white_large_square:'
# green = ':green_square:'
# yellow = ':yellow_square:'
# mystery_word = ''


# @mem.slash_command(name='wordle', description='Play Wordle game on Discord!', dm_permission=True)
# async def wordle(interaction: nextcord.Interaction):
#     embed = nextcord.Embed(
#         title='test title',
#         description='this is the description',
#         color=nextcord.Colour.green()
#     )
#
#     global player, game_over, attempts, mystery_word
#
#     if game_over:
#         global printable
#         game_over = False
#         player = interaction.user
#         attempts = 0
#
#         # Pick random word from all possible wordle answers
#         mystery_word = wordle_answers[randrange(0, len(wordle_answers))]
#
#         await interaction.response.send_message(f'Please enter a 5-letter word, {player.mention}!\n'
#                                                 f'Type `>input (word)` !!')
#
#     else:
#         await interaction.response.send_message('A game is currently in progress!')
#
#
#
# @mem.command(name='input')
# async def wordle_input(ctx, guess : str):
#     global player, game_over, wordle_embed, attempts, mystery_word, white, green, yellow, is_solved
#
#     # checks if a game is currently running or not
#     if not game_over:
#
#         # ensures that the game is unique for each player
#         if player == ctx.author:
#
#             # CHECK FOR INPUT VALIDATION
#             error_msg = ''
#             guess = guess.strip().lower()
#
#             if guess not in wordle_possible:
#                 error_msg += 'Invalid word. '
#
#             if len(guess) != 5:
#                 error_msg += 'Word must be 5 characters long. '
#
#             if error_msg != '':
#                 await ctx.send(error_msg + 'Try again!')
#
#             # IF INPUT IS VALID, STARTS AN ATTEMPT
#             if len(guess) == 5 and guess in wordle_possible:
#                 attempts += 1
#                 # await ctx.send(f'Your input "{guess}" is VALID !')
#                 await ctx.send(f'**Attempt {attempts} / 6**')
#
#                 attempt_printable = (f'`{guess[0].upper()}  {guess[1].upper()}  {guess[2].upper()}  '
#                                      f'{guess[3].upper()}  {guess[4].upper()}`') # String to store current guess word
#                 green_list = []
#                 block_printable = ''
#                 correct_letters = 0
#
#                 guess_count = {letter: guess.count(letter) for letter in guess}
#                 mystery_count = {letter: mystery_word.count(letter) for letter in mystery_word}
#
#                 # MAIN WORDLE GAME
#                 for index in range(len(guess)):
#                     # Green tile
#                     if guess[index] == mystery_word[index]:
#                         correct_letters += 1
#                         block_printable += green
#
#                         # updating the letter count
#                         green_list.append(guess[index])
#                         guess_count[guess[index]] -= 1
#                         mystery_count[mystery_word[index]] -= 1
#
#                     # Yellow tile
#                     elif guess[index] in mystery_word and guess[index] != mystery_word[index]:
#                         green_tileable = False
#
#                         # this for loop prioritizes green tile over yellow tile
#                         for j in range(5):
#                             if guess[j] == mystery_word[j] and guess[j] == guess[index]:
#                                 green_tileable = True
#
#                         if green_tileable and (guess[index] not in green_list) and mystery_count[
#                             guess[index]] == 1:
#                             block_printable += white
#                             guess_count[guess[index]] -= 1
#
#                         else:
#                             # this if statement ensures the case of duplicate letters in the mystery word
#                             if mystery_count[guess[index]] > 0 and guess_count[guess[index]] > 0:
#                                 block_printable += yellow
#
#                                 # updating the letter count
#                                 guess_count[guess[index]] -= 1
#                                 mystery_count[guess[index]] -= 1
#
#                             else:
#                                 block_printable += white
#
#                                 # updating the letter count
#                                 guess_count[guess[index]] -= 1
#
#                     # White tile
#                     else:
#                         block_printable += white
#
#                         # updating the letter count, ONLY the guess letter count is updated SINCE the guess letter is NOT in the mystery word
#                         guess_count[guess[index]] -= 1
#
#                     if correct_letters == 5:
#                         is_solved = True
#
#
#                 # PRINTING THE MAIN OUTPUT
#                 wordle_embed.add_field(name='', value=f'{attempt_printable}\n{block_printable}\n',inline=False)
#                 wordle_embed.set_footer(text=f'{"❤️" * (6 - attempts)}')
#                 await ctx.send(embed=wordle_embed)
#
#
#                 # CHECKS IF PUZZLE IS SOLVED OR USER FINISHES THEIR 6TH ATTEMPT BUT NOT SOLVED -> ENDS THE GAME
#                 if is_solved:
#                     await ctx.send('Congratulations!! 🎉🎉🎉 You have guessed the right word 🙂')
#                     game_over = True
#                     wordle_embed.clear_fields()
#                     attempts = 0
#
#                 if attempts == 6 and not is_solved:
#                     await ctx.send(f'The correct answer is {mystery_word}!')
#                     game_over = True
#                     wordle_embed.clear_fields()
#                     attempts = 0
#
#         else:
#             await ctx.send('Please start a new Wordle game using `/wordle` !')
#     else:
#         await ctx.send('Please start a new Wordle game using `/wordle` !')
#
#
# @mem.command(name='exit')
# async def exit_game(ctx):
#     global game_over, wordle_embed, attempts, mystery_word
#
#     if not game_over:
#         game_over = True
#         wordle_embed.clear_fields()
#         attempts = 0
#
#         await ctx.send(f'You have forcibly end the game! The answer is {mystery_word}!')
#     else:
#         await ctx.send('There is no game currently running!')
#
# '''
# =================================================== WORDLE GAME ========================================================
# '''


# BOT STARTUP
@mem.event
async def on_ready() -> None:
    print(f'{mem.user.name} is online!')

# LOGGING INCOMING MESSAGES
'''
@bot.event
async def on_message(message) -> None:
    if message.author == bot.user:
        return

    print(f'[{message.channel}] {message.author}: "{message.content}"')
'''

# MAIN ENTRY POINT
mem.run(token=TOKEN)