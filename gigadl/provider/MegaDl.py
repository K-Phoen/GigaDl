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


from ..result.MegaResult import MegaResult
from gigadl.provider.ProviderBase import ProviderBase

import re
from BeautifulSoup import BeautifulSoup
from urllib import unquote_plus as unquote
from urllib2 import quote, urlopen, Request


class MegaDl(ProviderBase):

    SERVER_URL = 'http://www.megavideo.com'
    XML_INFOS_URL = '%s/xml/videolink.php?v=%s'
    SEARCH_URL = '%s/?c=search&s=%s'

    URL_PLAYER_REGEX = 'value="([a-zA-Z\./:0-9]*)"'


    def __repr__(self):
        """ Represents the provider's name """

        return 'MegaDl'

    def search(self, keywords):
        url = MegaDl.SEARCH_URL % (MegaDl.SERVER_URL, quote(keywords))
        tmp_data = self.downloader.get(url)

        results = []

        soup = BeautifulSoup(tmp_data)
        for div in soup.findAll('div', attrs={'class': 'forms_div2'}):
            # filter non-result divs
            try:
                div['onclick']
            except KeyError:
                continue

            result = self._parse_search_result(div)
            if result is not None:
                results.append(result)

        return results

    def _parse_search_result(self, div):
        try:
            title = div.div.findAll('div', attrs={'class': 'bl_thumb_fl1'})[0].div.string
            img = div.div.findAll('img')[0]['src']
            video_id = div['onclick'].split("'")[1] # watchvideo('9C080NTL'); --> ['watchvideo(', '9C080NTL', ');']

            return MegaResult({
                'title': title,
                'thumb': img,
                'play_url': '%s/?v=%s' % (MegaDl.SERVER_URL, video_id)
            })
        except KeyError:
            return None

    def retrieve_data(self, url):
        video_id = url.split('=')[1]
        video_data = {'play_url': url}

        url = MegaDl.XML_INFOS_URL % (MegaDl.SERVER_URL, video_id)
        soup = BeautifulSoup(self.downloader.get(url))
        row = soup.findAll('row')[0]

        v9 = row['un']
        v3 = int(row['k1'])
        v10 = int(row['k2'])
        server = row['s']

        # to find the thumbnail
        embed_code = unquote(row['embed'])
        url_player = re.compile(MegaDl.URL_PLAYER_REGEX).findall(embed_code)[0]

        video_data['title'] = unquote(row['title'])
        video_data['thumb'] = urlopen(Request(url_player)).geturl().split('=')[1].split('&')[0]

        try:
            video_data['url'] = unquote(row['hd_url'])
        except KeyError:
            video_data['url'] = 'http://www%s.megavideo.com/files/%s/' % (server, self._decrypt(v9, v3, v10))

        return MegaResult(video_data)

    def _decrypt(self, string, key1, key2):
        v1, v3 = [], 0
        stop = len(string)

        while v3 < stop:
            v1.append(unicode(bin(int('0x%s' % string[v3], 16))[2:]).zfill(4))
            v3 += 1

        v1 = [int(i) for i in ''.join(v1)]

        v3, v6 = 0, [''] * 384
        while v3 < 384:
            key1 = (key1 * 11 + 77213) % 81371
            key2 = (key2 * 17 + 92717) % 192811
            v6[v3] = (key1 + key2) % 128

            v3 += 1

        v3 = 256
        while v3 >= 0:
            v5 = v6[v3]
            v4 = v3 % 128
            v8 = v1[v5]
            v1[v5] = v1[v4]
            v1[v4] = v8

            v3 -= 1

        v3 = 0
        while v3 < 128:
            v1[v3] ^= (v6[v3 + 256] & 1)
            v3 += 1

        v12 = u''.join([unicode(i) for i in v1])
        v3, v7 = 0, []
        stop = len(v12)
        while v3 < stop:
            v9 = v12[v3: v3 + 4]
            v7.append(v9)

            v3 += 4

        v2, v3 = [], 0
        stop = len(v7)
        while v3 < stop:
            v2.append(self._bin2hex(v7[v3]))
            v3 += 1

        return ''.join(v2)

    def _bin2hex(self, bin_val):
        return unicode(hex(int(bin_val, 2))[2:])
