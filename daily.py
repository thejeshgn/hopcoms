import requests
import json
import csv
import datetime
import couchdb
from BeautifulSoup import BeautifulSoup

all_items_load = False

all_item_list = {}
db_full_url= ""
couch = couchdb.Server(db_full_url)
hopcoms_meta 	= couch["hopcoms_meta"]

if all_items_load:
	with open('item_list.csv', "r") as csv_file:
		reader = csv.reader(csv_file)
		header = True
		for row in reader:
			if header:
				header = False
				continue
			label = (row[1]).strip()
			label =	label.replace(" ","")
			label = label.lower()
			all_item_list[label]=int(row[0])

	try:
		if hopcoms_meta["item_codes"]:
			pass
	except couchdb.http.ResourceNotFound:
			print "add"
			all_item_list["_id"]="item_codes"

	print str(all_item_list)
	hopcoms_meta.save(all_item_list)
else:
	all_item_list = hopcoms_meta["item_codes"]
	#print str(all_item_list)



hopcoms_daily 	= couch["hopcoms_daily"]



web_data_url = "http://www.hopcoms.kar.nic.in/(S(vks0rmawn5a2uf55i2gpl3zo))/RateList.aspx"
table_x_path ="""//*[@id="ctl00_LC_grid1"]"""
total_data = {}
r = requests.get(web_data_url)
if r.status_code == 200:
	html = r.text
	soup = BeautifulSoup(html)
	date_span = soup.find(id='ctl00_LC_DateText')
	date_span_text = date_span.text
	date_span_text = date_span_text.strip()
	date_span_text = date_span_text.replace("Last Updated Date: ","")
	date_span_text_array = date_span_text.split("/")
	final_date = date_span_text_array[2]+date_span_text_array[1]+date_span_text_array[0]
	print str("Updating for ="+final_date)


	table = soup.find(id='ctl00_LC_grid1')
	#print str(table)
	for tr in table:
		if str(tr).strip() == "":
			continue
		if len(tr.findChildren('th')) > 0:
			continue
		#six elements	
		row = 0
		row_data = {}
		label1 =""
		data1=0
		label2 =""
		data2=0

		for th in tr.findChildren('td'):			
			for span in th.findChildren('span'):
				content = str(span.text).strip()

				row = row + 1
				if row == 1 or row == 4:
					continue
				if row == 2 and content != "":
					label1 = str(content)				
				if row == 3 and content != "":
					data1 = float(content)				
				
				if row == 5 and content != "":
					label2 = str(content)				
				if row == 6 and content != "":
					data2 = float(content)

		if label1.strip() != "":
			label1 = label1.replace(" ","")
			label1 = label1.lower()
			item_id = all_item_list[label1]
			total_data[item_id]=data1				
			

		if label2.strip() != "":
			label2 = label2.replace(" ","")
			label2 = label2.lower()
			item_id = all_item_list[label2]
			total_data[item_id]=data2				


dt = datetime.date.today()
_id = '{:%Y%m%d}'.format(dt)
print str(_id)
if str(final_date) == str(_id):
	print "MATCHES final_date and _id"
	total_data["_id"]=_id
	print str("----------------------------------------------------------")
	try:
		if hopcoms_daily[_id]:
			print "exists"
			x = hopcoms_daily[_id]
			print str(x["_id"])
			print str(x["_rev"])
			total_data["_rev"] = x["_rev"]						
	except couchdb.http.ResourceNotFound:
			print "add"
			total_data["_id"]=_id

	print str(total_data)
	hopcoms_daily.save(total_data)
else:
	print "DOESN'T MATCH"
	