import os
import json

def fetch_documents():
    """
    Fetch documents from the database or file system.
    Returns a list of document dictionaries with quantum maturity data.
    """
    # Check if there's a documents file or database connection
    documents_file = os.getenv("DOCUMENTS_FILE", "documents.json")
    
    try:
        if os.path.exists(documents_file):
            with open(documents_file, 'r') as f:
                documents = json.load(f)
                return documents
        else:
            # Return empty list if no documents found
            return []
    except Exception as e:
        print(f"Error fetching documents: {e}")
        return []

def save_document(document):
    """
    Save a document to the database or file system.
    """
    documents_file = os.getenv("DOCUMENTS_FILE", "documents.json")
    
    try:
        # Load existing documents
        documents = fetch_documents()
        
        # Add the new document
        documents.append(document)
        
        # Save back to file
        with open(documents_file, 'w') as f:
            json.dump(documents, f, indent=2)
            
        return True
    except Exception as e:
        print(f"Error saving document: {e}")
        return False
