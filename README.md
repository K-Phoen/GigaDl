# GigaDl

**GigaDl** is a library wich helps you search and download video/songs/whatever
from popular websites.

The library is splitted in two parts: `Downloaders` and `Providers` and is really extensible.


# Supported providers

There are only two providers currently supported:

 * MegaVideo
 * Vimeo (no search available)


# Usage

First, you need a `downloader`:

```python
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
gigadl.register_providers(FooProvider(downloader), BarProvider(downloader),
                         foobar=FooProvider(downloader))
gigadl.use('MegaDl')
```

Here, we chose to download content from MegaVideo, using the urllib2 downloader
we just created.


# API

The main methods are `search(terms)` and `retrieve_data(url)`, they are the
only methods available in all the providers.

```python
provider = MegaDl(Urllib2Downloader())
gigadl = GigaDl(provider)

# the search(terms) method performs a ... search!
results = gigadl.search('daft punk') # returns a list of MegaResult objects

# and the retrieve_data(url) returns all the data that a provider can find for an url
data = gigadl.retrieve_data(results[0].play_url)
print 'The "%s" item can be downloaded here: %s' % (data, data.url)
```

Even if these two methods are enough to use GigaDl, there are a few more:

```python
gigadl.register_provider(myNewProvider) # adds the given provider to the usable providers
gigadl.register_provider(myNewProvider, 'yet another provider') # same, but with a specific name
gigadl.register_providers(myFirstProvider, otherProvider, kewl_provider=myKewlProvider) # same, but with an arguments list and named arguments
gigadl.use('SomeProviderName') # selects the provider to use for the next calls to search() or retrieve_data()
gigadl.use(someProviderObject')
gigadl.provider = MegaDl(Urllib2Downloader())   # same, but directly with an object
gigadl.provider = 'SomeProviderName'            # also works
gigadl.provider                                 # returns the provider object in use
```


# Licence

**GigaDl** is under MIT/Expat licence (see the LICENCE file).
