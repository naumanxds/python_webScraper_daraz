import csv

from datetime import datetime
from selenium import webdriver
from bs4 import BeautifulSoup
from webdriver_manager.firefox import GeckoDriverManager
from selenium.webdriver.firefox.options import Options

# constants used in code
NOT_FOUND = 'None'
INCREMENT_ONE = 1
BASE_URL = 'https://www.daraz.pk'

# create file with time attached to it for safty purposes
fHandle = open('csvFileCreatedAt-' + datetime.now().strftime('%H-%M-%S') + '.csv', 'w', encoding='utf-8')

# create browser instance
manager = GeckoDriverManager()
browserOptions = Options()
browserOptions.add_argument("--headless")
driver = webdriver.Chrome(executable_path=manager.install(), options=browserOptions)

# get html of the provided page url
def getHtml(url):
    try:
        driver.get(url)
        driver.execute_script('return document.documentElement.outerHTML')
        return BeautifulSoup(driver.page_source, 'html.parser')

    except Exception as e:
        print('     >> Error in Fetching HTML from Url => ' + url)
        print('     >> ERRROR => ' + format(e))

    return False

# write in file
def writeFile(data, url = ''):
    try:
        csvWriter = csv.writer(fHandle)
        csvWriter.writerow(data)
    except Exception as e:
        print('     >> Error in Writing Data into the file => ' + url)
        print('     >> ERRROR => ' + format(e))

# iterate through the fetched links get data
def iterateLinks(links):
    for link in links:
        html = getHtml(link)
        try:
            # product name
	        title = html.find('span', {'class' : 'pdp-mod-product-badge-title'})
	        if str(title) != NOT_FOUND:
	            title = title.get_text().strip()
	        else:
	            title = 'Title not found'

	        # prodct price
	        price = html.find('span', {'class' : 'pdp-price pdp-price_type_normal pdp-price_color_orange pdp-price_size_xl'})
	        if str(price) != NOT_FOUND:
	            price = price.get_text().split('Rs. ')[1]
	        else:
	            price = 'Price not found'

	        # breadcrums
	        breadcrum = html.find('ul', {'id' : 'J_breadcrumb'})
	        if str(breadcrum) != NOT_FOUND:
	            breadcrum = breadcrum.get_text(separator=' > ', strip=True)
	        else:
	            breadcrum = 'Breadcrums not found'

	        # details points
	        detail = html.find('div', {'class' : 'html-content pdp-product-highlights'})
	        if str(detail) != NOT_FOUND:
	        	detail = detail.get_text(separator='\n', strip=True)
	        else:
	            detail = 'Product Description points not found'

	        # product descripton
	        descripton = html.find('div', {'class' : 'html-content detail-content'})
	        if str(descripton) != NOT_FOUND:
	            descripton = descripton.get_text()
	        else:
	            descripton = 'Product Detail Description not found'

	        # product specifications
	        specifications = ''
	        specification = html.find_all('li', {'class' : 'key-li'})
	        if str(specification) != NOT_FOUND:
	            for l in specification:
	                specifications += l.find('span').get_text() + ' : ' + l.find('div').get_text() + '\n'
	        else:
	            specifications = 'Product Specifications not found'

	        # box content
	        boxContent = html.find('div', {'class' : 'box-content'})
	        if str(boxContent) != NOT_FOUND:
	            boxContent = boxContent.find('span').get_text() + ' : ' + boxContent.find('div').get_text()
	        else:
	            boxContent = 'Box Content not found'

	        # product pictures
	        pics = html.find_all('img', {'class' : 'pdp-mod-common-image item-gallery__thumbnail-image'})
	        images = []
	        if str(pics) != NOT_FOUND:
	            for l in pics:
	                images.append(l.get('src').split('.jpg_')[0] + '.jpg_400x400.jpg')
	        else:
	            images = ['Images not found']

	        # write data in file
	        writeFile([title, price, breadcrum, detail, descripton, specifications, boxContent] + images)
	        print('         	** Product Done => ' + str(link))
        except Exception as e:
            print('     >> Entry missed due to some error from this link => ' + str(link))
            print('     >> ERRROR => ' + format(e))


# input for user
siteUrl = input('Please Enter Starting Point for Scrapper: ')
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
    count = siteUrl.split('&page=')[1]
    count = int(count.split('&')[0]) + 1
except:
    count = 2

while True:
    html = getHtml(siteUrl)
    link = html.find_all('div', {'class' : 'c16H9d'})
    links = []
    for loop in link:
        links.append('https:' + loop.find('a').get('href'))

    iterateLinks(links)
    print(' >> Page Done >> ' + str(count - 1) + ' Done URL => ' + siteUrl)
    siteUrl = html.find('li', {'title' : count})
    if str(link) == NOT_FOUND or str(siteUrl) == NOT_FOUND:
        break

    siteUrl = BASE_URL + siteUrl.find('a').get('href')
    count += 1

# close file
fHandle.close()
driver.quit()
print('=== Scrapping Finished ===')