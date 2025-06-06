from pymongo import MongoClient
from bson.objectid import ObjectId

connection_string = "mongodb://localhost:27017/"
client = MongoClient(connection_string)

print("Databases")
db_list = client.list_database_names()
for db in db_list:
    print(" - " + db)

database = input("Select Database: ")
db = client[database]

print(f"\n{database}\n")
print("Collections")
collist = db.list_collection_names()
for col in collist:
    print(" - " + col)

collection = input("Select Collection: ")
col = db[collection]

print(f"\n{database}.{collection}")
docs = list(col.find({}, {"_id": 1}))

print("\nDocuments")
id_map = {}
for doc in docs:
    full_id = str(doc["_id"])
    short_id = full_id[-7:]
    id_map[short_id] = full_id
    print(f" - {short_id}")

document_short_id = input("\nSelect Document: ")

if document_short_id in id_map:
    full_id = id_map[document_short_id]
    document_data = col.find_one({"_id": ObjectId(full_id)})

    print(f"\n{database}.{collection}.{full_id}\n")
    for key, value in document_data.items():
        print(f"{key}: {value}")
else:
    print("Ungültige Dokument-ID.")

input("\nPress any button to return")
