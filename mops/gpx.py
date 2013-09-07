#!/usr/bin/python

import os
import sys
from jinja2 import Environment, PackageLoader

class Storyline (list):
    def __init__(self, *args, **kwargs):
        super(list, self).__init__(*args, **kwargs)

        self.tracks    = []
        self.waypoints = {}
        self.wptid     = 0
        self.env

        for story in self:
            for segment in story['segments']:
                if segment['type'] == 'place':
                    place = segment['place']

                    # only support a single waypoint per location
                    wptkey='{lat}.{lon}'.format(**place['location'])
                    if wptkey in self.waypoints:
                        continue

                    self.wptid += 1

                    # give waypoints a display name if they don't already have
                    # one.
                    if not 'name' in place:
                        place['name'] = 'wpt{:03d}'.format(self.wptid)

                    self.waypoints[wptkey] = place
                elif segment['type'] == 'move':
                    self.tracks.append(segment)

    def asgpx(self):
        template = jinja2.Template(open('gpx.tmpl').read())
        template.render(
                waypoints=waypoints,
                tracks=tracks)

if __name__ == '__main__':
    import json
    data = json.load(sys.argv[1])
    storyline = Storyline(data['storyline'])


