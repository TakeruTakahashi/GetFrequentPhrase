#!/usr/bin/env python
# -*- coding:utf-8 -*-
import json


class LawJsonDecoder():

  def __init__(self, filename):
      with open(filename) as f:
        self.src_dict = json.load(f)

  def decode(self):
      src = ""
      for jo in self.src_dict[u'法令'][u'条']:
          for ko in jo[u'項']:
              src += ko['text']
              if not ko[u'号'] is None:
                  for go in ko[u'号']:
                      src += go['text']
      return src
