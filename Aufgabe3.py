from pymongo import MongoClient
from bson.son import SON
import re

client = MongoClient("mongodb://localhost:27017/")
db = client["restaurants"]
collection = db["restaurants"]

def show_unique_boroughs():
    print("Stadtbezirke (ohne Duplikate):")
    boroughs = collection.distinct("borough")
    for borough in boroughs:
        print(" -", borough)

def show_top_3_restaurants_by_rating():
    print("\nTop 3 Restaurants nach Durchschnitts-Score:")

    pipeline = [
        {"$unwind": "$grades"},
        {"$group": {
            "_id": "$name",
            "avg_score": {"$avg": "$grades.score"}
        }},
        {"$sort": SON([("avg_score", -1)])},
        {"$limit": 3}
    ]

    results = collection.aggregate(pipeline)
    for r in results:
        print(f"{r['_id']} - Ø Score: {round(r['avg_score'], 2)}")

def find_nearest_to_le_perigord():
    print("\nRestaurant am nächsten zu 'Le Perigord':")

    # Stelle sicher, dass der Geo-Index existiert
    collection.create_index([("address.coord", "2dsphere")])

    base_restaurant = collection.find_one({"name": "Le Perigord"})
    if not base_restaurant:
        print("Fehler: 'Le Perigord' wurde nicht gefunden.")
        return

    coord = base_restaurant.get("address", {}).get("coord")
    if not coord or not isinstance(coord, list) or len(coord) != 2:
        print("Fehler: 'Le Perigord' hat keine gültigen Koordinaten.")
        return

    geo_point = {
        "type": "Point",
        "coordinates": coord
    }

    try:
        nearest = collection.find_one({
            "name": {"$ne": "Le Perigord"},
            "address.coord": {
                "$near": {
                    "$geometry": geo_point
                }
            }
        })

        if nearest:
            print("Nächstgelegenes Restaurant:", nearest["name"])
            print("Adresse:", nearest["address"].get("street", "Keine Angabe"))
        else:
            print("Kein nahegelegenes Restaurant gefunden.")

    except Exception as e:
        print("Fehler bei Geo-Abfrage:", e)


def search_restaurants():
    print("\nRestaurantsuche:")
    name = input("Name enthält (optional): ").strip()
    cuisine = input("Küche enthält (optional): ").strip()

    query = {}
    if name:
        query["name"] = {"$regex": re.escape(name), "$options": "i"}
    if cuisine:
        query["cuisine"] = {"$regex": re.escape(cuisine), "$options": "i"}

    results = collection.find(query, {"name": 1, "cuisine": 1, "borough": 1}).limit(20)

    print("\nGefundene Restaurants:")
    found = False
    for r in results:
        found = True
        print(f"- {r.get('name')} | {r.get('cuisine')} | {r.get('borough')}")
    if not found:
        print("Keine Restaurants gefunden.")

if __name__ == "__main__":
    print("Restaurant Explorer (MongoDB)\n")
    show_unique_boroughs()
    show_top_3_restaurants_by_rating()
    find_nearest_to_le_perigord()
    search_restaurants()
