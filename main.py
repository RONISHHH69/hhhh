import os
os.system('pip install discord.py==1.7.3 requests')
import discord
from discord.ext import commands
import json

os.system('cls' if os.name == 'nt' else 'clear')

infected = 'token'
PREFIX = ''

intents = discord.Intents.default()

auto_messages = {}

def load_autoresponder_data():
    try:
        with open('autoresponder_data.json', 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return {}


def save_autoresponder_data(data):
    with open('autoresponder_data.json', 'w') as file:
        json.dump(data, file)

bot = commands.Bot(command_prefix=PREFIX, help_command=None, self_bot=True, intents=intents)  

c2i_value = 88
i2c_value = 91      
        
@bot.event
async def on_ready():
    print(f"{'='*30}")
    print(f"        Logged in as: {bot.user.name}")
    print(f"        User ID: {bot.user.id}")
    print(f"{'='*30}\n")
    print("I N F E C T E D x 7")
    print(f"{'-'*30}")
    print(f"   Username: {bot.user.name}")
    print(f"   Guilds: {len(bot.guilds)}")
    print(f"   Members: {sum([guild.member_count for guild in bot.guilds])}")
    print(f"{'-'*30}")
    print("I N F E C T E D")        

@bot.command(aliases=['h'])
async def help(ctx):
    command_list = bot.commands
    sorted_commands = sorted(command_list, key=lambda x: x.name)

    response = "**D R U G S**\n\n"
    for command in sorted_commands:
        response += f"_{command.name}_, "

    await ctx.send(response)
    await ctx.message.delete()
    
@bot.command()
async def addar(ctx, trigger, *, response):
    autoresponder_data = load_autoresponder_data()
    autoresponder_data[trigger] = response
    save_autoresponder_data(autoresponder_data)
    await ctx.send(f'Autoresponder added: `{trigger}` -> `{response}`')
    await ctx.message.delete()

@bot.command()
async def delar(ctx, trigger):
    autoresponder_data = load_autoresponder_data()
    if trigger in autoresponder_data:
        del autoresponder_data[trigger]
        save_autoresponder_data(autoresponder_data)
        await ctx.send(f'Autoresponder removed: `{trigger}`')
    else:
        await ctx.send('Autoresponder not found.')
    await ctx.message.delete()    

@bot.command()
async def listar(ctx):
    autoresponder_data = load_autoresponder_data()
    if autoresponder_data:
        response = 'ARs LIST\n'
        for trigger, response_text in autoresponder_data.items():
            response += f'`{trigger}` -> `{response_text}`\n'
        await ctx.send(response)
    else:
        await ctx.send('No ARs found')
        
    await ctx.message.delete()    

@bot.command(aliases=['cltc'])
async def ltcprice(ctx):
    url = 'https://api.coingecko.com/api/v3/coins/litecoin'
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()
        price = data['market_data']['current_price']['usd']
        await ctx.send(f"The current price of Litecoin (LTC) is ${price:.2f}")
    else:
        await ctx.send("Failed to fetch Litecoin price")
    await ctx.message.delete() 

@bot.command(aliases=['bal', 'ltcbal'])
async def getbal(ctx, ltcaddress):
    
    
    response = requests.get(f'https://api.blockcypher.com/v1/ltc/main/addrs/{ltcaddress}/balance')
    if response.status_code == 200:
        data = response.json()
        balance = data['balance'] / 10**8  
        total_balance = data['total_received'] / 10**8
        unconfirmed_balance = data['unconfirmed_balance'] / 10**8
    else:
        await ctx.send("Failed to retrieve balance. Please check the Litecoin address.")
        return

    
    cg_response = requests.get('https://api.coingecko.com/api/v3/simple/price?ids=litecoin&vs_currencies=usd')
    if cg_response.status_code == 200:
        usd_price = cg_response.json()['litecoin']['usd']
    else:
        await ctx.send("Failed to retrieve the current price of Litecoin.")
        return
    
    
    usd_balance = balance * usd_price
    usd_total_balance = total_balance * usd_price
    usd_unconfirmed_balance = unconfirmed_balance * usd_price
    
    
    message = f"LTC Address: `{ltcaddress}`\n"
    message += f"Current LTC: **${usd_balance:.2f} USD**\n"
    message += f"Total LTC Received: **${usd_total_balance:.2f} USD**\n"
    message += f"Unconfirmed LTC: **${usd_unconfirmed_balance:.2f} USD**"
    
    
    response_message = await ctx.send(message)
    await ctx.message.delete()
    
@bot.command()
async def vc2i(ctx, *, c2i):
    author_id = ctx.author.id
    await ctx.message.delete()
    await ctx.send(f'+rep {author_id} EXCHANGE • [{c2i}] LTC TO GOOGLE PAY UPI')

@bot.command()
async def vi2c(ctx, *, i2c):
    author_id = ctx.author.id
    await ctx.message.delete()
    await ctx.send(f'+rep {author_id} EXCHANGE • [{i2c}] GOOGLE PAY UPI TO LTC') 

@bot.command()
async def seti2c(ctx, new_value: float):
    global i2c_value
    i2c_value = new_value
    await ctx.message.delete()
    await ctx.send(f'i2c value has been updated to {new_value}')
        
@bot.command()
async def i2c(ctx, amount: float, currency: str):
    await ctx.message.delete()
    if currency == '₹':
        result = amount / i2c_value
        await ctx.send(f'**I2C** for **__₹{amount}__** \n ~ ${result}')
    elif currency == '$':
        result = amount * i2c_value
        await ctx.send(f'** I2C** for **__${amount}__** \n ~ ₹{result}')
    else:
        await ctx.send('`.i2c amt$/₹`')       

@bot.command()
async def setc2i(ctx, new_value: float):
    global c2i_value
    c2i_value = new_value
    await ctx.message.delete()
    await ctx.send(f'c2i value has been updated to {new_value}')

@bot.command()
async def c2i(ctx, amount: float, currency: str):
    await ctx.message.delete()
    if currency == '₹':
        result = amount / c2i_value
        await ctx.send(f'**C2I** for **__₹{amount}__**\n ~ ${result}')
    elif currency == '$':
        result = amount * c2i_value
        await ctx.send(f'**C2I** for **__${amount}__** \n ~ ₹{result}')
    else:
        await ctx.send('`.c2i amt$/₹`')       
    
@bot.event
async def on_message(message):
    if message.author != bot.user:
        return
      
    autoresponder_data = load_autoresponder_data()
    content = message.content.lower()
    if content in autoresponder_data:
        response = autoresponder_data[content]
        await message.channel.send(response)

    await bot.process_commands(message)


if __name__ == "__main__":
    bot.load_extension("ticket")
    bot.run(infected, bot=False)