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


import unittest

from gigadl.GigaDl import GigaDl
from .mock_provider import MockProvider
from .mock_downloader import MockDownloader



class TestGigaDl(unittest.TestCase):
    def setUp(self):
        self.test_downloader = MockDownloader()
        self.test_provider = MockProvider(self.test_downloader)
        self.gigadl = GigaDl()

    def test_init_one_provider(self):
        gigadl = GigaDl(self.test_provider)

        self.assertIn(self.test_provider, gigadl,
            'The provider given in the constructor is registered in the '
            'GigaDl instance')

        self.assertIs(gigadl.provider, self.test_provider,
            'The provider given in the constructor is the one currently used')

        self.assertIs(len(gigadl), 1, 'Only one provider is registered')

    def test_register_provider(self):
        bar_provider = MockProvider(self.test_downloader)

        self.gigadl.register_provider(self.test_provider)
        self.gigadl.register_provider(self.test_provider, 'foo')
        self.gigadl.register_provider(bar_provider, 'Bar bar')

        # match the name
        self.assertIn('Mock provider', self.gigadl,
            'The "Mock provider" provider in is registered in the GigaDl instance')

        self.assertIn('foo', self.gigadl,
            'The "foo" provider in is registered in the GigaDl instance')

        self.assertIn('Bar bar', self.gigadl,
            'The "bar" provider in is registered in the GigaDl instance')

        # match the object
        self.assertIn(self.test_provider, self.gigadl,
            'The "foo" provider in is registered in the GigaDl instance')

        self.assertIn(bar_provider, self.gigadl,
            'The "Bar bar" provider in is registered in the GigaDl instance')

        self.assertIs(len(self.gigadl), 3, 'Three providers are registered')

    def test_register_multiple_named_providers(self):
        bar_provider = MockProvider(self.test_downloader)

        self.gigadl.register_providers(foo=self.test_provider,
                                       bar=bar_provider)

        # match the name
        self.assertIn('foo', self.gigadl,
            'The "foo" provider in is registered in the GigaDl instance')

        self.assertIn('bar', self.gigadl,
            'The "bar" provider in is registered in the GigaDl instance')

        # match the object
        self.assertIn(bar_provider, self.gigadl,
            'The "foo" provider in is registered in the GigaDl instance')

        self.assertIn(self.test_provider, self.gigadl,
            'The "bar" provider in is registered in the GigaDl instance')

        self.assertIs(len(self.gigadl), 2, 'Two providers are registered')

    def test_register_multiple_providers(self):
        bar_provider = MockProvider(self.test_downloader, 'Bar bar')

        self.gigadl.register_providers(bar_provider, self.test_provider)

        # match the name
        self.assertIn('Mock provider', self.gigadl,
            'The "Mock provider" provider in is registered in the GigaDl instance')

        self.assertIn('Bar bar', self.gigadl,
            'The "Bar bar" provider in is registered in the GigaDl instance')

        # match the object
        self.assertIn(self.test_provider, self.gigadl,
            'The "Mock provider" provider in is registered in the GigaDl instance')

        self.assertIn(bar_provider, self.gigadl,
            'The "Bar bar" provider in is registered in the GigaDl instance')

        self.assertIs(len(self.gigadl), 2, 'Two providers are registered')



if __name__ == '__main__':
    unittest.main()
