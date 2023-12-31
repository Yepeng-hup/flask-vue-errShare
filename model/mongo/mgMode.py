from datetime import datetime


from .mongo import mg_col_es_text



def w():
    current_time = datetime.now()
    post = {
        "author": "Mike",
        "text": "My test",
        "tags": ["mongodb", "python", "pymongo"],
        "date": current_time.strftime("%Y-%m-%d %H:%M:%S")
    }

    result = mg_col_es_text.insert_one(post)
    print("Inserted document with ID:", result.inserted_id)
