import requests
import json
import csv
import datetime
import couchdb

#READ THESE FROM CONFIG
config_file = "/home/thej/.config/code_config/hopcoms.json"
config  = json.load(open(config_file))
db_full_url= config["db_full_url"]
couch = couchdb.Server(db_full_url)


all_items_load = False
hopcoms_meta 	= couch["hopcoms_meta"]

#all_item_list = {}
# with open('item_list.csv', "r") as csv_file:
#     reader = csv.reader(csv_file)
#     header = True
#     for row in reader:
#         if header:
#             header = False
#             continue
#         label = (row[1]).strip()
#         label =	label.replace(" ","")
#         label = label.lower()
#         all_item_list[label]=int(row[0])

# try:
#     if hopcoms_meta["item_codes"]:
#         pass
# except couchdb.http.ResourceNotFound:
#         print "add"
#         all_item_list["_id"]="item_codes"
#         print str(all_item_list)
#         hopcoms_meta.save(all_item_list)


#all_item_list = {}
# with open('item_list2.csv', "r") as csv_file:
#     reader = csv.reader(csv_file)
#     header = True
#     for row in reader:
#         if header:
#             header = False
#             continue
#         label = (row[1]).strip()
#         label =	label.replace(" ","")
#         label = label.lower()
#         all_item_list[label]=int(row[0])

# try:
#     if hopcoms_meta["item_codes2"]:
#         pass
# except couchdb.http.ResourceNotFound:
#         print "add"
#         all_item_list["_id"]="item_codes2"
#         print str(all_item_list)
#         hopcoms_meta.save(all_item_list)


item_details_all = {}
with open('item_details3.csv', "r") as csv_file:
    reader = csv.reader(csv_file)
    header = True
    for row in reader:
        if header:
            header = False
            continue
        insertRow = {}
        insertRow["name_en"] = row[1]
        insertRow["name_kn"] = row[2]
        item_details_all[row[0]] = insertRow

try:
    if hopcoms_meta["item_details3"]:
        pass
except couchdb.http.ResourceNotFound:
        print("add")
        item_details_all["_id"]="item_details3"
        print(item_details_all)
        hopcoms_meta.save(item_details_all)
