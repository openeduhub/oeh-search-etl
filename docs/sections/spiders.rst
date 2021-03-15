Spider Documentation
====================


Spider Building example
-----------------------

In this example, we document how we built the kindoergarten spider.

First of all, we need to create a new spider file in the repository.

Then we add the very basic skeleton for testing:

.. code-block:: python

    class KindoergartenSpider(scrapy.Spider):
        """
        scrapes the kindOERgarten wordpress.
        this wordpress instance has no json api enabled, so we go by sitemap
        https://kindoergarten.wordpress.com/sitemap.xml
        """
        name = 'kindoergarten_spider'
        start_urls = ['https://kindoergarten.wordpress.com/sitemap.xml']

        def parse(self, response: scrapy.http.XmlResponse, **kwargs): ...

The start_url parameter will be used by scrapy for the initial request.
Once the request completes, scrapy will call the parse function with the result.
Since we just received a sitemap, we'll parse that and instruct scrapy to grab all the urls we just collected.
As somebody else already had implemented the parsing of the sitemap (converter.util.sitemap), we'll just use that.

The single elements look like this, just so you can get a feel for what we are working with

.. code-block:: xml

    <url>
        <loc>https://kindoergarten.wordpress.com/2017/10/20/wuerfelblatt-trauben-bis-3-0047/</loc>
        <mobile:mobile/>
        <image:image>
        <image:loc>https://kindoergarten.files.wordpress.com/2017/08/ankuendigung-wuerfelblatt_trauben_bis3.jpg</image:loc>
        <image:title>Ankuendigung-Wuerfelblatt_Trauben_bis3</image:title>
        </image:image>
        <lastmod>2018-05-29T20:47:12+00:00</lastmod>
        <changefreq>monthly</changefreq>
    </url>


.. code-block:: python

    def parse(self, response: scrapy.http.XmlResponse, **kwargs):
        items = from_xml_response(response)
        for item in items:
            yield response.follow(item.loc, callback=self.parse_site, cb_kwargs={'sitemap_entry': item})

Now, parse just has the single responsibility of extracting the sites that are listed in the sitemap.
But since we want tha content stored there, we have to create another parser function that uses the newly created response.

So, to dissect the response.follow call:

.. code-block:: python

    yield response.follow(
      # the url to request
      item.loc,
      # the function that will be called with the response
      callback=self.parse_site,
      # additional data that we want to give that function
      cb_kwargs={'sitemap_entry': item})

That means, our new function will look like this:

.. code-block:: python

    def parse_site(self, response, sitemap_entry): ...

The parse_site function will handle reading all the important information, so it will be quite long.
For a little testing we can just use some simple things:

.. code-block:: python

    def parse_site(self, response, sitemap_entry):
        thumbnail = response.css('.post-thumbnail img::attr(src)').get()
        title: str = response.css('.entry-title span::text').get()
        descr = response.css('.entry-content p::text').get()
        yield {'title': title, 'thumbnail': thumbnail, 'description': descr}

The dictionary will be put through the pipelines and will eventually end up in edu-sharing.
But not just, yet.
There's more data to filter out of the website and metadata to collect.
And we want the data to be in a very specific format that the pipeline understands.
To hopefully simplify that, we built the LOMBase class.

To use it, we add it to the inherited classes of our Spider.
And we add the getId and getHash methods, they very important to the LOMBase class.

.. code-block:: python

    class KindoergartenSpider(scrapy.Spider, LomBase):
        def getId(self, response) -> str:
            pass

        def getHash(self, response) -> str:
            pass

These methods are there to check if an item is already present in the edu-sharing database.
The id must be unique to the crawled site and should be the same even if something in the page changed.
So here, we use the path of the website, that we get from urllib.parse.urlparse.

For the hash we should use something that we can compare to if the site changed, so the modification date would be nice.
That is stored in sitemap_entry.lastmod, but not in the response.
But the getHash function only receives response for the input,
so we have to attach it to the response, before getHash is called.

.. code-block:: python

    def parse_site(self, response, sitemap_entry):
        response.meta['sitemap_entry'] = sitemap_entry

    def getHash(self, response) -> str:
        return self.getId(response) + response.meta['sitemap_entry'].lastmod

    def getId(self, response) -> str:
        return parse.urlparse(response.meta['sitemap_entry'].loc).path

With that done, we can finally get to populating all the other fields to complete the item.



Base Classes
------------

.. automodule:: converter.spiders.base_classes.lom_base
   :members:
   :private-members:

.. automodule:: converter.spiders.base_classes.mediawiki_base
   :members:
   :private-members:

