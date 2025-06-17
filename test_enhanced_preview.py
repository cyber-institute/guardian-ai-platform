"""
Test the enhanced content preview system with real document data
"""
import psycopg2
import os
import sys
sys.path.append('.')

from utils.content_preview import generate_enhanced_preview

def test_preview_system():
    conn = psycopg2.connect(os.environ['DATABASE_URL'])
    cursor = conn.cursor()
    
    # Test with documents that have limited content (503 chars)
    cursor.execute('SELECT id, title, content, content_preview FROM documents WHERE LENGTH(content) = 503 LIMIT 3')
    results = cursor.fetchall()
    
    print("Testing enhanced preview system with limited content documents:")
    print("=" * 70)
    
    for result in results:
        doc = {
            'content': result[2],
            'title': result[1],
            'content_preview': result[3]
        }
        
        print(f"\nDocument ID: {result[0]}")
        print(f"Title: {result[1]}")
        print(f"Original content length: {len(result[2])} chars")
        print(f"Original preview length: {len(result[3]) if result[3] else 0} chars")
        
        # Generate enhanced preview
        try:
            enhanced_preview = generate_enhanced_preview(doc)
            print(f"Enhanced preview length: {len(enhanced_preview)} chars")
            print(f"Enhanced preview (first 500 chars):")
            print(enhanced_preview[:500])
            print("-" * 50)
        except Exception as e:
            print(f"Error generating preview: {e}")
    
    conn.close()

if __name__ == "__main__":
    test_preview_system()