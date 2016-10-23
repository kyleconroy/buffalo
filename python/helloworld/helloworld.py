import pb
import aioh2


class HelloRequest(pb.Message):
    """
    The request message containing the user's name.
    """

    name: pb.field(1, str)

    def __init__(self, name=""):
        self.name = name


class HelloReply(pb.Message):
    """
    The response message containing the greetings
    """

    message: pb.field(1, str)

    def __init__(self, message=""):
        self.message = message


class Greeter(object):
    """
    The greeting service definition.
    """
    async def say_hello(self, msg: HelloRequest) -> HelloReply:
        raise NotImplementedError


def attach_greeter(server, greeter: Greeter):
    # Just an idea
    server.route({
        "helloworld.Greeter/SayHello", greeter.say_hello,
    })


class GreeterClientH2(object):
    """
    The Gretter client definition.
    """
    def __init__(self, host, port):
        self.conn = aioh2.open_connection(host, port)

    async def say_hello(self, name="") -> HelloReply:
        print('Await conn')
        client = await self.conn

        # Start request with headers
        print('Await stream')
        stream_id = await client.start_request({':method':'GET', ':path':'/post'})

        # Send my name "world" as whole request body
        # print('Await data')
        # await client.send_data(stream_id, b'world', end_stream=True)

        # Receive response headers
        # print('Await headers')
        # headers = await client.recv_response(stream_id)
        # print('Response headers:', headers)

        # Read all response body
        print('Await resp')
        resp = await client.read_stream(stream_id, -1)
        print('Response body:', resp)

        # Read response trailers
        # print('Await trailers')
        # trailers = await client.recv_trailers(stream_id)
        # print('Response trailers:', trailers)

        return HelloRequest(name='fake')

class GreeterClientProxy(object):
    """
    The Gretter client definition.
    """
    def __init__(self, srv):
        self.srv = srv

    async def say_hello(self, name="") -> HelloReply:
        return await self.srv.say_hello(None, HelloRequest(
            name=name,
        ))
