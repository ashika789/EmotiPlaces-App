#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import webapp2
import operator
import jinja2
import os
import urllib2
import json
import pprint
from collections import defaultdict

jinja_environment = jinja2.Environment(loader=
    jinja2.FileSystemLoader(os.path.dirname(__file__)))

class HomeHandler(webapp2.RequestHandler):
    def get(self):
        template_values = {#'name' : self.request.get('name'),
        }

        response = urllib2.urlopen('https://api.foursquare.com/v2/venues/search?ll=40.7,-74&client_id=4PVC0RLB5XVMRVOGN1FLS2MVQCYXLBWGNHXPSGLGKL3KWOCO&client_secret=MMGCYSNJBAIBOSHRTTGHDM4IPT20AMWGCDLCKDJN5045MEM2&v=20140920')
        body = response.read()
        foursquares = json.loads(body)
        categorynames = set()
        categoryvenues = defaultdict(list)
        venues = foursquares['response']['venues']
        for venue in venues:
            for category in venue['categories']:
                categorynames.add(category['name'])
                categoryvenues[category['name']].append(venue)
                '''
                search_results = api.GetSearch(self, term='name', geocode=loc, count=1000, result_type='recent')
                emojis = defaultdict(0)
                for result in search_results:
                    for character in result['text']:
                        if ord(character) > 10000: #edit; if it's an emoji
                            emojis[character] += 1
                sorted_emojis = sort(emojis.iteritems(), key=operator.itemgetter(1))
                #top 3 emojis are here
                print sorted_emojis[-1], sorted_emojis[-2], sorted_emojis[-3]
                '''


        template_values['categorynames'] = categorynames
        template_values['categoryvenues'] = categoryvenues[self.request.get('category')]

        template = jinja_environment.get_template('views/home.html')
        self.response.out.write(template.render(template_values))

class MainHandler(webapp2.RequestHandler):
    def get(self):
        self.response.write('Hello world!')

app = webapp2.WSGIApplication([
    ('/', HomeHandler), ('/go', HomeHandler)
], debug=True)
