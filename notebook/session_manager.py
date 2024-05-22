from uuid import uuid4

# Dictionary to hold session IDs for users
session_store = {}

def get_session_id(user_id):
    """Retrieve an existing session ID for a user, or return None if no session exists."""
    return session_store.get(user_id, None)

def create_new_session(user_id):
    """Create a new session ID for a user and store it."""
    session_id = str(uuid4())
    session_store[user_id] = session_id
    return session_id

def end_session(user_id):
    """End a session by removing it from the store."""
    if user_id in session_store:
        del session_store[user_id]
