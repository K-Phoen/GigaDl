#!/usr/bin/env python
# -*- coding: utf-8 -*-

#   Copyright 2011 Kévin Gomez <contact@kevingomez.fr>
#
#   Permission is hereby granted, free of charge, to any person obtaining a
#   copy of this software and associated documentation files (the "Software"),
#   to deal in the Software without restriction, including without limitation
#   the rights to use, copy, modify, merge, publish, distribute, sublicense,
#   and/or sell copies of the Software, and to permit persons to whom the
#   Software is furnished to do so, subject to the following conditions:
#
#   The above copyright notice and this permission notice shall be included in
#   all copies or substantial portions of the Software.
#
#   The Software is provided "as is", without warranty of any kind, express or
#   implied, including but not limited to the warranties of merchantability,
#   fitness for a particular purpose and noninfringement. In no event shall the
#   authors or copyright holders be liable for any claim, damages or other
#   liability, whether in an action of contract, tort or otherwise, arising
#   from, out of or in connection with the software or the use or other dealing
#   in the Software.

from gigadl.GigaDl import GigaDl
from gigadl.provider.MegaDl import MegaDl
from gigadl.downloader.Urllib2Downloader import Urllib2Downloader


if __name__ == '__main__':
  provider = MegaDl(Urllib2Downloader())
  dl = GigaDl(provider)

  while True:
    print 'Search:',
    keywords = raw_input()

    print

    print 'Searching...'
    results = dl.search(keywords)

    for i, result in enumerate(results):
      print '(%d) %s' % (i, result)
    else:
      print 'Nothing found!'
      continue

    print
    print 'Which video do you want to download? (enter to make a new search)'

    try:
      num = int(raw_input())
    except ValueError:
      continue

    if num >= len(results):
      print 'Incorrect number!'

    print 'Retrieving data...'
    data = dl.retrieveData(results[num].play_url)

    print data
    print 'You can download the video here: %s' % data.url
