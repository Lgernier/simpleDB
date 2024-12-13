import copy

class InMemoryDB:
    def __init__(self):
        self.transaction_active = False
        self.comit_DB = {}
        self.editor_DB = {}

    def begin_transaction(self):
        if self.transaction_active:
            print("Finish this one first")
            return
        self.editor_DB = copy.deepcopy(self.comit_DB)
        self.transaction_active = True

    def get(self, key):
        try:
            return self.comit_DB[key]
        except KeyError:
            print("value does not exist")

    def put(self, key, val):
        if not self.transaction_active:
            print("No active transaction to commit")
            return
        
        self.editor_DB[key] = val


    
    def commit(self):
        if not self.transaction_active:
            print("No active transaction to commit")
            return
        self.comit_DB = copy.deepcopy(self.editor_DB)
        self.transaction_active = False
  
    def rollback(self):
        if not self.transaction_active:
            print("No active transaction to rollback")
            return
        self.transaction_active = False

if __name__ == "__main__":
    db = InMemoryDB()

    # Test: Begin transaction
    db.begin_transaction()

    # Test: Put some values in the transaction (not visible yet)
    db.put("key1", 100)
    db.put("key2", 200)

    # Test: Get values (not committed yet, so will show the original state)
    print(db.get("key1"))  # Output: None (since not committed)
    print(db.get("key2"))  # Output: None

    # Test: Commit the transaction
    db.commit()

    # Test: Get values after commit (should be visible now)
    print(db.get("key1"))  # Output: 100
    print(db.get("key2"))  # Output: 200

    # Test: Begin another transaction
    db.begin_transaction()

    # Test: Put a new value in the transaction (not committed yet)
    db.put("key3", 300)

    # Test: Rollback the transaction (key3 should disappear)
    db.rollback()

    # Test: Get after rollback (key3 should not exist)
    print(db.get("key3"))  # Output: None