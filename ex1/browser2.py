#!/usr/bin/env python

import urllib		
from bs4 import BeautifulSoup

quote_page = 'http://syllabus.cs.manchester.ac.uk/ugt/COMP18112/page3.html'
page = urllib2.urlopen(quote_page)
soup = BeautifulSoup(page, ‘html.parser’)


