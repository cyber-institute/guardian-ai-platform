"""
Retroactive Region Detection for Existing Documents
Updates all existing documents with intelligent region detection using multi-LLM analysis
"""

from utils.database import DatabaseManager
from utils.region_detector import extract_enhanced_metadata_with_region
import time

def update_all_documents_with_regions():
    """Update all existing documents with region detection"""
    
    db_manager = DatabaseManager()
    
    # Get all documents that need region detection
    documents = db_manager.execute_query("""
        SELECT id, title, text_content, author_organization, content_preview
        FROM documents 
        WHERE detected_region IS NULL OR detected_region = '' OR detected_region = 'Unknown'
        ORDER BY id
    """)
    
    if not documents:
        print("No documents need region detection updates.")
        return
    
    print(f"Starting region detection for {len(documents)} documents...")
    
    processed = 0
    for doc in documents:
        try:
            doc_id = doc['id']
            title = doc.get('title', 'Unknown')
            content = doc.get('text_content', '') or doc.get('content_preview', '')
            org = doc.get('author_organization', 'Unknown')
            
            print(f"Processing document {doc_id}: {title[:50]}...")
            
            # Perform region detection
            region_metadata = extract_enhanced_metadata_with_region(
                title, content[:1000], org
            )
            
            detected_region = region_metadata.get('detected_region', 'Unknown')
            confidence = region_metadata.get('region_confidence', 0.0)
            reasoning = region_metadata.get('region_reasoning', '')
            
            # Update document with region information
            db_manager.execute_query("""
                UPDATE documents 
                SET 
                    detected_region = %s,
                    region_confidence = %s,
                    region_reasoning = %s,
                    updated_at = CURRENT_TIMESTAMP
                WHERE id = %s
            """, (detected_region, confidence, reasoning, doc_id))
            
            print(f"  → Detected: {detected_region} (confidence: {confidence:.1%})")
            processed += 1
            
            # Small delay to avoid overwhelming the LLM API
            time.sleep(0.5)
            
        except Exception as e:
            print(f"Error processing document {doc.get('id', 'unknown')}: {e}")
            continue
    
    print(f"\nCompleted region detection for {processed}/{len(documents)} documents.")
    return processed

def add_region_columns_if_missing():
    """Add region detection columns to documents table if they don't exist"""
    
    db_manager = DatabaseManager()
    
    try:
        # Check if columns exist and add them if missing
        db_manager.execute_query("""
            ALTER TABLE documents 
            ADD COLUMN IF NOT EXISTS detected_region VARCHAR(50) DEFAULT 'Unknown',
            ADD COLUMN IF NOT EXISTS region_confidence FLOAT DEFAULT 0.0,
            ADD COLUMN IF NOT EXISTS region_reasoning TEXT DEFAULT ''
        """)
        print("Region detection columns added/verified in database.")
        
    except Exception as e:
        print(f"Error adding region columns: {e}")

if __name__ == "__main__":
    print("Setting up region detection system...")
    
    # Add columns if missing
    add_region_columns_if_missing()
    
    # Update all documents
    update_all_documents_with_regions()
    
    print("Region detection setup complete!")