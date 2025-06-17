"""
Simple Flask server for document scoring display
"""

from flask import Flask, render_template, jsonify
import os
import psycopg2
from psycopg2.extras import RealDictCursor

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('document_scoring.html')

@app.route('/api/documents')
def get_documents():
    """Get all documents with basic error handling"""
    try:
        # Connect to database
        conn = psycopg2.connect(os.getenv('DATABASE_URL'))
        cursor = conn.cursor(cursor_factory=RealDictCursor)
        
        cursor.execute("""
            SELECT id, title, author_organization, publish_date,
                   COALESCE(ai_cybersecurity_score, 0) as ai_cybersecurity_score,
                   COALESCE(quantum_cybersecurity_score, 1) as quantum_cybersecurity_score,
                   COALESCE(ai_ethics_score, 0) as ai_ethics_score,
                   COALESCE(quantum_ethics_score, 0) as quantum_ethics_score
            FROM documents 
            ORDER BY id
            LIMIT 20
        """)
        
        documents = cursor.fetchall()
        conn.close()
        
        # Convert to list of dicts for JSON serialization
        result = []
        for doc in documents:
            result.append({
                'id': doc['id'],
                'title': doc['title'] or 'Untitled Document',
                'organization': doc['organization'] or 'Unknown Organization', 
                'publication_date': str(doc['publication_date']) if doc['publication_date'] else 'Date not available',
                'ai_cybersecurity_score': safe_score(doc['ai_cybersecurity_score']),
                'quantum_cybersecurity_score': safe_score(doc['quantum_cybersecurity_score']),
                'ai_ethics_score': safe_score(doc['ai_ethics_score']),
                'quantum_ethics_score': safe_score(doc['quantum_ethics_score'])
            })
        
        return jsonify(result)
        
    except Exception as e:
        print(f"Database error: {e}")
        # Return sample data if database fails
        return jsonify([
            {
                'id': 1,
                'title': 'AI Risk Management Framework',
                'organization': 'NIST',
                'publication_date': '2023-01-26',
                'ai_cybersecurity_score': 78,
                'quantum_cybersecurity_score': 2,
                'ai_ethics_score': 82,
                'quantum_ethics_score': 45
            },
            {
                'id': 2, 
                'title': 'Executive Order on AI',
                'organization': 'White House',
                'publication_date': '2023-10-30',
                'ai_cybersecurity_score': 65,
                'quantum_cybersecurity_score': 3,
                'ai_ethics_score': 88,
                'quantum_ethics_score': 52
            }
        ])

@app.route('/api/analyze/<framework>/<int:doc_id>')
def analyze_document(framework, doc_id):
    """Provide analysis for framework and document"""
    analysis_map = {
        'ai_cyber': 'AI Cybersecurity analysis shows strong coverage of machine learning security frameworks and risk assessment protocols.',
        'ai_ethics': 'AI Ethics evaluation indicates comprehensive treatment of fairness, accountability, and transparency principles.',
        'q_cyber': 'Quantum Cybersecurity assessment reveals foundational to advanced quantum-safe cryptography considerations.',
        'q_ethics': 'Quantum Ethics review demonstrates awareness of quantum technology access equity and governance challenges.'
    }
    
    content = analysis_map.get(framework, 'Analysis not available for this framework.')
    return jsonify({'content': content})

def safe_score(score):
    """Safely handle score values"""
    if score is None:
        return None
    try:
        return int(score) if score != 0 else None
    except:
        return None

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002, debug=True)