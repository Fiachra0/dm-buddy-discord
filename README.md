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

# Create Character
!create char [char_type]
- [real]:   Rolls 3d6 for 6 stats
- [cali]:   Rolls 3d6 for 7 stats, drop the lowest one. DOES NOT SUPPORT STRICT
- [std]:    Rolls 4d6 for 6 stats and drops the lowest dice on each roll
- [amfat]:  Rolls 4d6 for 7 stats and drops the lowest dice on each roll. Drop lowest stat. DOES NOT SUPPORT STRICT
- [rise]:   Rolls 3d6-1 for 6 stats. Proceed to drop 2 from any choice.
- [hero]:   Rolls 4d6+1 for primary stat. Then rolls 3d6-1 for the rest. NOTE: Supports Flexible only. e.g. !create char_type hero str

