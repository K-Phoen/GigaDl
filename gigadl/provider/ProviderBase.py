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


class ProviderBase(object):
  """
    Base class of all providers. The search and retrieveData methods are here
    just to remind us to overload and really implement them in subclasses.
  """

  def __init__(self, downloader):
    """ Initializes the provider with the given download adapter (downloader) """
    self.downloader = downloader

  def search(self, terms):
    """ Searches the given terms to return a list of result objects """
    raise NotImplementedError

  def retrieveData(self, url):
    """
      Retrieves the data corresponding to the given URL. It will return the
      title, download url and stuff like that.
      Each provider returns its own data set (even if we'll try to normalize it).
    """
    raise NotImplementedError

  def __repr__(self):
    """ Represents the provider's name """

    return 'changeme'
