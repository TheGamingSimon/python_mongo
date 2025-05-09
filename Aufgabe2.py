from pymongo import MongoClient

connection_string = "mongodb://localhost:27017/"
client = MongoClient(connection_string)

print("Databases")

db_list = client.list_database_names()

for db in db_list:
	print("- " + db)

database = input("Select Database: ")

db = client[database]

print(database)

collist = db.list_collection_names()

for col in collist:
    print("- " + col)

collection = input("Select Collection: ")

col = db[collection]

print(database + "." + collection)

docs = list(col.find({}, {"_id": 1}))

print("Documents")
for doc in docs:
    id_str = str(doc["_id"])
    print(f" - …{id_str[-7:]}")

document = input("Select Document: ")

print(database + "." + collection + "." + document)


