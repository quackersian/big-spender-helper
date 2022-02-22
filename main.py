import logging, disnake, config, tokens
from disnake.ext import commands

#TODO: Replace this with the one below once your code is live. Once live, changes to commands can take up to 1 hour to sync.
bot = commands.Bot(test_guilds = [config.test_guild_id])
#bot = commands.Bot()


#sets up logging using the standard logging library. Configure the level in the config.py file.
def setup_logging():
    try:
        logging.basicConfig(
            format = "%(asctime)s %(levelname)-8s %(message)s",
            filename='bot.log',
            encoding='utf-8',
            filemode='w',
            level = config.logging_level,
            datefmt="%Y-%m-%d %H:%M:%S")
        logging.info("-----------")
        print('Setup logging correctly.')

    except Exception as e:
        print(f"ERROR - failed to setup logging - {e}") 



#Alerts once the bot is ready to receive commands
@bot.event
async def on_ready():
    print(f"{config.bot_name} ready")




#An example slash command, will respond World when you use /hello
@bot.slash_command(description = "Responds with 'World'")
async def hello(inter):

    await inter.send("World")
    
    

@bot.slash_command(description = "Adds/removes a role.")
async def roles(inter, role: disnake.Role, remove: bool):

    if remove == True:
    #the member wants to remove the role

        logging.info(f"{inter.author} tried to remove {role} role.")

        try:
            await inter.author.remove_roles(role, reason = "Removed via slash command", atomic = False)
            logging.info(f"Succesfully removed {role} role from {inter.author}.")
            await inter.send(f"Succesfully removed {role} role.")
            
        
        except disnake.errors.Forbidden as e:
            #bot didn't have sufficient permissions to remove role.
            logging.exception(f"Could not remove {role} from {inter.author}, invalid permissions.")
            await inter.send("This action failed, please try again.")
        
        except Exception as e:
            #generic error
            logging.exception(f"Could not remove {role} from {inter.author}. {e}")
            await inter.send("This action failed, please try again.")


    elif remove == False:
    #the member wants to add the role

        logging.info(f"{inter.author} tried to add {role} role.")
        
        try:
            await inter.author.add_roles(role, reason = "Added via slash command", atomic = False)
            logging.info(f"Succesfully added {role} role from {inter.author}.")
            await inter.send(f"Succesfully added {role} role.")
            
        
        except disnake.errors.Forbidden as e:
            #bot didn't have sufficient permissions to add role.
            logging.exception(f"Could not add {role} from {inter.author}, invalid permissions.")
            await inter.send("This action failed, please try again.")
        
        except Exception as e:
            #generic error
            logging.exception(f"Could not add {role} from {inter.author}. {e}.")
            await inter.send("This action failed, please try again.")



if __name__ == "__main__":
    setup_logging()
    bot.run(tokens.live_token)
