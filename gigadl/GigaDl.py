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



def provider_required(func):
  """
    Decorator that forces the selection of a provider to execute the given
    function
  """

  def wrapper(self, *args, **kwargs):
    if self.provider is None:
      raise ValueError('You must select a provider to do this')

    return func(self, *args, **kwargs)

  return wrapper



class GigaDl:
  """ Download manager class """

  def __init__(self, provider=None, providers=None):
    self.provider = provider
    self._providers = {}

    self.registerProviders(providers)

  @property
  def provider(self):
    """ Returns the current provider """

    return self._provider

  @provider.setter
  def proxy(self, provider):
    """ Defines the provider to use (expects an object) """

    self._provider = provider
    self.registerProvider(provider)

  @proxy.deleter
  def proxy(self):
    """ Deletes the current selected provider """

    del self.providers[self._provider]
    self._proxy = None

  def registerProvider(self, provider):
    """ Register the given lists of providers """

    if provider is not None:
      self._providers[provider] = provider

    return self

  def registerProviders(self, providers):
    """ Register the given lists of providers """

    if providers is not None:
      for provider in providers:
        self._registerProvider(provider)

    return self

  def use(self, provider_name):
    """ Selects the provider to use """

    try:
      self._provider = self.providers[provider_name]
    except KeyError, e:
      raise KeyError('The provider "%s" is not registered' % provider_name)

    return self

  @provider_required
  def search(self, terms):
    """ Use the selected provider to search items matching the given terms """

    if not terms:
      return []

    return self.provider.search(terms)

  @provider_required
  def retrieveData(self, url):
    """
      Use the selected provider to retrieve the data corresponding to the given
      URL
    """

    if not url:
      raise Exception('You must pass an URL to retrieve')

    return self.provider.retrieveData(url)