import asyncio
import grpc
import helloworld


async def run():
    channel = grpc.insecure_channel('localhost:50051')
    client = helloworld.GreeterClient(channel)
    resp = await client.say_hello(name='you')
    print("Greeter client received: " + resp.message)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()  
    loop.run_until_complete(run())  
    loop.close()
