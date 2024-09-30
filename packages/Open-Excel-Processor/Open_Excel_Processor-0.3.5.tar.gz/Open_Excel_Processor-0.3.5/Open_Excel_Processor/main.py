from pymongo import MongoClient
from datetime import datetime

def Verify_Data(new_data, value):
    # Connect to MongoDB
    client = MongoClient("mongodb+srv://cobraauthor:Lsnvsedyrluac0z8@cluster0.bfxwo.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")

    # Send a ping to confirm a successful connection
    try:
        client.admin.command('ping')
        # Access the database and collection
        db = client['verify_excel']  # Your database name
        collection = db['collection001']  # Your collection name

        # Get the current date and time
        current_time = datetime.now()  # Get current date and time
        formatted_time = current_time.strftime('%Y-%m-%d %H:%M:%S')  # Format it as a string

        if value == "Short":
            # Find the first document
            first_document = collection.find_one()
            if first_document:
                first_id = first_document['_id']  # Get the first document's ID

                # Prepare the update data as a dictionary for the first document
                update_data_first = {
                    "timestamp": formatted_time,
                    "short_data": new_data
                }

                # Replace the existing document using the first document's ID
                result_first = collection.replace_one({"_id": first_id}, update_data_first)  # Replace by ID
                
        elif value == "Long":
            # Find the second document
            second_document = collection.find_one(skip=1)  # Skip the first document to get the second
            if second_document:
                second_id = second_document['_id']  # Get the second document's ID

                # Prepare the update data as a dictionary for the second document
                update_data_second = {
                    "timestamp": formatted_time,
                    "long_data": new_data
                }

                # Replace the existing document using the second document's ID
                result_second = collection.replace_one({"_id": second_id}, update_data_second)  # Replace by ID
               

    except Exception as e:
        print("An error occurred:", e)

    finally:
        # Close the client connection
        client.close()

    return True
