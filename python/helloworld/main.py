import helloworld
import pb

msg = helloworld.HelloRequest(name='foo')
print(msg)

blob = pb.encode(msg)
parsed = pb.decode(blob, helloworld.HelloRequest)

print(parsed)
