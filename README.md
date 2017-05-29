# Discord-Dice Roller
A bot that handles most RPG dice rolls

# Dependencies
This bot is extended from [Discord.py] (https://github.com/Rapptz/discord.py/). Install Discord.py prior to running this bot.

#Python Version
This requires Python 3.4.1+. If you are using Python 3.5:

Replace `async def` instead of `@asyncio.corouting` and `await` instead of `yield from`

# Usage
1. Follow the directions [here] (https://github.com/reactiflux/discord-irc/wiki/Creating-a-discord-bot-&-getting-a-token) to create a bot token.
2. Add the bot to the servers you want.
3. Place the token in the last line of the script.
4. Launch script.

# Commands
`!purge`
Deletes all messages made from the bot. Used to clean up after a session.

`!roll`
Supported rolls are:
- !roll 100 - Rolls from 1-100
- !roll 50-100 - Rolls from 50-100
- !roll 3d6 - Rolls 3 6-sided die

#Modifiers
- `+` Modifier. Used with any roll. Adds or subtracts from the roll. !roll 100mod4 will add 4 to the roll.

#Create Character
!create char [char_type]

