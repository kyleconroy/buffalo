import asyncio
import helloworld

class Greeter(helloworld.Greeter):
    async def say_hello(self, ctx, msg):
        return helloworld.HelloReply(message='Hello, %s!' % msg.name)


async def run():
    client = helloworld.GreeterClientProxy(Greeter())
    resp = await client.say_hello(name='you')
    print("Greeter client received: " + resp.message)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()  
    loop.run_until_complete(run())  
    loop.close()
