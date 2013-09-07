#!/usr/bin/python

import os
import sys
from jinja2 import Environment, PackageLoader

from .templates import Templates

class Storyline (list):
    def __init__(self, *args, **kwargs):
        super(Storyline, self).__init__(*args)

        self.tracks    = []
        self.waypoints = {}
        self.wptid     = 0
        self.templates = Templates('templates')

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
        template = self.templates['gpx.tmpl']
        return template.render(
                waypoints=self.waypoints.values(),
                tracks=self.tracks)

if __name__ == '__main__':
    import json
    data = json.load(open(sys.argv[1]))
    storyline = Storyline(data['storyline'])

    print (storyline.asgpx())

