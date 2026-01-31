# Simple in-memory database for testing
users_db = {}
watchlist_db = {}
alerts_db = {}

def get_users_collection():
    return users_db

def get_watchlist_collection():
    return watchlist_db

def get_alerts_collection():
    return alerts_db

# Mock MongoDB collections
class MockCollection:
    def __init__(self, data_dict):
        self.data = data_dict
    
    def find_one(self, query):
        for key, value in self.data.items():
            if isinstance(value, dict):
                match = True
                for q_key, q_value in query.items():
                    if value.get(q_key) != q_value:
                        match = False
                        break
                if match:
                    value["_id"] = key
                    return value
        return None
    
    def insert_one(self, document):
        import uuid
        doc_id = str(uuid.uuid4())
        self.data[doc_id] = document.copy()
        print(f"MockCollection.insert_one: Added {document} with ID {doc_id}")
        print(f"Current data after insert: {self.data}")
        return type('Result', (), {'inserted_id': doc_id})()
    
    def find(self, query=None):
        results = []
        print(f"MockCollection.find called with query: {query}")
        print(f"Current data: {self.data}")
        
        for key, value in self.data.items():
            if query is None:
                value_copy = value.copy()
                value_copy["_id"] = key
                results.append(value_copy)
            else:
                match = True
                for q_key, q_value in query.items():
                    if value.get(q_key) != q_value:
                        match = False
                        break
                if match:
                    value_copy = value.copy()
                    value_copy["_id"] = key
                    results.append(value_copy)
        
        print(f"MockCollection.find returning: {results}")
        return results
    
    def delete_one(self, query):
        for key, value in list(self.data.items()):
            match = True
            for q_key, q_value in query.items():
                if value.get(q_key) != q_value:
                    match = False
                    break
            if match:
                del self.data[key]
                return type('Result', (), {'deleted_count': 1})()
        return type('Result', (), {'deleted_count': 0})()

users_collection = MockCollection(users_db)
watchlist_collection = MockCollection(watchlist_db)
alerts_collection = MockCollection(alerts_db)