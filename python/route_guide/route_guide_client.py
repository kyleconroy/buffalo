import random
import time

import grpc

import route_guide
import route_guide_resources


def make_route_note(message, latitude, longitude):
    point = route_guide.Point(latitude=latitude, longitude=longitude)
    return route_guide.RouteNote(message=message, location=point)


async def guide_get_one_feature(client, point):
    feature = await client.get_feature(point)
    if not feature.location:
        print("Server returned incomplete feature")
        return

    if feature.name:
        print("Feature called %s at %s" % (feature.name, feature.location))
    else:
        print("Found no feature at %s" % feature.location)


async def guide_get_feature(client):
    for (lat, lng) in [(409146138, -746188906), (0, 0)]:
        point = route_guide.Point(latitude=lat, longitude=lng)
        await guide_get_one_feature(client, point)


async def guide_list_features(client):
    rectangle = route_guide.Rectangle(
        lo=route_guide.Point(latitude=400000000, longitude=-750000000),
        hi=route_guide.Point(latitude=420000000, longitude=-730000000))

    print("Looking for features between 40, -75 and 42, -73")
    features = await client.list_features(rectangle)

    for feature in features:
        print("Feature called %s at %s" % (feature.name, feature.location))


def generate_route(feature_list):
    for _ in range(0, 10):
        random_feature = feature_list[random.randint(0, len(feature_list) - 1)]
        print("Visiting point %s" % random_feature.location)
        yield random_feature.location
        time.sleep(random.uniform(0.5, 1.5))


async def guide_record_route(client):
    feature_list = route_guide_resources.read_route_guide_database()

    route_iterator = generate_route(feature_list)
    route_summary = await client.record_route(route_iterator)
    print("Finished trip with %s points " % route_summary.point_count)
    print("Passed %s features " % route_summary.feature_count)
    print("Travelled %s meters " % route_summary.distance)
    print("It took %s seconds " % route_summary.elapsed_time)


async def generate_messages():
    messages = [
        make_route_note("First message", 0, 0),
        make_route_note("Second message", 0, 1),
        make_route_note("Third message", 1, 0),
        make_route_note("Fourth message", 0, 0),
        make_route_note("Fifth message", 1, 0),
    ]
    for msg in messages:
        print("Sending %s at %s" % (msg.message, msg.location))
        yield msg
        time.sleep(random.uniform(0.5, 1.0))


async def guide_route_chat(client):
    responses = client.route_chat(generate_messages())
    async for resp in responses:
        print("Received message %s at %s" % (resp.message, resp.location))


async def run():
    channel = grpc.insecure_channel('localhost:50051')
    client = route_guide.RouteGuideClient(channel)
    print("-------------- GetFeature --------------")
    await guide_get_feature(client)
    print("-------------- ListFeatures --------------")
    await guide_list_features(client)
    print("-------------- RecordRoute --------------")
    await guide_record_route(client)
    print("-------------- RouteChat --------------")
    await guide_route_chat(client)


if __name__ == '__main__':
    loop = asyncio.get_event_loop()  
    loop.run_until_complete(run())  
    loop.close()
