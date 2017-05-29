# A dice rolling bot for use on Discord servers
# LICENSE: This work is licensed under a Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License.
# @category   Tools
# @copyright  Copyright (c) 2016 Robert Thayer (http://www.gamergadgets.net)
# @version    1.1
# @link       http://www.gamergadgets.net
# @author     Jon Rankin, Robert Thayer

# from random import randint
import random
from random import randint
import discord as discord # Imported from https://github.com/Rapptz/discord.py
import asyncio
from discord.ext import commands

#CONSTANTS
stat_type = ['STR','DEX','CON','INT','WIS','CHA']

# A dice bot for use with Discord
bot = discord.Client()
bot = commands.Bot(command_prefix='!', description="A bot to handle all your RPG rolling needs")

# Determines if a message is owned by the bot
def is_me(m):
    return m.author == bot.user

# Determines if the value can be converted to an integer
# Parameters: s - input string
# Returns: boolean. True if can be converted, False if it throws an error.
def is_num(s):
    try:
        int(s)
        return True
    except ValueError:
        return False

# Roll die and get a random number between a and b (inclusive) adding/subtracting the modifier
# Parameters: a [low number], b [high number], modifier [amount to add/subtract to total]
# threshold [number that result needs to match or exceed to count as a success]
# Returns: str 
def roll_basic(a, b, modifier, threshold):
    results = ""
    base = randint(int(a), int(b))
    if (base + modifier) >= threshold:
        if modifier != 0:
            if modifier > 0:
                results += "***{}+{} [{}]***".format(base, modifier, (base + modifier))
            else:
                results += "***{}+{} [{}]***".format(base, modifier, (base + modifier))
        else:
            results += "***{}***".format(base)
    else:
        if modifier != 0:
            if modifier > 0:
                results += "***Failure***: {}+{} [{}]".format(base, modifier, (base + modifier))
            else:
                results += "***Failure***: {}{} [{}]".format(base, modifier, (base + modifier))
        else:
            results += "***Failure***: {}".format(base)
    return results

# Rolls a set of die and returns either number of hits or the total amount
# Parameters: num_of_dice [Number of dice to roll], dice_type[die type (e.g. d8, d6), 
# hit [number that must be exceeded to count as a success], modifier [amount to add to/subtract from total],
# threshold [number of successes needed to be a win]
# Returns: String with results 
def roll_hit(num_of_dice, dice_type, hit, modifier, threshold):
    results = ""
    total = 0
    for x in range(0, int(num_of_dice)):
        y = randint(1, int(dice_type))
        if (int(hit) > 0):
            if (y >= int(hit)):
                results += "{}+".format(y)
                total += 1
            else:
                results += "{}+".format(y)
        else:
            results += "{}+".format(y)
            total += y
    results = results[:-1]
    total += int(modifier)
    if modifier != 0:
        if modifier > 0:
            results += "+{} = **{}**".format(modifier, total)
        else:
            results += "{} = **{}**".format(modifier, total)
    else:
        results += "= {}".format(total)
    if threshold != 0:
        if total >= threshold:
            results += " meets or beats the {} threshold. ***Success***".format(threshold)
        else:
            results += " does not meet the {} threshold. ***Failure***".format(threshold)
    return results

# Determines the style of character creation. Default is standard 4d6 drop 1 x 6
def create_character(number_of_stats=6, number_of_dice=4, dropped_die=1, flex=1, modifier=0 ):

    results = ""
    for x in range(0, number_of_stats):
        z = [random.randint(1,6) for _ in range(number_of_dice)]
        print(z)
        for y in range(0, dropped_die):
             z.remove(min(z))
        stat = (sum(z))+modifier
        if (flex):
           results += "{}, ".format(stat)
        else:
           results += "{}: {}, ".format(stat_type[x],stat)
    return results[:-2]


@bot.event
@asyncio.coroutine 
def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')

# Parse !roll verbiage
@bot.command(pass_context=True,description='Rolls dice.\nExamples:\n100  Rolls 1-100.\n50-100  Rolls 50-100.\n3d6  Rolls 3 d6 dice and returns total.\nModifiers:\n! Hit success. 3d6!5 Counts number of rolls that are greater than 5.\nmod: Modifier. 3d6mod3 or 3d6mod-3. Adds 3 to the result.\n> Threshold. 100>30 returns success if roll is greater than or equal to 30.\n\nFormatting:\nMust be done in order.\nSingle die roll: 1-100mod2>30\nMultiple: 5d6!4mod-2>2')
@asyncio.coroutine
def roll(ctx, roll : str):
    a, b, modifier, hit, num_of_dice, threshold, dice_type = 0, 0, 0, 0, 0, 0, 0
    # author: Writer of discord message
    author = ctx.message.author
    if (roll.find('>') != -1):
        roll, threshold = roll.split('>')
    if (roll.find('+') != -1):
        roll, modifier = roll.split('+')
    #if (roll.find('!') != -1):
    #    roll, hit = roll.split('!')
    if (roll.find('d') != -1):
        num_of_dice, dice_type = roll.split('d')
    elif (roll.find('-') != -1):
        a, b = roll.split('-')
    else:
        a = 1
        b = roll
    #Validate data
    try:
        if (modifier != 0):
            if (is_num(modifier) is False):
                raise ValueError("Modifier value format error. Proper usage 1d4+1")
                return
            else:
                modifier = int(modifier)
        if (hit != 0):
            if (is_num(hit) is False):
                raise ValueError("Hit value format error. Proper usage 3d6!5")
                return
            else:
                hit = int(hit)
        if (num_of_dice != 0):
            if (is_num(num_of_dice) is False):
                raise ValueError("Number of dice format error. Proper usage 3d6")
                return
            else:
                num_of_dice = int(num_of_dice)
        if (num_of_dice > 200):
            raise ValueError("Too many dice. Please limit to 200 or less.")
            return
        if (dice_type != 0):
            if (is_num(dice_type) is False):
                raise ValueError("Dice type format error. Proper usage 3d6")
                return
            else:
                dice_type = int(dice_type)
        if (a != 0):
            if (is_num(a) is False):
                raise ValueError("Error: Minimum must be a number. Proper usage 1-50.")
                return
            else:
                a = int(a)
        if (b != 0):
            if (is_num(b) is False):
                raise ValueError("Error: Maximum must be a number. Proper usage 1-50 or 50.")
                return
            else:
                b = int(b)
        if (threshold != 0):
            if (is_num(threshold) is False):
                raise ValueError("Error: Threshold must be a number. Proper usage 1-100>30")
                return
            else:
                threshold = int(threshold)
        if (dice_type != 0 and hit != 0):
            if (hit > dice_type):
                raise ValueError("Error: Hit value cannot be greater than dice type")
                return
            elif (dice_type < 0):
                raise ValueError("Dice type cannot be a negative number.")
                return
            elif (num_of_dice < 0):
                raise ValueError("Number of dice cannot be a negative number.")
                return
        if a != 0 and b != 0:
            yield from bot.say("**{}** rolls 1d{}. Result: {}".format(author, b, roll_basic(a, b, modifier, threshold)))
        else:
            yield from bot.say("**{}** rolls {}d{}. Results: {}".format(author, num_of_dice, dice_type, roll_hit(num_of_dice, dice_type, hit, modifier, threshold)))
        yield from bot.delete_message(ctx.message)
    except ValueError as err:
        # Display error message to channel
        yield from bot.say(err)

#Bot command to delete all messages the bot has made.        
@bot.command(pass_context=True,description='Deletes all messages the bot has made')
@asyncio.coroutine
def purge(ctx):
    channel = ctx.message.channel
    deleted = yield from bot.purge_from(channel, limit=100, check=is_me)
    yield from bot.send_message(channel, 'Deleted {} message(s)'.format(len(deleted)))


#Bot command to create a new character
@bot.group(pass_context=True,description='Rolls for new character stats')
@asyncio.coroutine
def create(ctx):
    if ctx.invoked_subcommand is None:
        #display the character to the channel
        channel = ctx.message.channel
        author = ctx.message.author 
        yield from bot.send_message(channel, """```Markdown
#{} created a 'Standard' character
[Stats]: {}
```""".format(author, create_character()))
        yield from bot.delete_message(ctx.message)

#sub command for char_type
@create.command(pass_context=True)
@asyncio.coroutine
def char(ctx, type : str='standard', flex :str ='flex'):
	try:
		if ((type=='cali' or type=='amfat') and flex=='strict'):
			raise ValueError("Strict not supported with this character stat template")
		elif (type=='real'):
			type, number_of_stats, number_of_dice, dropped_die, modifier = 'Realistic',6,3,0,0
		elif (type=='cali'):
			type, number_of_stats, number_of_dice, dropped_die, modifier = 'Californian',7,3,0,0
		elif (type=='std'):
			type, number_of_stats, number_of_dice, dropped_die, modifier = 'Standard',6,4,1,0
		elif (type=='amfat'):
                        type, number_of_stats, number_of_dice, dropped_die, modifier = 'American Fatcat',7,4,1,0
		elif (type=='rise'):
			type, number_of_stats, number_of_dice, dropped_die, modifier = 'Rise up',6,3,0,-1
		elif (type=='hero'):
			if flex.upper() not in stat_type:
				raise ValueError("Please Specify the correct stat")
				return
			yield from bot.say("""```Markdown
#{} created a True Hero
{}: {}
Other Stats: {}
```""".format(ctx.message.author,flex.upper(), create_character(1,4,1,1,1), create_character(5,3,0,1,-1)))
			yield from bot.delete_message(ctx.message)
		else:
			raise ValueError("Incorrect roll template. Please use '!create help' for options")
			return
		if (flex=='flex'):
			flex=1
		elif (flex=='strict'):
			flex=0
		elif (flex.upper() in stat_type):
			return
		else:
			raise ValueError("Incorrect Parameter. Please use either 'strict' or 'flex' for stat assignment.")
			return
	except ValueError as err:
		#display error
		yield from bot.say(err)
		return
	yield from bot.say("""```Markdown
#{} created a '{}' style character
[Stats]: {}
```""".format(ctx.message.author, type, create_character(number_of_stats, number_of_dice, dropped_die, flex, modifier)))
	yield from bot.delete_message(ctx.message)

@create.command(pass_context=True)
@asyncio.coroutine
def help(ctx):
	yield from bot.say("""```Markdown
# Creating a character

Creates a Standard Character  by rolling 4d6 and dropping the lowest die for 6 stats.
Can use the [char] sub-command to customize. usage !create char_type [StyleOfChar] [StatAssignment].

Style of Character Options(optional):
[real]:   Rolls 3d6 for 6 stats
[cali]:   Rolls 3d6 for 7 stats, drop the lowest one. DOES NOT SUPPORT STRICT
[std]:    Rolls 4d6 for 6 stats and drops the lowest dice on each roll
[amfat]:  Rolls 4d6 for 7 stats and drops the lowest dice on each roll. Drop lowest stat. DOES NOT SUPPORT STRICT
[rise]:   Rolls 3d6-1 for 6 stats. Proceed to drop 2 from any choice.
[hero]:   Rolls 4d6+1 for primary stat. Then rolls 3d6-1 for the rest. NOTE: Supports Flexible only. e.g. !create char_type hero str

Stat Assignment (optional)
[flex]:   Flexible Stat Assignment*
[strict]: Strict Stat Assignment, Assigns each stat in order*
```""")
	yield from bot.delete_message(ctx.message)


# Follow this helpful guide on creating a bot and adding it to your server.
# https://github.com/reactiflux/discord-irc/wiki/Creating-a-discord-bot-&-getting-a-token
bot.run('Mjk2Mjc0Njc5NTg3NDA1ODI0.C7v4Bw.rYaj0X5fqRI1kWrW5tHmV620WnE')
