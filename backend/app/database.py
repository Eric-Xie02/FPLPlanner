from motor.motor_asyncio import AsyncIOMotorClient

# Connect to your local MongoDB server
client = AsyncIOMotorClient("mongodb://localhost:27017")

# Use (or create) the 'fpl_planner' database
db = client.fpl_planner
