import pb


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


class GreeterClient(object):
    """
    The Gretter client definition.
    """
    def __init__(self, srv):
        self.srv = srv

    async def say_hello(self, name="") -> HelloReply:
        return await self.srv.say_hello(None, HelloRequest(
            name=name,
        ))
