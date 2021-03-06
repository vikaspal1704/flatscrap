#!/usr/bin/python

import sys
import feedparser
import simplejson
from FlatScrape import *

class BatchScrape :
	
	def __init__(self,rss,limit=10):
		self.rss = rss
		self.limit = limit
	
	def scrape(self) :
		d = feedparser.parse(self.rss)
		self.title = d.feed.title
		e = d['entries']
		self.urls=[]
		self.fs=[]
		for k in range(0,min(len(e),self.limit)) :
			url = e[k].links[0].href
			self.urls.append(url)
			f = FlatScrape(url)
			f.scrape()
			self.fs.append(f)
	
	def outJs(self,file) :
		items = []
		for k in range(0,len(self.fs)):
			fs = self.fs[k]
			latlong = str(fs.lat) + "," + str(fs.lng)
			if fs.place=='':
				items.append({'type':'Flat','label':fs.title,'description':fs.description,'email':fs.email,'address':fs.location,'imageURL':fs.image})
			else:
				items.append({'type':'Flat','label':fs.title,'description':fs.description,'email':fs.email,'address':fs.place,'location':fs.location,'addressLatLng':latlong,'imageURL':fs.image})
		json = {"items":items}
		f = open(file,'w')
		simplejson.dump(json,f),
		f.close()


bs = BatchScrape(sys.argv[1],limit=50)
bs.scrape()
bs.outJs(sys.argv[2])

