#!/usr/bin/python

import os
import sys
import jinja2

activity_names = {
        'wlk': 'walking',
        'trp': 'transport',
        'run': 'running',
        'bik': 'biking',
        }

def moves2gpx(storyline):
    tracks = []
    waypoints = {}
    wptcount = 0

    for story in storyline:
        for segment in story['segments']:
            if segment['type'] == 'place':
                place = segment['place']

                # only support a single waypoint per location
                wptkey='{lat}.{lon}'.format(**place['location'])
                if wptkey in waypoints:
                    continue

                wptcount += 1

                # give waypoints a display name if they don't already have
                # one.
                if not 'name' in place:
                    place['name'] = 'wpt{:03d}'.format(wptcount)

                waypoints[wptkey] = place
            elif segment['type'] == 'move':
                tracks.append(segment)

    template = jinja2.Template(open('gpx.tmpl').read())
    print template.render(
            waypoints=waypoints,
            tracks=tracks)

if __name__ == '__main__':
    main()

