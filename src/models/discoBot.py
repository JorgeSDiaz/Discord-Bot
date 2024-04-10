import discord


class DiscoBot(discord.Client):

    def __init__(self) -> None:
        intents = discord.Intents.default()
        intents.message_content = True

        super().__init__(intents=intents)

    async def on_ready(self):
        print(f'Logged on as {self.user}, {self.guilds[0]}!')

    async def on_message(self, message):
        print(f'Message from {message.author}: {message.content}')
