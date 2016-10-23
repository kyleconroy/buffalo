import asyncio
import time
import math

import route_guide
import route_guide_resources


def get_feature(feature_db, point):
    """Returns Feature at given location or None."""
    for feature in feature_db:
        if feature.location == point:
            return feature
    return None


def get_distance(start, end):
    """Distance between two points."""
    coord_factor = 10000000.0
    lat_1 = start.latitude / coord_factor
    lat_2 = end.latitude / coord_factor
    lon_1 = start.longitude / coord_factor
    lon_2 = end.longitude / coord_factor
    lat_rad_1 = math.radians(lat_1)
    lat_rad_2 = math.radians(lat_2)
    delta_lat_rad = math.radians(lat_2 - lat_1)
    delta_lon_rad = math.radians(lon_2 - lon_1)

    a = (pow(math.sin(delta_lat_rad / 2), 2) +
        (math.cos(lat_rad_1) * math.cos(lat_rad_2) *
            pow(math.sin(delta_lon_rad / 2), 2)))
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    R = 6371000; # metres
    return R * c;


class RouteGuider(route_guide.RouteGuide):
    def __init__(self):
        self.db = route_guide_resources.read_route_guide_database() 

    async def get_feature(self, ctx, request):
        feature = get_feature(self.db, request)
        if feature is None:
            return route_guide.Feature(location=request)
        else:
            return feature

    async def list_features(self, ctx, request):
        left = min(request.lo.longitude, request.hi.longitude)
        right = max(request.lo.longitude, request.hi.longitude)
        top = max(request.lo.latitude, request.hi.latitude)
        bottom = min(request.lo.latitude, request.hi.latitude)
        for feature in self.db:
            if (feature.location.longitude >= left and
                feature.location.longitude <= right and
                feature.location.latitude >= bottom and
                feature.location.latitude <= top):
                yield feature

    async def record_route(self, ctx, stream):
        point_count = 0
        feature_count = 0
        distance = 0.0
        prev_point = None

        start_time = time.time()
        async for point in stream:
            point_count += 1
            if get_feature(self.db, point):
                feature_count += 1
            if prev_point:
                distance += get_distance(prev_point, point)
            prev_point = point

        elapsed_time = time.time() - start_time
        return route_guide.RouteSummary(point_count=point_count,
                                        feature_count=feature_count,
                                        distance=int(distance),
                                        elapsed_time=int(elapsed_time))

    async def route_chat(self, ctx, stream):
        prev_notes = []
        async for note in stream:
            for prev in prev_notes:
                lat = prev.location.latitude == note.location.latitude
                lng = prev.location.longitude == note.location.longitude
                if lat and lng:
                    yield prev
            prev_notes.append(note)
