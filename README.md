# GigaDl

**GigaDl** is a library wich helps you search and download video/songs/whatever
from popular websites.

The library is splitted in two parts: `Downloaders` and `Providers` and is really extensible.


# Usage

First, you need a `downloader`:

``` python
downloader = Urllib2Downloader()
```

This downloader uses the urllib2 standard library to make HTTP queries. It
support classic queries, but also "proxified" ones (see its `proxy` parameter).


Then, choose a provider and create a GigaDl instance:

```python
provider = MegaDl(downloader)

gigadl = GigaDl(provider) # use the MegaDl provider
# or
gigadl = GigaDl()
gigadl.registerProvider(provider)
gigadl.registerProviders([
  FooProvider(downloader),
  BarProvider(downloader)
])
gigadl.use('MegaDl')
```

Here, we chose to download content from MegaVideo, using the urllib2 downloader
we just created.


# API

The main methods are `search(terms)` and `retrieveData(url)`, they are the only methods available in all the providers.

```python
provider = MegaDl(Urllib2Downloader())
gigadl = GigaDl(provider)

# the search(terms) method performs a ... search!
results = gigadl.search('daft punk') # returns a list of MegaResult objects

# and the retrieveData(url) returns all the data that a provider can find for an url
data = gigadl.retrieveData(results[0].play_url)
print 'The "%s" item can be downloaded here: %s' % (data, data.url)
```

Even if these two methods are enough to use GigaDl, there are a few more:

```python
gigadl.registerProvider(myNewProvider) # adds the given provider to the usable providers
gigadl.registerProviders([myFirstProvider, otherProvider]) # same, but with a list
gigadl.use('SomeProviderName') # selects the provider to use for the next calls to search() or retrieveData()
gigadl.provider = MegaDl(Urllib2Downloader()) # same, but directly with an object
gigadl.provider # returns the provider object in use
```


# Licence

**GigaDl** is under MIT/Expat licence (see the LICENCE file).
