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


from ..result.VimeoResult import VimeoResult
from ProviderBase import ProviderBase

from BeautifulSoup import BeautifulSoup


class Vimeo(ProviderBase):

  XML_INFOS_URL = 'http://www.vimeo.com/moogaloop/load/clip:%s'


  def __repr__(self):
    """ Represents the provider's name """

    return 'Vimeo'

  def search(self, keywords):
    raise NotImplementedError('Not implemented')

  def retrieveData(self, url):
    video_id = url.split('/')[-1]
    video_data = {'play_url': url}

    url = Vimeo.XML_INFOS_URL % video_id
    print 'downloading %s' % url
    soup = BeautifulSoup(self.downloader.get(url))

    # find the title
    try:
      video_data['title'] = soup.video.title.string
    except AttributeError:
      video_data['title'] = soup.video.caption.string

    # is the video available in HD?
    try:
      video_data['is_hd'] = soup.video.isHD.string == '1'
    except AttributeError:
       video_data['is_hd'] = False

    # find the thumbnail url
    video_data['thumb'] = soup.video.thumbnail.string

    # find the video duration (in seconds)
    video_data['duration'] = int(soup.video.duration.string)

    # the following stuff is part of the download url
    request_signature = soup.request_signature.string
    timestamp = soup.timestamp.string
    q = 'hd' if video_data['is_hd'] else 'sd'

    data = (video_id, request_signature, timestamp, q)

    video_data['url'] = "http://www.vimeo.com/moogaloop/play/clip:%s/%s/%s/?q=%s" % data
    video_data['url_sd'] = video_data['url'].replace('?q=%s' % q, '?q=sd')

    return VimeoResult(video_data)
