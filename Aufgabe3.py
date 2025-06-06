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
    print("\n⭐ Top 3 Restaurants nach Durchschnitts-Score:")

    pipeline = [
        {"$unwind": "$grades"},
        {"$group": {
            "_id": "$name",
            "avg_score": {"$avg": "$grades.score"},
            "address": {"$first": "$address"}
        }},
        {"$sort": SON([("avg_score", -1)])},
        {"$limit": 3}
    ]

    results = collection.aggregate(pipeline)
    for r in results:
        print(f"{r['_id']} - Ø Score: {round(r['avg_score'], 2)}")

def find_nearest_to_le_perigord():
    print("\nRestaurant am nächsten zu 'Le Perigord':")

    base_restaurant = collection.find_one({"name": "Le Perigord"})
    if not base_restaurant or "address" not in base_restaurant or "coord" not in base_restaurant["address"]:
        print("Fehler: 'Le Perigord' nicht gefunden oder ohne Koordinaten.")
        return

    coordinates = base_restaurant["address"]["coord"]

    nearest = collection.find_one({
        "name": {"$ne": "Le Perigord"},
        "address.coord": {
            "$near": coordinates
        }
    })

    if nearest:
        print("Nächstgelegenes Restaurant:", nearest["name"])
        print("Adresse:", nearest["address"].get("street", "Keine Angabe"))
    else:
        print("Kein nahes Restaurant gefunden.")

def search_restaurants():
    print("\nRestaurantsuche")
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
