from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import os
import dotenv

dotenv.load_dotenv()

URI = os.getenv("DATABASE_URI")
client = MongoClient(URI, server_api=ServerApi("1"))
# Send a ping to confirm a successful connection
try:
    client.admin.command("ping")
    print("Pinged your deployment. You successfully connected to MongoDB!")
except Exception as e:
    print(e)

db = client.get_database("MobaLegends")
scrims_collection = db.Scrims  # collection: Scrims
teams_collection = db.Teams  # collection: Teams
members_collection = db.Members  # collection: Members
