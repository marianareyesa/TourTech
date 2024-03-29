from firebase_admin import firestore

def save_user_input(db, user_data):
    """
    Save user's input data to Firebase.
    Parameters:
    - db: The Firestore client.
    - user_data: A dictionary containing the user's input data.
    """
    doc_ref = db.collection('users').document()
    doc_ref.set(user_data)
    return doc_ref.id

def fetch_plan(db, user_id):
    """
    Fetch a generated plan for a given user ID from Firebase.
    Parameters:
    - db: The Firestore client.
    - user_id: The document ID for the user's data.
    """
    doc_ref = db.collection('plans').document(user_id)
    doc = doc_ref.get()
    if doc.exists:
        return doc.to_dict()
    else:
        return None