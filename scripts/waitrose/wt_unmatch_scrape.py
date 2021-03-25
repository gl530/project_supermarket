from wt_proddesc_offer import get_prod_page_details
import pandas as pd
import csv

products_to_match = pd.read_csv('../data/processed/products_to_match_8.csv', sep='|', header=0)
links = list(products_to_match['link'])
links = list(set(links))
row_to_write = []
counter = 0

with open('../data/wt_raw/prod_page_details_8.csv','w') as f:
	csvwriter = csv.writer(f,delimiter='|')
	csvwriter.writerow(['link', 'prod_desc', 'mktg_desc', 'offer'])
	f.close()

for link in links:
	row_to_write = []
	row_to_write.append(link)
	try:
		proddesc_offer = get_prod_page_details(link)
	except:
		proddesc_offer = ('','','')

	for item in proddesc_offer:
		row_to_write.append(item)

	with open('../data/wt_raw/prod_page_details_8.csv','a') as f:
		csvwriter = csv.writer(f,delimiter='|')
		csvwriter.writerow(row_to_write)
		f.close()

	print(counter, link)
	counter += 1
