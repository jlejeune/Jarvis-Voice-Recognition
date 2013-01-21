#!/usr/bin/python
# -*- coding: utf-8 -*-

from xml.dom import minidom
from httpGET import httpGET


class Feed:
    def __init__(self, url):
        self.url = url

    def body(self):
        get = httpGET(self.url)
        file_feed = get._page.read()
        file_xml = minidom.parseString(file_feed)

        # get item node
        item_node = file_xml.getElementsByTagName("item")

        # define output body
        output = list()

        for item in item_node:
            # init one body per item
            body = dict()
            # get title
            title = item.childNodes[1]
            body[title.tagName] = title.firstChild.data

            # get link
            #link = item.childNodes[3]
            #body[link.tagName] = link.firstChild.data

            # get description
            description = item.childNodes[5]
            body[description.tagName] = description.firstChild.data

            # get date
            date = item.childNodes[7]
            body[date.tagName] = date.firstChild.data

            # append body in output variable
            output.append(body)

        return output


if __name__ == "__main__":
    #feed = Feed('http://www.transilien.com/flux/rss/traficLigne?codeLigne=A')
    feed = Feed('http://www.transilien.com/flux/rss/traficLigne')
    print feed.body()
