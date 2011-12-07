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


def throw_error(search):
    raise ValueError(search)


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

    def test_use(self):
        self.test_provider.search = throw_error

        # use our custom provider
        self.gigadl.register_provider(self.test_provider)
        self.gigadl.use('Mock provider')

        with self.assertRaises(ValueError) as cm:
            self.gigadl.search('foo')

        self.assertIs(str(cm.exception), 'foo', 'The right provider is used '
                      'when giving its name')

        self.gigadl.use(self.test_provider)
        with self.assertRaises(ValueError) as cm:
            self.gigadl.search('bar')

        self.assertIs(str(cm.exception), 'bar', 'The right provider is used '
                      'when giving an already registered object')

        bar_provider = MockProvider(self.test_downloader, 'Bar bar')
        bar_provider.search = throw_error

        self.gigadl.use(bar_provider)
        with self.assertRaises(ValueError) as cm:
            self.gigadl.search('biz')

        self.assertIs(str(cm.exception), 'biz', 'The right provider is used '
                      'when giving a non registered object')

    def test_provider_setter_property(self):
        self.test_provider.search = throw_error

        # use our custom provider
        self.gigadl.register_provider(self.test_provider)
        self.gigadl.provider = 'Mock provider'

        with self.assertRaises(ValueError) as cm:
            self.gigadl.search('foo')

        self.assertIs(str(cm.exception), 'foo', 'The right provider is used '
                      'when giving its name')

        self.gigadl.provider = self.test_provider
        with self.assertRaises(ValueError) as cm:
            self.gigadl.search('bar')

        self.assertIs(str(cm.exception), 'bar', 'The right provider is used '
                      'when giving an already registered object')

        bar_provider = MockProvider(self.test_downloader, 'Bar bar')
        bar_provider.search = throw_error

        self.gigadl.provider = bar_provider
        with self.assertRaises(ValueError) as cm:
            self.gigadl.search('biz')

        self.assertIs(str(cm.exception), 'biz', 'The right provider is used '
                      'when giving a non registered object')


    def test_provider_getter_property(self):
        self.assertIsNone(self.gigadl.provider, 'None if no provider selected')

        # register a provider and use it
        self.gigadl.register_provider(self.test_provider)
        self.gigadl.use(self.test_provider)

        self.assertIs(self.gigadl.provider, self.test_provider, 'When a '
                      'provider is selected, it is returned by the property')

        # register another provider
        bar_provider = MockProvider(self.test_downloader)
        self.gigadl.register_provider(bar_provider)

        self.assertIs(self.gigadl.provider, self.test_provider, 'Registering '
                      'another provider does not impact the selected one')

        # use it
        self.gigadl.use(bar_provider)

        self.assertIs(self.gigadl.provider, bar_provider, 'When another '
                      'provider is selected, it is returned by the property')

    def test_provider_deleter_property(self):
        self.assertIsNone(self.gigadl.provider, 'No provider selected')

        self.gigadl.register_provider(MockProvider(self.test_downloader, 'bar'))

        self.gigadl.use(self.test_provider)
        self.assertIs(self.gigadl.provider, self.test_provider, 'A provider is selected')

        del self.gigadl.provider
        self.assertIsNone(self.gigadl.provider, 'No provider selected')
        self.assertIs(len(self.gigadl), 1, 'Still one provider registered')
        self.assertNotIn('Mock provider', self.gigadl, 'The "Mock provider" is'
                         'not registered anymore')
        self.assertIn('bar', self.gigadl, 'The bar provider is still'
                      'registered')

    def test_search(self):
        with self.assertRaises(ValueError):
            self.gigadl.search('foo')

        self.test_provider.search = throw_error
        self.gigadl.provider = self.test_provider

        self.assertEqual(self.gigadl.search(''), [], 'An empty search returns an '
                      'empty list, withouth calling the provider')

        with self.assertRaises(ValueError) as cm:
            self.gigadl.search('biz')

        self.assertIs(str(cm.exception), 'biz', 'The search call is delegated '
                      'to the provider')

    def test_retrieve_data(self):
        with self.assertRaises(ValueError):
            self.gigadl.retrieve_data('http://www.some-url.com/?v=some_id')

        self.test_provider.retrieve_data = throw_error
        self.gigadl.provider = self.test_provider

        with self.assertRaises(ValueError):
            self.gigadl.retrieve_data('')

        with self.assertRaises(ValueError) as cm:
            self.gigadl.retrieve_data('biz')

        self.assertIs(str(cm.exception), 'biz', 'The retrieve_data call is delegated '
                      'to the provider')
