#!/usr/bin/env python

import urllib

def checkInputInt(userinput):
	try:
		int(userinput)
	except ValueError:
		print False
	else:
		print True

def openPage(webpage):

	url = webpage
	data = urllib.urlopen(url)
	tokens  = data.read().split()

	startPrinting = False
	addLink = False
	numberOfLinks = 1
	linksInPage = []


	for token in tokens :
		if startPrinting:
			### Print type heading
			if token == '<h1>':
				print 'HEADING: ',
			elif token == '<p>':
				print 'PARAGRAPH: ',
			### Print bold text ###
			elif token == '<em>':
				print '\033[1m',
			elif token == '</em>':
				print '\033[0;0m'
			### Stop printing when title is finished ###
			elif token == '</title>':
				print '\n'
				startPrinting = False
			elif token.startswith('</'):
				print '\033[0;0m'
			elif token.startswith('<a'):
				print '\033[4m',
				startPrinting = False
				addLink = True
			elif token == '</a>':
				print '\033[0;0m',
			else:
				print token,
		if addLink:
			if token.startswith('href'):
				linksInPage.append(token.split('"')[1])
				startPrinting = True
				addLink = False
		if token == '<title>':
				print 'Page title: ',
				startPrinting = True
		if token == '<body>':
				startPrinting = True

	for link in linksInPage:
		print str(numberOfLinks) + ' : ',
		print link
		numberOfLinks +=1
	
	linkChosen = raw_input('Enter number of link: ')
	while linkChosen.isdigit() == False or int(linkChosen) >= numberOfLinks or int(linkChosen) <= 0:
		linkChosen = raw_input('Not a link, enter number of link: ')
	if linksInPage[int(linkChosen) -1].startswith('.'):
		link =  url.rsplit('/', 1)[0] + linksInPage[int(linkChosen) -1].split('.', 1)[1]
	else:
		link = linksInPage[int(linkChosen) -1]
	openPage(link)
	
##Open on page 3##
openPage('http://syllabus.cs.manchester.ac.uk/ugt/COMP18112/page3.html') 

myMessage = raw_input('Which link would you like to navigate to: ')

