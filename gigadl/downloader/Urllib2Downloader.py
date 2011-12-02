#!/usr/bin/env python
# -*- coding: utf-8 -*-

#  Copyright 2011 Kévin Gomez <contact@kevingomez.fr>
#
#  Permission is hereby granted, free of charge, to any person obtaining a
#  copy of this software and associated documentation files (the "Software"),
#  to deal in the Software without restriction, including without limitation
#  the rights to use, copy, modify, merge, publish, distribute, sublicense,
#  and/or sell copies of the Software, and to permit persons to whom the
#  Software is furnished to do so, subject to the following conditions:
#
#  The above copyright notice and this permission notice shall be included in
#  all copies or substantial portions of the Software.
#
#  The Software is provided "as is", without warranty of any kind, express or
#  implied, including but not limited to the warranties of merchantability,
#  fitness for a particular purpose and noninfringement. In no event shall the
#  authors or copyright holders be liable for any claim, damages or other
#  liability, whether in an action of contract, tort or otherwise, arising
#  from, out of or in connection with the software or the use or other dealing
#  in the Software.


from urllib2 import build_opener, HTTPHandler, ProxyHandler

from gigadl.downloader.DownloaderBase import DownloaderBase


class Urllib2Downloader(DownloaderBase):
    """ urllib2 based downloader """

    USER_AGENT = 'Mozilla/5.0 (X11; U; Linux i686; fr; rv:1.9.1.1) Gecko/20090715 Firefox/3.5.1'

    def __init__(self, proxy=None):
        self.proxy = proxy

    def get(self, url, data=None, headers_list=None):
        handler = HTTPHandler() if self.proxy is None \
                                else ProxyHandler({'http': self.proxy})

        opener = build_opener(handler)
        opener.addheaders = [('User-Agent', Urllib2Downloader.USER_AGENT)]

        if headers_list is not None:
            opener.addheaders.extend(headers_list)

        return opener.open(url, data).read()
