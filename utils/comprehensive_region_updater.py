"""
Comprehensive Region Detection Updater
Updates all documents with enhanced multi-LLM region detection capabilities
"""

import os
import sys
sys.path.append('/home/runner/workspace')
from utils.db import fetch_documents
from utils.enhanced_region_detector import enhanced_region_detection

def update_all_documents_with_enhanced_regions():
    """Apply enhanced region detection to all documents in the database"""
    
    print("Starting comprehensive region detection update...")
    
    # Fetch all documents
    documents = fetch_documents()
    
    if not documents:
        print("No documents found in database")
        return
    
    total_docs = len(documents)
    updated_count = 0
    
    print(f"Processing {total_docs} documents...")
    
    for i, doc in enumerate(documents, 1):
        try:
            doc_id = doc.get('id')
            title = doc.get('title', '')
            content = doc.get('text', '') or doc.get('content', '')
            organization = doc.get('author_organization', '') or doc.get('organization', '')
            url = doc.get('url', '') or doc.get('source_url', '')
            
            print(f"\n[{i}/{total_docs}] Processing: {title[:50]}...")
            
            # Apply enhanced region detection
            region_result = enhanced_region_detection(
                title=title,
                content=content[:2000],  # Use first 2000 chars for analysis
                organization=organization,
                url=url
            )
            
            # Update document with region data
            from utils.database import get_db_connection
            
            conn = get_db_connection()
            cur = conn.cursor()
            
            update_query = """
                UPDATE documents 
                SET detected_region = %s,
                    region_confidence = %s,
                    region_reasoning = %s,
                    author_organization = %s
                WHERE id = %s
            """
            
            cur.execute(update_query, (
                region_result.get('region', 'Unknown'),
                region_result.get('confidence', 0.0),
                region_result.get('reasoning', 'Enhanced multi-LLM detection'),
                organization if organization else 'Unknown',
                doc_id
            ))
            
            conn.commit()
            cur.close()
            conn.close()
            
            updated_count += 1
            
            print(f"   ✓ Region: {region_result.get('region', 'Unknown')} "
                  f"(confidence: {region_result.get('confidence', 0):.1%})")
            
        except Exception as e:
            print(f"   ✗ Error processing document {doc_id}: {e}")
            continue
    
    print(f"\n=== Region Detection Update Complete ===")
    print(f"Total documents: {total_docs}")
    print(f"Successfully updated: {updated_count}")
    print(f"Failed: {total_docs - updated_count}")
    
    # Display region distribution
    display_region_distribution()

def display_region_distribution():
    """Display the distribution of detected regions"""
    
    try:
        from utils.database import get_db_connection
        
        conn = get_db_connection()
        cur = conn.cursor()
        
        # Get region distribution
        cur.execute("""
            SELECT detected_region, COUNT(*) as count, AVG(region_confidence) as avg_confidence
            FROM documents 
            WHERE detected_region IS NOT NULL 
            GROUP BY detected_region 
            ORDER BY count DESC
        """)
        
        results = cur.fetchall()
        
        print("\n=== Region Distribution ===")
        for region, count, avg_conf in results:
            print(f"{region:15}: {count:2d} documents (avg confidence: {avg_conf:.1%})")
        
        cur.close()
        conn.close()
        
    except Exception as e:
        print(f"Error displaying region distribution: {e}")

def test_region_detection_samples():
    """Test region detection on sample text to verify functionality"""
    
    print("\n=== Testing Region Detection ===")
    
    test_cases = [
        {
            'title': 'NASA Cybersecurity Guidelines',
            'organization': 'NASA',
            'content': 'National Aeronautics and Space Administration cybersecurity framework for space missions. Washington DC headquarters.',
            'expected': 'US'
        },
        {
            'title': 'ENISA Cloud Security Report',
            'organization': 'European Union Agency for Cybersecurity',
            'content': 'GDPR compliance and cloud security in the European Union. Brussels office coordination.',
            'expected': 'Europe'
        },
        {
            'title': 'NCSC Threat Assessment',
            'organization': 'UK National Cyber Security Centre',
            'content': 'UK government cybersecurity assessment. GCHQ collaboration and Crown services.',
            'expected': 'UK'
        }
    ]
    
    for i, test_case in enumerate(test_cases, 1):
        print(f"\nTest {i}: {test_case['title']}")
        
        try:
            result = enhanced_region_detection(
                title=test_case['title'],
                content=test_case['content'],
                organization=test_case['organization'],
                url=""
            )
            
            detected = result.get('region', 'Unknown')
            confidence = result.get('confidence', 0)
            expected = test_case['expected']
            
            status = "✓" if detected == expected else "✗"
            print(f"   {status} Expected: {expected}, Detected: {detected} (confidence: {confidence:.1%})")
            print(f"     Reasoning: {result.get('reasoning', 'No reasoning')}")
            
        except Exception as e:
            print(f"   ✗ Test failed: {e}")

if __name__ == "__main__":
    # Test detection first
    test_region_detection_samples()
    
    # Update all documents
    update_all_documents_with_enhanced_regions()