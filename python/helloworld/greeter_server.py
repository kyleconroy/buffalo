import asyncio
import grpc
import helloworld


class Greeter(helloworld.Greeter):
    async def say_hello(self, ctx, msg):
        return helloworld.HelloReply(message='Hello, %s!' % msg.name)


def serve():
    server = grpc.async_server(asyncio.get_event_loop())
    helloworld.attach_greeter(server, Greeter())
    server.add_insecure_port('[::]:50051')
    server.start()

if __name__ == '__main__':
    serve()
