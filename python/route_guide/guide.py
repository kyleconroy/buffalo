import asyncio
import route_guide
import route_guide_server

async def run():
    server = route_guide_server.RouteGuider()
    client = route_guide.RouteGuideClient(Greeter())
    resp = await client.say_hello(name='you')
    print("Greeter client received: " + resp.message)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()  
    loop.run_until_complete(run())  
    loop.close()

