import discord

class MyClient(discord.Client):
    async def on_ready(self):
        print(f'Logged on as {self.user}!')
        facter = client.get_user(1284316522415657011)
        print(dir(facter))
        dms = await facter.create_dm()
        await dms.send("yay")
    async def on_message(self, message):
        print(f'Message from {message.author}: {message.content}')

intents = discord.Intents.default()
intents.message_content = True

client = MyClient(intents=intents)


# Dear Headquarters, 
# I trust this message reaches you securely. I am writing to provide an update on my current location. I am currently positioned close to the midpoint of the following IDs:
# •	8c1e806a3ca19ff 
# •	8c1e806a3c125ff 
# •	8c1e806a3ca1bff 
# My location is pinpointed with precision using Uber's cutting-edge geospatial
# technology, which employs shape-based location triangulation and partitions
# areas of the Earth into identifiable cells.
# To initiate secure communication with me, please adhere to the discreet method
# we've established. Transmit the identified location's name through the secure
# communication channel accessible at
# https://www.linkedin.com/company/the-book-lighthouse Awaiting your
# confirmation and further operational directives. 
# Best regards, 
# Vivoxanderith

# 41.544426767, 12.994242633
# 41.544551463, 12.994414040
# 41.544383254, 12.994469395