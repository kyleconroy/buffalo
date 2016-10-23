import json

import route_guide


def read_route_guide_database():
  """Reads the route guide database.

  Returns:
    The full contents of the route guide database as a sequence of
      route_guide_pb2.Features.
  """
  feature_list = []
  with open("route_guide_db.json") as route_guide_db_file:
    for item in json.load(route_guide_db_file):
      feature = route_guide.Feature(
          name=item["name"],
          location=route_guide.Point(
              latitude=item["location"]["latitude"],
              longitude=item["location"]["longitude"]))
      feature_list.append(feature)
  return feature_list
