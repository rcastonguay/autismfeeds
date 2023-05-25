import feedparser
from feedgen.feed import FeedGenerator
from dateutil import parser
from dateutil import tz
from pytz import timezone
import re


# Define a custom time zone mapping for EDT
tzinfos = {"PST": tz.gettz("America/Los_Angeles"), "EDT": tz.gettz("America/New_York")}


feeds = [
    'https://vancouversun.com/feed/?x=1',
    'https://rss.cbc.ca/lineup/canada-britishcolumbia.xml',
    'https://rss.cbc.ca/lineup/topstories.xml',
    'https://www.thestar.com/content/thestar/feed.RSSManagerServlet.articles.topstories.rss',
    'https://www.thestar.com/content/thestar/feed.RSSManagerServlet.articles.vancouver.rss',
    'http://www.thestar.com/content/thestar/feed.RSSManagerServlet.articles.news.rss',
    'https://vancouverisland.ctvnews.ca/rss/ctv-vancouver-island-latest-news-1.1245414',
    'https://montreal.ctvnews.ca/rss/ctv-news-montreal-1.822366',
    'http://feeds2.feedburner.com/fluxdudevoir',
    'https://www.lapresse.ca/manchettes/rss',
    'http://ctvnews.ca/rss/TopStories',
    'https://www.ctvnews.ca/rss/ctvnews-ca-canada-public-rss-1.822284',
    'https://vancouverisland.ctvnews.ca/rss/ctv-vancouver-island-latest-news-1.1245414',
    'https://globalnews.ca/feed/',
        ]

keywords = ['autism', 'autistic', 'autisme', 'autistique', 'asperger']

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
            date = parser.parse(entry.published, fuzzy=True, tzinfos=tzinfos)
            if date.tzinfo is None or date.tzinfo.utcoffset(date) is None:
                date = date.replace(tzinfo=tz.gettz('UTC')).astimezone(tz.gettz('PST'))
            else:
                date = date.astimezone(tz.gettz('PST'))
            fe.pubDate(date)

# Generate the RSS feed XML file.
rssfeed = fg.rss_str(pretty=True)
print(rssfeed.decode())
