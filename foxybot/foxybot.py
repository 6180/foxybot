import asyncio

import discord
import requests

from config import Config as config


async def _on_ready(shard, shard_id, num_shards):
        print(f'Shard {shard_id+1} connected with {len(shard.servers)} servers.')
        await shard.change_presence(game=discord.Game(name=f'Alive! | Shard {shard_id+1}/{num_shards}'))


async def _on_member_join(client, member):
    pass


async def _on_message(client, msg):
    print(msg.content)


def _register_shard_events(_shard, _shard_id, _num_shards):
    @_shard.async_event
    async def on_ready():
        await _on_ready(_shard, _shard_id, _num_shards)

    @_shard.async_event
    async def on_member_join(member):
        await _on_member_join(_shard, member)

    @_shard.async_event
    async def on_message(msg):
        await _on_message(_shard, msg)


class Bot(object):

    def __init__(self):
        self.startup_delay = 5
    
    def run(self, token=None):
        async def _delayed_start(token, shard, delay):
            await asyncio.sleep(delay)
            await shard.start(self.token)

        self.shards = []
        self.token = token or config['token']
        
        tasks = []
        num_shards = requests.get('https://discordapp.com/api/v7/gateway/bot',
                                  headers={'Authorization': f'Bot {self.token}'}).json()['shards']

        for shard_id in range(num_shards):
            shard = discord.Client(shard_id=shard_id, shard_count=num_shards)
            _register_shard_events(shard, shard_id, num_shards)
            tasks.append(_delayed_start(self.token, shard, shard_id * self.startup_delay))
            self.shards.append(shard)

        self.shards = tuple(self.shards)
        
        loop = asyncio.get_event_loop()

        try:
            loop.run_until_complete(asyncio.gather(*tasks))
        except Exception as ex:
            print(ex)
        finally:
            loop.run_until_complete(loop.shutdown_asyncgens())
            loop.close()

bot = Bot()
bot.run()
