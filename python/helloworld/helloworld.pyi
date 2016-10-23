class HelloRequest:
    name: str
    def __init__(self, name: str): ...


class HelloReply:
    message: str
    def __init__(self, message: str): ...
