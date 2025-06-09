from utils.database import db_manager

def fetch_documents():
    """
    Fetch documents from the PostgreSQL database.
    Returns a list of document dictionaries with quantum maturity data.
    """
    try:
        return db_manager.fetch_documents()
    except Exception as e:
        print(f"Error fetching documents: {e}")
        return []

def save_document(document):
    """
    Save a document to the PostgreSQL database.
    """
    try:
        return db_manager.save_document(document)
    except Exception as e:
        print(f"Error saving document: {e}")
        return False

def save_assessment(document_id, assessment_data):
    """
    Save assessment results to the database.
    """
    try:
        return db_manager.save_assessment(document_id, assessment_data)
    except Exception as e:
        print(f"Error saving assessment: {e}")
        return False

def get_assessment_history(document_id):
    """
    Get assessment history for a document.
    """
    try:
        return db_manager.get_assessment_history(document_id)
    except Exception as e:
        print(f"Error fetching assessment history: {e}")
        return []
