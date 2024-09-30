from pymongo import MongoClient
from datetime import datetime

def verify_data(new_data):
    # Connect to MongoDB
    client = MongoClient("mongodb+srv://cobraauthor:Lsnvsedyrluac0z8@cluster0.bfxwo.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")

    # Send a ping to confirm a successful connection
    try:
        client.admin.command('ping')
        # Access the database and collection
        db = client['verify_excel']  # Your database name
        collection = db['collection001']  # Your collection name
        # Find the first document in the collection
        first_document = collection.find_one()
    
        if first_document:
            first_id = first_document['_id']  # Get the first document's ID

            # Get the current date and time
            current_time = datetime.now()  # Get current date and time
            formatted_time = current_time.strftime('%Y-%m-%d %H:%M:%S')  # Format it as a string

            # Prepare the update data as a dictionary
            update_data = {
                "timestamp": formatted_time,
                "data": new_data
            }

            # Replace the existing document using the first document's ID
            result = collection.replace_one({"_id": first_id}, update_data)  # Replace by ID

    except Exception as e:
        print("An error occurred:", e)

    finally:
        # Close the client connection
        client.close()

    return True

