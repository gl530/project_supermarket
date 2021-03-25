from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
import selenium.common.exceptions as exception
import csv
import pandas as pd
import time

def get_prices(link,category):
	chrome_options = Options()
	chrome_options.add_argument("--headless")
	driver = webdriver.Chrome(options=chrome_options)
	driver.get(link)
	driver.implicitly_wait(10)
	wait = WebDriverWait(driver, 5)
	wait.until(EC.presence_of_element_located((By.XPATH, "//*[@id='tSr']/div/div[2]/button")))

	cookie_alert = driver.find_element_by_xpath("/html/body/div[3]/div/div/div/section/div[2]/button[1]")
	action = ActionChains(driver)
	action.click(on_element = cookie_alert)
	action.perform()

	length = {}
	data = {'names':[],
			'prices':[],
			'sizes':[],
			'links':[],
			'offers':[],
			'offer_flags':[]}


	while True:
		try:
			action = ActionChains(driver)
			load_more = driver.find_element_by_xpath("//*[@id='tSr']/div/div[2]/button")
			action.click(on_element = load_more)
			action.perform()
			time.sleep(.100)
		except exception.NoSuchElementException:
			print(category, 'reached end of page. There are no more items to be loaded.')
			break

	try:	
		prod_names = driver.find_elements_by_xpath('//article[@data-test="product-pod"]')
		for n in prod_names:
			data['names'].append(n.get_attribute('data-product-name'))
		length['names'] = len(data['names'])
	except:
		print('error in extracting ', category, ' names')

	try:
		prod_prices = driver.find_elements_by_xpath('//article[@data-test="product-pod"]/div/section[2]/div/span/span')
		for p in prod_prices:
			data['prices'].append(p.text)
			print(p)
		length['prices'] = len(data['prices'])
		print(category, 'prices', data['prices'][:20], length['prices'])
	except:
		print('error in extracting ', category, ' prices')

	try:
		prod_sizes = driver.find_elements_by_xpath('//article[@data-test="product-pod"]/div/section/header/a/span')
		for s in prod_sizes:
			data['sizes'].append(s.text)
			print(s)
		length['sizes'] = len(data['sizes'])
		print(category, 'sizes', data['sizes'][:20], length['sizes'])
	except:
		print('error in extracting ', category, ' sizes')

	try:
		prod_links = driver.find_elements_by_xpath('//article[@data-test="product-pod"]/div/section/header/a')
		for l in prod_links:
			data['links'].append(l.get_attribute('href'))
		length['links'] = len(data['links'])
	except:	
		print('error in extracting ', category, ' links')

	try:
		prod_offers = driver.find_elements_by_xpath('//article[@data-test="product-pod"]/div/section/div[3]/div/div/a/p/span')
		for o in prod_offers:
			data['offers'].append(o.text)
	except:	
		print('error in extracting ', category, ' offers')

	try:
		prod_offer_flags = driver.find_elements_by_xpath('//article[@data-test="product-pod"]')
		for f in prod_offer_flags:
			data['offer_flags'].append(f.get_attribute('data-product-on-offer'))
		length['offer_flags'] = len(data['offer_flags'])
	except:
		print('error in extracting ', category, ' offer_flags')

	# product data including name, price, size and link to product details are saved in one csv file if they are of same length; 
	# otherwise individual data are saved in separate files, and cleaned manually in notebook.
	
	if len(set(length.values())) == 1:
		print('number of values for all fields ex offer are the same')

		filename_exoffer = '../data/wt_raw/'+ category + '_exoffer.csv'
		filename_offer = '../data/wt_raw/'+ category + '_offer.csv'
		
		with open(filename_exoffer, 'w') as f:
			datawriter = csv.writer(f, delimiter='|')
			for i in range(length['names']):
				datawriter.writerow([data['names'][i], data['prices'][i], data['sizes'][i], data['links'][i], data['offer_flags'][i]])
			f.close()
		print(filename_exoffer, 'created')

		with open(filename_offer, 'w') as o:
			datawriter = csv.writer(o, delimiter='|')
			for i in range(len(data['offers'])):
				datawriter.writerow([data['offers'][i]])
			o.close()
		print(filename_offer, 'created')

	else:

		for k,v in data.items():
			filename = '../data/wt_raw/'+ category + '_' + k + '.csv'

			with open(filename, "w") as f:
				datawriter = csv.writer(f, delimiter='|')
				datawriter.writerow(v)
				f.close()
			print(filename, ' created.')

	driver.quit()


if __name__ == '__main__':

	link = 'https://www.waitrose.com/ecom/shop/browse/groceries/'
	categories = ['pet','fresh_and_chilled','bakery','frozen','food_cupboard','tea_coffee_and_soft_drinks',
	'beer_wine_and_spirits','toiletries_health_and_beauty','household','baby_child_and_parent',
	'kitchen_dining_and_home']

	for category in categories:
		get_link = link + category
		get_prices(get_link,category)
		print(category, ' completed')
