import couchdb
import json
import time
import csv

#READ THESE FROM CONFIG
config_file = "/home/thej/.config/code_config/hopcoms.json"
config  = json.load(open(config_file))
db_full_url= config["db_full_url"]


couch = couchdb.Server(db_full_url)
hopcoms_stores 	= couch["hopcoms_stores"]

with open('hopcoms_stores.csv', "r") as csv_file:
	reader = csv.reader(csv_file)
	header = True
	for row in reader:
		if header:
			header = False
			continue
		data = {}
		store_id = row[1]
		data["store_id"] = store_id
		data["address"] = str(row[2]).replace("\n",", ")
		data["landmark"] = str(row[3]).replace("\n"," ")

		if row[4] != "":
			data["pincode"] = int(row[4])
		
		city = row[5]

		data["city"] = city
		
		if row[6] != "" and row[7] != "":
			longitude = float(row[6])
			latitude = float(row[7])

		data["opening_hours"] = row[8]

		_id = city.lower()+"-"+str(store_id)
		data["_id"] = _id
		try:
			if hopcoms_stores[_id]:
				print "exists"
				x = hopcoms_stores[_id]
				print str(x["_id"])
				print str(x["_rev"])
				data["_rev"] = x["_rev"]						
		except couchdb.http.ResourceNotFound:
				print "add"
				data["_id"]=_id

		print str(data)
		hopcoms_stores.save(data)
