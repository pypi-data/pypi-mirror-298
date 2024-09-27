from pymongo import MongoClient
from pymongo.errors import (
    OperationFailure, AutoReconnect, ConnectionFailure, ConfigurationError, 
    CursorNotFound, DuplicateKeyError, ExceededMaxWaiters, ExecutionTimeout, 
    InvalidOperation, InvalidURI, NetworkTimeout, NotMasterError, PyMongoError
)

class MongoDBAuth:
    def __init__(self, uri, db_name, username=None, password=None):
        """Initialize MongoDB client with optional authentication."""
        self.uri = uri
        self.db_name = db_name
        self.username = username
        self.password = password
        self.client = None
        self.db = None
        self.connect()

    def connect(self):
        """Connect to MongoDB using credentials if provided."""
        try:
            if self.username and self.password:
                self.client = MongoClient(self.uri, username=self.username, password=self.password)
            else:
                self.client = MongoClient(self.uri)
                
            # Access the database
            self.db = self.client[self.db_name]
            print(f"Connected to MongoDB database: {self.db_name}")
        
        except (ConnectionFailure, ConfigurationError, PyMongoError) as e:
            print(f"Error connecting to MongoDB: {e}")

    def get_collection(self, collection_name):
        """Get a MongoDB collection."""
        try:
            return self.db[collection_name]
        except PyMongoError as e:
            print(f"Error retrieving collection: {e}")
    
    def fetch_data(self, collection_name):
        """Fetch all data from a MongoDB collection."""
        try:
            collection = self.get_collection(collection_name)
            data = list(collection.find())
            print(f"Fetched {len(data)} records from {collection_name}")
            return data
        except CursorNotFound:
            print("Cursor not found error while fetching data")
        except PyMongoError as e:
            print(f"Error fetching data: {e}")
    
    def insert_data(self, collection_name, data):
        """Insert a document into a MongoDB collection."""
        try:
            collection = self.get_collection(collection_name)
            result = collection.insert_one(data)
            print(f"Data inserted successfully with ID: {result.inserted_id}")
        except DuplicateKeyError:
            print("Duplicate key error when inserting data")
        except PyMongoError as e:
            print(f"Error inserting data: {e}")

    def authenticate_user(self, username, password):
        """Authenticate against MongoDB user account."""
        try:
            self.client = MongoClient(self.uri, username=username, password=password)
            self.db = self.client[self.db_name]
            print(f"User {username} authenticated successfully")
        except OperationFailure:
            print("Authentication failed")
        except PyMongoError as e:
            print(f"Authentication error: {e}")
    
    def close_connection(self):
        """Close the connection to the MongoDB server."""
        if self.client:
            self.client.close()
            print("MongoDB connection closed")

