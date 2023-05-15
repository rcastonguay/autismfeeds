import feedparser
from feedgen.feed import FeedGenerator
from dateutil import parser
from pytz import timezone
import re

feeds = [
    'https://vancouversun.com/feed/?x=1',
    'https://rss.cbc.ca/lineup/canada-britishcolumbia.xml',
    'https://rss.cbc.ca/lineup/topstories.xml'
]

keywords = ['autism', 'autistic']

# Create a new feed generator object.
fg = FeedGenerator()
fg.title('Good autism resources')
fg.link(href='https://rcastonguay.github.io/autismfeeds/index.xml', rel='self')
fg.description('An RSS feed filtered by autism keywords.')

for feed in feeds:
    d = feedparser.parse(feed)
    for entry in d.entries:
        if any(keyword in entry.title.lower() or keyword in entry.summary.lower() for keyword in keywords):
            fe = fg.add_entry()
            fe.title(entry.title)
            fe.link(href=entry.link)
            date = parser.parse(entry.published)
            if date.tzinfo is None or date.tzinfo.utcoffset(date) is None:
                date = timezone('UTC').localize(date)
            else:
                date = date.astimezone(timezone('UTC'))
            fe.pubDate(date)

# Generate the RSS feed XML file.
rssfeed = fg.rss_str(pretty=True)
print(rssfeed.decode())
