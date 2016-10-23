import pb
from pb import Type


class Point(pb.Message):
    """
    Points are represented as latitude-longitude pairs in the E7 representation
    (degrees multiplied by 10**7 and rounded to the nearest integer).
    Latitudes should be in the range +/- 90 degrees and longitude should be in
    the range +/- 180 degrees (inclusive).
    """

    latitude: pb.field(1, Type.int32)
    longitude: pb.field(2, Type.int32)

    def __init__(self, latitude=0, longitude=0):
        self.latitude = latitude
        self.longitude = longitude


class Rectangle(pb.Message):
    """
    A latitude-longitude rectangle, represented as two diagonally opposite
    points "lo" and "hi".
    """

    """One corner of the rectangle."""
    lo: pb.field(1, Point)

    """The other corner of the rectangle."""
    hi: pb.field(2, Point)

    def __init__(self, lo=0, hi=0):
        self.lo = lo
        self.hi = hi


class Feature(pb.Message):
    """
    A feature names something at a given point.

    If a feature could not be named, the name is empty.
    """

    """The name of the feature."""
    name: pb.field(1, str)

    """The point where the feature is detected."""
    location: pb.field(2, Point)

    def __init__(self, name="", location=None):
        self.name = name
        self.location = location


class RouteNote(pb.Message):
    """A RouteNote is a message sent while at a given point."""

    """The location from which the message is sent."""
    location: pb.field(1, Point)

    """The message to be sent."""
    message: pb.field(2, str)

    def __init__(self, location=None, message=""):
        self.location = location
        self.message = message


class RouteSummary(pb.Message):
    """
    A RouteSummary is received in response to a RecordRoute rpc.

    It contains the number of individual points received, the number of
    detected features, and the total distance covered as the cumulative sum of
    the distance between each point.
    """

    """The number of points received."""
    point_count: pb.field(1, Type.int32)

    """The number of known features passed while traversing the route."""
    feature_count: pb.field(2, Type.int32)

    """The distance covered in metres."""
    distance: pb.field(3, Type.int32)

    """The duration of the traversal in seconds."""
    elapsed_time: pb.field(4, Type.int32)

    def __init__(self, point_count=0, feature_count=0, distance=0,
                 elapsed_time=0):
        self.point_count = point_count
        self.feature_count = feature_count
        self.distance = distance
        self.elapsed_time = elapsed_time


class RouteGuide(object):
    """Provides methods that implement functionality of route guide server."""

    async def get_feature(self, ctx, request):
        raise NotImplementedError()

    async def list_features(self, ctx, request):
        raise NotImplementedError()

    async def record_route(self, ctx, stream):
        raise NotImplementedError()

    async def route_chat(self, ctx, stream):
        raise NotImplementedError()


class RouteGuideClient(object):
    """Provides methods that implement functionality of route guide server."""

    def __init__(self, srv):
        self.srv = srv

    async def get_feature(self, latitude=0, longitude=0):
        return await self.srv.get_feature(None, Point(
            longitude=longitude,
            latitude=latitude,
        ))

    async def list_features(self, lo=None, hi=None):
        rect = Rectangle(lo=lo, hi=hi)
        async for feature in self.srv.list_features(None, rect):
            yield feature

    async def record_route(self, stream):
        return await self.srv.record_route(None, stream)

    async def route_chat(self, stream):
        async for note in self.srv.route_chat(None, stream):
            yield note
