import asyncio
import helloworld


async def run():
    client = helloworld.GreeterClientH2('0.0.0.0', 50051)
    resp = await client.say_hello(name='you')
    print("Greeter client received: " + resp.message)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()  
    loop.run_until_complete(run())  
    loop.close()
