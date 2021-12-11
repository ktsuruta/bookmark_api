import pprint
import bookmarks_parser

bookmarks = bookmarks_parser.parse("data/bookmarks.html")
pprint.pprint(bookmarks)