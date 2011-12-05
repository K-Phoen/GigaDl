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


from functools import wraps



def provider_required(func):
    """
        Decorator that forces the selection of a provider to execute the given
        function. If no provider is selected, a ValueError exception is raised.
    """

    @wraps(func)
    def wrapper(self, *args, **kwargs):
        if self.provider is None:
            raise ValueError('You must select a provider to do this')

        return func(self, *args, **kwargs)

    return wrapper



class GigaDl(object):
    """ Download manager class """

    def __init__(self, provider=None):
        self._providers = {}
        self._provider = provider

        self.register_provider(provider)

    @property
    def provider(self):
        """ Returns the current provider """

        return self._provider

    @provider.setter
    def provider(self, provider):
        """ Defines the provider to use (expects an object) """

        self._provider = provider
        self.register_provider(provider)

    @provider.deleter
    def provider(self):
        """ Deletes the current selected provider """

        del self._providers[self._provider]
        self._provider = None

    def register_provider(self, provider, name=None):
        """ Register the given lists of providers """

        if provider is not None:
            self._providers[name or repr(provider)] = provider

        return self

    def register_providers(self, *args, **kwargs):
        """ Register the given lists of providers """

        for provider in args:
            self.register_provider(provider)

        for name, provider in kwargs.items():
            self.register_provider(provider, name)

        return self

    def use(self, provider_name):
        """ Selects the provider to use """

        try:
            self._provider = self._providers[provider_name]
        except KeyError:
            raise KeyError('The provider "%s" is unknown' % provider_name)

        return self

    @provider_required
    def search(self, terms):
        """
          Use the selected provider to search items matching the given terms.
        """

        if not terms:
            return []

        return self.provider.search(terms)

    @provider_required
    def retrieve_data(self, url):
        """
            Use the selected provider to retrieve the data corresponding to
            the given URL
        """

        if not url:
            raise Exception('You must pass an URL to retrieve')

        return self.provider.retrieve_data(url)

    def __iter__(self):
        """ Iterator for looping through the providers """

        return iter(self._providers)

    def __contains__(self, item):
        """ Test if the given item in registered as a provider """

        if type(item) is str:
            return item in self._providers

        return item in self._providers.values()

    def __len__(self):
        """ Counts the registered providers """

        return len(self._providers)
