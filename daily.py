import requests
import json
import csv
import datetime
import couchdb
from BeautifulSoup import BeautifulSoup

#READ THESE FROM CONFIG
config_file = "/home/thej/.config/code_config/hopcoms.json"
config  = json.load(open(config_file))
db_full_url= config["db_full_url"]
couch = couchdb.Server(db_full_url)


all_items_load = False
all_item_list = {}
hopcoms_meta 	= couch["hopcoms_meta"]

all_item_list = hopcoms_meta["item_codes2"]
#print str(all_item_list)

hopcoms_daily 	= couch["hopcoms_daily"]

web_data_url = "http://hopcoms.karnataka.gov.in/CropRates.aspx"
total_data = {}
r = requests.get(web_data_url)
if r.status_code == 200:
	html = r.text
	soup = BeautifulSoup(html)
	date_span = soup.find(id='lblDate')
	date_span_text = date_span.text
	date_span_text = date_span_text.strip()
	#date_span_text = date_span_text.replace("Last Updated Date: ","")
	date_span_text_array = date_span_text.split("/")
	final_date = date_span_text_array[2]+date_span_text_array[1]+date_span_text_array[0]
	print str("Updating for ="+final_date)


	table = soup.find(id='grdRates')
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
			for span in th.findChildren('font'):
				row = row + 1
				#print str(span)
				if row == 3:
					continue


				content = str(span.text).strip()
				if row == 1 :
					label1 = str(content)				
				
				if row == 4:
					data1 = float(content)
					
				total_data[label1]=data1								

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
	
