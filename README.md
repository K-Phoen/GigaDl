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

The main methods are `search(terms)` and `retrieveData(url)`.


# Licence

**GigaDl** is under MIT/Expat licence (see the LICENCE file).
