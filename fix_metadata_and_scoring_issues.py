"""
Comprehensive Fix for Metadata Extraction and Scoring Issues
Addresses the specific NIST document and similar problems across all documents
"""

import os
import re
import psycopg2
from typing import Dict, Optional, List

def extract_proper_title(content: str) -> Optional[str]:
    """Extract the proper document title from content using enhanced patterns"""
    if not content:
        return None
    
    # NIST-specific patterns first
    nist_patterns = [
        r'NIST\s+Special\s+Publication\s+\d+[^\n]*(?:Secure\s+Software\s+Development\s+Practices[^\n]*)',
        r'NIST\s+SP\s+\d+[-\d]*[A-Z]*[^\n]*(?:Secure\s+Software\s+Development[^\n]*)',
        r'NIST\s+SP\s+\d+[-\d]*[A-Z]*[^\n]*(?:Generative\s+AI[^\n]*)',
        r'(?:^|\n)\s*(NIST\s+Special\s+Publication[^\n]{10,100})\s*(?:\n|$)',
        r'(?:^|\n)\s*(NIST\s+SP\s+\d+[-\d]*[A-Z]*[^\n]{10,100})\s*(?:\n|$)'
    ]
    
    # General document title patterns
    general_patterns = [
        r'(?:^|\n)\s*([A-Z][A-Za-z\s\d-]{15,120}(?:Guidelines?|Framework|Strategy|Policy|Standard|Publication|Practices|Advisory))\s*(?:\n|$)',
        r'(?:^|\n)\s*((?:[A-Z][a-z]+\s+){2,}(?:for\s+)?(?:[A-Z][a-z]+\s*){1,3})\s*(?:\n|$)',
        r'(?:^|\n)\s*([A-Z][^.\n]{20,100}(?:AI|Artificial Intelligence|Cybersecurity|Security)[^.\n]*)\s*(?:\n|$)',
        r'(?:^|\n)\s*(Secure\s+Software\s+Development[^\n]{5,80})\s*(?:\n|$)',
        r'(?:^|\n)\s*(AI\s+Security\s+[^\n]{5,80})\s*(?:\n|$)'
    ]
    
    # Try NIST patterns first
    for pattern in nist_patterns:
        match = re.search(pattern, content[:1000], re.IGNORECASE | re.MULTILINE)
        if match:
            title = match.group(1) if match.groups() else match.group(0)
            title = re.sub(r'<[^>]+>', '', title).strip()
            if len(title) > 15 and len(title) < 150:
                return title
    
    # Then try general patterns
    for pattern in general_patterns:
        match = re.search(pattern, content[:800], re.IGNORECASE | re.MULTILINE)
        if match:
            title = match.group(1).strip()
            title = re.sub(r'<[^>]+>', '', title).strip()
            if (len(title) > 15 and len(title) < 150 and
                not any(bad in title.lower() for bad in ['skip', 'search', 'menu', 'while', 'click', 'javascript'])):
                return title
    
    return None

def should_score_document(content: str, title: str) -> Dict[str, bool]:
    """Determine which scoring frameworks should apply to a document"""
    text_lower = content.lower()
    title_lower = title.lower()
    combined = f"{title_lower} {text_lower}"
    
    # AI-related keywords
    ai_keywords = [
        'artificial intelligence', 'machine learning', 'deep learning', 'neural network',
        'ai system', 'algorithm', 'automated decision', 'chatbot', 'llm', 'gpt',
        'generative ai', 'foundation model', 'responsible ai', 'trustworthy ai',
        'ai plan', 'ai framework', 'ai policy', 'ai governance', 'ai security'
    ]
    
    # Quantum-related keywords  
    quantum_keywords = [
        'post-quantum', 'quantum computing', 'quantum cryptography',
        'quantum encryption', 'quantum key', 'quantum-safe', 'quantum-resistant',
        'qkd', 'quantum supremacy', 'quantum advantage', 'quantum security'
    ]
    
    # Cybersecurity keywords
    cyber_keywords = [
        'cybersecurity', 'security', 'encryption', 'cryptography', 'vulnerability',
        'threat', 'attack', 'defense', 'protection', 'breach', 'secure development'
    ]
    
    # Ethics keywords
    ethics_keywords = [
        'ethics', 'ethical', 'responsible', 'trustworthy', 'governance', 'bias',
        'fairness', 'transparency', 'accountability', 'privacy', 'human rights'
    ]
    
    has_ai = any(keyword in combined for keyword in ai_keywords)
    has_quantum = any(keyword in combined for keyword in quantum_keywords)
    has_cyber = any(keyword in combined for keyword in cyber_keywords)
    has_ethics = any(keyword in combined for keyword in ethics_keywords)
    
    return {
        'ai_cybersecurity': has_ai and has_cyber,
        'quantum_cybersecurity': has_quantum and has_cyber,
        'ai_ethics': has_ai and has_ethics,
        'quantum_ethics': has_quantum and has_ethics
    }

def calculate_ai_cybersecurity_score(content: str, title: str) -> int:
    """Calculate AI cybersecurity score based on content analysis"""
    text_lower = content.lower()
    title_lower = title.lower()
    combined = f"{title_lower} {text_lower}"
    
    score = 0
    
    # High-value indicators for NIST documents
    if 'nist' in title_lower and 'secure software development' in combined:
        score += 40  # Authoritative guidance
    
    if 'generative ai' in combined and 'secure' in combined:
        score += 25  # Specific AI security focus
    
    # Security practice indicators
    security_practices = [
        'secure development', 'vulnerability', 'threat modeling', 'security testing',
        'risk assessment', 'security controls', 'secure coding', 'penetration testing'
    ]
    score += sum(5 for practice in security_practices if practice in combined)
    
    # AI-specific security indicators
    ai_security_terms = [
        'ai security', 'model security', 'adversarial attack', 'data poisoning',
        'model poisoning', 'prompt injection', 'ai governance', 'responsible ai'
    ]
    score += sum(8 for term in ai_security_terms if term in combined)
    
    # Government/standards organization boost
    if any(org in combined for org in ['nist', 'cisa', 'dhs', 'ncsc']):
        score += 15
    
    return min(100, max(0, score))

def calculate_ai_ethics_score(content: str, title: str) -> int:
    """Calculate AI ethics score based on content analysis"""
    text_lower = content.lower()
    title_lower = title.lower()
    combined = f"{title_lower} {text_lower}"
    
    score = 0
    
    # Ethics-specific terms
    ethics_terms = [
        'responsible ai', 'trustworthy ai', 'ai ethics', 'bias', 'fairness',
        'transparency', 'accountability', 'explainability', 'human oversight'
    ]
    score += sum(8 for term in ethics_terms if term in combined)
    
    # Governance and policy terms
    governance_terms = [
        'governance', 'policy', 'framework', 'guidelines', 'standards',
        'compliance', 'oversight', 'human rights', 'privacy'
    ]
    score += sum(5 for term in governance_terms if term in combined)
    
    # AI context bonus
    if any(ai_term in combined for ai_term in ['artificial intelligence', 'ai system', 'generative ai']):
        score += 20
    
    return min(100, max(0, score))

def fix_document_metadata_and_scoring():
    """Fix metadata extraction and scoring issues for all documents"""
    print("Starting comprehensive metadata and scoring fix...")
    
    try:
        DATABASE_URL = os.environ.get('DATABASE_URL')
        if not DATABASE_URL:
            print("DATABASE_URL environment variable not found")
            return
            
        conn = psycopg2.connect(DATABASE_URL)
        cursor = conn.cursor()
        
        # Get documents that need fixing (missing scores or poor titles)
        cursor.execute("""
            SELECT id, title, text_content 
            FROM documents 
            WHERE text_content IS NOT NULL 
            AND text_content != ''
            AND (
                ai_cybersecurity_score IS NULL 
                OR quantum_cybersecurity_score IS NULL 
                OR ai_ethics_score IS NULL 
                OR quantum_ethics_score IS NULL
                OR title LIKE '%Security Document%'
                OR title LIKE '%Document from%'
                OR title = 'Untitled'
                OR LENGTH(title) < 15
            )
            ORDER BY created_at DESC
        """)
        
        documents = cursor.fetchall()
        print(f"Found {len(documents)} documents to process")
        
        updated_count = 0
        for doc_id, current_title, content in documents:
            try:
                print(f"Processing document {doc_id}: {current_title[:50]}...")
                
                # Extract proper title
                new_title = extract_proper_title(content)
                if not new_title:
                    new_title = current_title  # Keep existing if extraction fails
                
                # Determine scoring applicability
                scoring_flags = should_score_document(content, new_title)
                
                # Calculate scores only for applicable frameworks
                scores = {}
                
                if scoring_flags['ai_cybersecurity']:
                    scores['ai_cybersecurity_score'] = calculate_ai_cybersecurity_score(content, new_title)
                
                if scoring_flags['ai_ethics']:
                    scores['ai_ethics_score'] = calculate_ai_ethics_score(content, new_title)
                
                # For quantum scoring, only apply if quantum content is detected
                if scoring_flags['quantum_cybersecurity']:
                    scores['quantum_cybersecurity_score'] = 3  # Conservative quantum cyber score
                
                if scoring_flags['quantum_ethics']:
                    scores['quantum_ethics_score'] = 50  # Moderate quantum ethics score
                
                # Update document
                update_parts = ["title = %s"]
                params = [new_title]
                
                for score_field, score_value in scores.items():
                    update_parts.append(f"{score_field} = %s")
                    params.append(score_value)
                
                params.append(doc_id)
                
                update_query = f"""
                    UPDATE documents 
                    SET {', '.join(update_parts)}
                    WHERE id = %s
                """
                
                cursor.execute(update_query, params)
                
                print(f"Updated document {doc_id}:")
                print(f"  Title: {new_title[:60]}...")
                if scores:
                    print(f"  Scores: {scores}")
                
                updated_count += 1
                
            except Exception as e:
                print(f"Error processing document {doc_id}: {e}")
                continue
        
        conn.commit()
        cursor.close()
        conn.close()
        
        print(f"\nCompleted! Updated {updated_count} documents")
        
    except Exception as e:
        print(f"Database error: {e}")

if __name__ == "__main__":
    fix_document_metadata_and_scoring()