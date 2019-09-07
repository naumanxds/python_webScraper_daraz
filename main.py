import requests
import json
import urllib.request
import time
import csv

from datetime import datetime
from bs4 import BeautifulSoup

# constants used in code
NOT_FOUND = 'None'
INCREMENT_ONE = 1
SLEEP_SEC = 2

# create file with time attached to it for safty purposes
fHandle = open('csvFileCreatedAt-' + datetime.now().strftime('%H-%M-%S') + '.csv', 'w')

# write in file
def writeFile(data, url = ''):
	try:
		csvWriter = csv.writer(fHandle)
		csvWriter.writerow(data)
	except:
		print('		>> Entry missed due to some error from this link = ' + url)
		print('		>> ERRROR = ' + format(e))
		print(' 	==========')

# get html of the provided url page
def getHtml(url):
	try:
		response = requests.get(url)
	except Exception as e:
		print('Oops! Something went worng fetching the link - ' + format(e))
	return BeautifulSoup(response.text, 'html.parser')

# iterate through the fetched links get data
def iterateLinks(subLinks):
	for link in subLinks:
		data = []
		html = getHtml(link['url'])
		time.sleep(SLEEP_SEC)
			
		try:
			# product name
			fetched = html.find('span', {'class' : 'pdp-mod-product-badge-title'})
			if str(fetched) != NOT_FOUND:
				data.append(fetched.get_text().strip())
			else:
				data.append('PRODUCT NAME NOT FOUND')

			# prodct price
			fetched = html.find('span', {'class' : 'pdp-price pdp-price_type_normal pdp-price_color_orange pdp-price_size_xl'})
			if str(fetched) != NOT_FOUND:
				data.append(fetched.get_text().split('Rs. ')[1])
			else:
				data.append('PRICE NOT FOUND')

			# breadcrums
			breadcrum = ''
			fetched = html.find_all('span', {'class' : 'breadcrumb_item_text'})
			if str(fetched) != NOT_FOUND:
				for l in fetched:
					breadcrum += ' > ' + l.find('span').get_text().strip()
			else:
				breadcrum = 'BREADCRUMS NOT FOUND'

			data.append(breadcrum)

			# details points
			details = ''
			fetched = html.find('div', {'class' : 'html-content pdp-product-highlights'})
			if str(fetched) != NOT_FOUND:
				fetched = fetched.find_all('li')
				for l in fetched:
					details += ' - ' + l.get_text() + '\n'
			else:
				details = 'PRODUCT DESCRIPTION POINTS NOT FOUND'

			data.append(details)

			# product descripton
			fetched = html.find('div', {'class' : 'html-content detail-content'})
			if str(fetched) != NOT_FOUND:
				data.append(fetched.get_text())
			else:
				data.append('PRODUCT DETAIL DESCRIPTION NOT FOUND')

			# product specifications
			specKey = ''
			fetched = html.find_all('li', {'class' : 'key-li'})
			if str(fetched) != NOT_FOUND:
				for l in fetched:
					specKey += l.find('span').get_text() + ' : ' + l.find('div').get_text() + '\n'
			else:
				specKey = 'PRODUCT SPECIFICATIONS NOT FOUND'

			data.append(specKey)

			# box content
			boxContent = html.find('div', {'class' : 'box-content'})
			if str(boxContent) != NOT_FOUND:
				data.append(boxContent.find('span').get_text() + ' : ' + boxContent.find('div').get_text())
			else:
				data.append('BOX CONTENT NOT FOUND')

			# product pictures
			pics = html.find_all('img', {'class' : 'pdp-mod-common-image item-gallery__thumbnail-image'})
			if str(pics) != NOT_FOUND:
				for l in pics:
					data.append(l.get('src').split('.jpg_')[0] + '.jpg_400x400.jpg')
			else:
				data.append('IMAGES NOT FOUND')

			# write data in file
			writeFile(data)
		except Exception as e:
			print('		>> Entry missed due to some error from this link = ' + link['url'])
			print('		>> ERRROR = ' + format(e))
			print(' 	==========')


# input for user
enteredUrl = input('Please Enter Starting Point for Scrapper: ')
startUrl = enteredUrl.split('&page=')[0]
print('=== Starting Scrapping ===')
writeFile([
	'Product Name',
	'Product Price',
	'Bread Crums',
	'Detail Points',
	'Product Descripton',
	'Product Specifications',
	'Box Content',
	'Images'
])
try:
	count = enteredUrl.split('&page=')[1]
	count = int(count.split('&')[0])
except:
	count = 1

while count <= 500:
	html = getHtml(startUrl + '&page=' + str(count))
	time.sleep(SLEEP_SEC)
	parsedJson = html.find_all('script', {'type':'application/ld+json'})
	links = (json.loads(parsedJson[1].text))['itemListElement']
	if not links:
		break

	iterateLinks(links)
	print(str(count) + ' == Pages Done')
	count += INCREMENT_ONE

# close file
fHandle.close()
print('=== Scrapping Finished ===')