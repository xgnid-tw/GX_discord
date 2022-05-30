"""System module."""
import json
from os import getenv
import threading
import asyncio

from dotenv import load_dotenv
import discord
import aio_pika

class Bot:
    def __init__(self) -> None:
        load_dotenv()
        # intents setting(permission of discord)
        intents = discord.Intents().all()
        self.client = discord.Client(intents=intents)

        @self.client.event
        async def on_ready() -> None:
            guild = self.get_guild(self.client.guilds)
            if guild:                
                await self.rabbit_consumer()
    
    async def rabbit_consumer(self):
        connection = await aio_pika.connect(
            host=getenv('RABBITMQ_HOST'),
            login=getenv('RABBITMQ_USERNAME'),
            password=getenv('RABBITMQ_PASSWORD'),
            virtualhost=getenv('RABBITMQ_VHOST')
        )

        channel = await connection.channel()

        exchange = await channel.declare_exchange(name=getenv('RABBITMQ_EXCHANGE'),type='direct')
        queue = await channel.declare_queue(name='',exclusive='True',)
        await queue.bind(exchange, getenv('RABBITMQ_QUEUE_KEY_NOTION'))

        async def callback(incoming_message: aio_pika.abc.AbstractIncomingMessage):
            try:
                result = json.JSONDecoder().decode(incoming_message.body.decode())
                targets = list(filter(lambda u: u.id == result['user_id'], self.client.users))
                if targets:
                    await targets[0].send(result['message'])
            except json.decoder.JSONDecodeError:
                # log jsondecode error here
                pass

        await queue.consume(callback, no_ack=True)
        await asyncio.Future()

    def get_guild(self,guilds):
        """ Get specify Guild """
        for guild in guilds:
            if guild.name == getenv('DISCORD_GUILD'):
                return guild
        return None

    def run(self) -> None:
        self.client.run(getenv('DISCORD_TOKEN'))
