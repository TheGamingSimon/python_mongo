from pymongo import MongoClient
from room import Room
from bson.objectid import ObjectId

class Dao_room:
    def __init__(self, connection_string):
        self.connection_string = connection_string
        self.col = MongoClient(connection_string)["buildings"]["rooms"]

    def create(self, room):
        # Fügt einen Raum in die Collection ein
        return self.col.insert_one(room.__dict__).inserted_id

    def read(self, room_id=None):
        # Gibt ein einzelnes Room-Objekt anhand der ID zurück, oder das erste beliebige
        if room_id:
            data = self.col.find_one({"_id": ObjectId(room_id)})
        else:
            data = self.col.find_one()

        return Room(**data) if data else None

    def update(self, room_id, updated_fields):
        """
        Aktualisiert ein Room-Dokument anhand seiner ID.
        updated_fields: dict mit den Feldern, die aktualisiert werden sollen.
        """
        result = self.col.update_one(
            {"_id": ObjectId(room_id)},
            {"$set": updated_fields}
        )
        return result.modified_count

    def delete(self, room_id):
        """
        Löscht ein Room-Dokument anhand seiner ID.
        """
        result = self.col.delete_one({"_id": ObjectId(room_id)})
        return result.deleted_count
