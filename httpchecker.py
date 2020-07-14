import requests
import string
from html.parser import HTMLParser

class CustomPetitionParser(HTMLParser):
	def __init__(self):
		self._recorder = False
		self.output = []
		self._parentName = ""
		super().__init__()

	def recordCheck(self, attrs, tag):
		if (self._recorder == False):
			if (tag == self._parentName):
				self._recorder = False
				return
		
		for item in attrs:
			if ('class' in item):
				switcher = {
					'petition_votes_status': True,
					'votes_status_label': True
				}
				self._recorder = switcher.get(item[1], False)
				
		if (tag == 'h1'):
#			print('h1 found')
			self._recorder = True	

		if (self._recorder):
			self._parentName = tag
			return				

	def handle_starttag(self, tag, attrs):
#		print(tag, attrs)
		self.recordCheck(attrs, tag)

	def handle_endtag(self, tag):
		self.recordCheck("-11", tag)

	def handle_data(self, data):
		if (self._recorder == True):
			self.output.append(data.strip())

def uaPetitionCheck(urllink):
	content = requests.get(urllink)
	if (content.status_code != 200):
		print("UA Petition Check Status For: ", urllink, " is failed")
	else:
		parser = CustomPetitionParser()
		parser.feed(content.content.decode("utf-8"))
		print("UA Petition Check Status For: ", urllink, ' '.join(parser.output))

uaPetitionCheck("https://petition.president.gov.ua/petition/92038")
