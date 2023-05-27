import discord
from discord.ext import commands
import asyncio

intents = discord.Intents.all()
intents.members = True

client = commands.Bot(command_prefix='/', intents=intents)

@client.event
async def on_ready():
    print(f"Logged in as {client.user}")

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    
    if message.content.startswith("/clearflights"):

        password_msg0 = await message.author.send("Please Enter The Password:")

            # Wait for the user's response in DM
        def check(msg):
            return msg.author == message.author and msg.channel == password_msg0.channel
        password_response = await client.wait_for('message', check=check)

        # Check if the password is correct (in this example, the password is "password123")
        if password_response.content == "beb24":

            filename = 'nextflight.txt'
            try:
                open(filename, 'w').close()
                await message.author.send(f'Flights Cleared.')
            except Exception as e:
                await message.author.send(f'Error occurred while removing text: {e}')
        else:
            await message.channel.send('Incorrect password.')
    
    if message.content.startswith("/discords"):
        embed = discord.Embed(title='Join our Discord!', description='[BEB](https://discord.gg/wCFAQjZtue)', color=discord.Color.blue())
        #channel = message.channel
        #image_url = "BEB.png"

        embed2 = discord.Embed(title='Join our Discord!', description='[La Laiga](https://discord.gg/g3qbwMgW63)', color=discord.Color.blue())
        #channel = message.channel
        #image_url2 = "lalaiga.png"
        embed.set_image(url='https://imgur.com/g7m4U5k.png')
        await message.channel.send(embed=embed)
        #await channel.send(file=discord.File(image_url)) 

        embed2.set_image(url='https://imgur.com/FUfHk9W.png')
        await message.channel.send(embed=embed2)
        #await channel.send(file=discord.File(image_url2))

    
    if message.content.startswith("/setnextflight"):
        # Send a direct message to the user asking for their password
        password_msg = await message.author.send("Please Enter The Password:")

        # Wait for the user's response in DM
        def check(msg):
            return msg.author == message.author and msg.channel == password_msg.channel
        password_response = await client.wait_for('message', check=check)

        # Check if the password is correct (in this example, the password is "password123")
        if password_response.content == "beb24":
    # Retrieve the Minecraft username from the command argument
            username = message.content[8:].strip()

            # Prompt the user to enter the place
            place_msg = await message.author.send("Enter Departure Location :")
            place_response = await client.wait_for('message', check=check)

            # Prompt the user to enter the arrival time
            time_msg = await message.author.send("Enter the Departure Time:")
            time_response = await client.wait_for('message', check=check)

            # Prompt the user to enter the airport
            airport_msg = await message.author.send("Enter Arrival Location:")
            airport_response = await client.wait_for('message', check=check)

            
            arrival_time_msg = await message.author.send("Enter the Arrival Time:")
            arrival_time_response = await client.wait_for('message', check=check)

            # Open the file in read mode and read the contents
            with open("nextflight.txt", "r", encoding='utf-8') as f:
                lines = f.readlines()

            # Find the index of the line containing the user's name, if it exists
            user_index = None
            user_found = False
            for i, line in enumerate(lines):
                if line.startswith(username):
                    user_index = i
                    user_found = True
                    break

            if user_found:
                pass
            else:
                lines.append(f"\nDeparture Location: {place_response.content} 🛫\nDeparture Time: {time_response.content} ⏰\nArrival Location: {airport_response.content} 🛬\nArrival Time: {arrival_time_response.content} ⏰\n-------------------------\n\n")

            # Open the file in write mode and write the updated contents
            with open("nextflight.txt", "w", encoding='utf-8') as f:
                f.writelines(lines)

            # Send a confirmation message to the user
            await message.author.send("Next Flight ✈️ Recorded!")
        else:
            await message.author.send("Password is incorrect.")

    
    if message.content.startswith('/nextflight'):
        with open('nextflight.txt', 'r',encoding='utf-8') as file:
            contents = file.read()

        embed = discord.Embed(title='Next Flight ✈️', description=contents, color=discord.Color.blue())
        embed.set_image(url='https://i.imgur.com/GaxMm0r.png')
        embed.set_footer(text="Flight information provided by BEB Airways")

        # Customize the font size and style of the title and description
        embed.title = f"**{embed.title}**"  # Make the title bold
        embed.description = f"```fix\n{embed.description}\n```"  # Add code block formatting to the description

        await message.channel.send(embed=embed)

    if message.content.startswith('/book'):
        category = discord.utils.get(message.guild.categories, name='Tickets')
        if category is None:
            category = await message.guild.create_category(name='Tickets')

        ticket_name = f'ticket-{message.author.name}'
        existing_ticket = discord.utils.get(message.guild.text_channels, name=ticket_name)
        if existing_ticket:
            await message.channel.send('You already have an open ticket!')
        else:
            overwrites = {
                message.guild.default_role: discord.PermissionOverwrite(read_messages=False),
                message.author: discord.PermissionOverwrite(read_messages=True)
            }

            ticket_channel = await category.create_text_channel(ticket_name, overwrites=overwrites)
            ticket_content = f'{ticket_channel.mention}'
            embed_ticket = discord.Embed(title='Ticket created ✈️', description=ticket_content, color=discord.Color.blue())
            ticket_message = await ticket_channel.send(embed=embed_ticket)
            await ticket_message.add_reaction('❌')

            def check(reaction, user):
                return str(reaction.emoji) == '❌' and reaction.message.channel == ticket_channel

            try:
                reaction, user = await client.wait_for('reaction_add', timeout=None, check=check)
            except asyncio.TimeoutError:
                pass
            else:
                await ticket_channel.delete()

client.run("")
