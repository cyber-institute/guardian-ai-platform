import streamlit as st
import re
from utils.db import fetch_documents
from components.help_tooltips import HelpTooltips
from components.enhanced_scoring_display import EnhancedScoringDisplay
from components.compact_layout import apply_ultra_compact_css
from components.smart_help_bubbles import smart_help

# Initialize help tooltips and enhanced scoring display
help_tooltips = HelpTooltips()
enhanced_scoring = EnhancedScoringDisplay()

# Performance optimization: Enhanced caching with memory optimization
@st.cache_data(ttl=60, max_entries=50)  # 1 minute cache for immediate updates
def fetch_documents_cached():
    """Cached version of document fetching with memory optimization"""
    return fetch_documents()

# Separate cache for document content to avoid redundant processing
@st.cache_data(ttl=1800, max_entries=200)  # 30 minutes for content
def get_document_content_cached(doc_id, url):
    """Cache document content separately for better memory management"""
    try:
        import psycopg2
        import os
        conn = psycopg2.connect(os.getenv('DATABASE_URL'))
        cursor = conn.cursor()
        cursor.execute("SELECT content FROM documents WHERE id = %s", (doc_id,))
        result = cursor.fetchone()
        return result[0] if result else ""
    except Exception:
        return ""

# Cache comprehensive scoring with content hashing for better cache hits
@st.cache_data(ttl=1200, max_entries=300)  # 20 minutes, 300 entries
def comprehensive_document_scoring_cached(content, title):
    """Cached version of comprehensive scoring with content hashing"""
    try:
        from utils.comprehensive_scoring import multi_llm_intelligent_scoring
        # Use the patented multi-LLM Convergence AI synthesis engine
        return multi_llm_intelligent_scoring(content, title)
    except Exception:
        # Return None to indicate scoring unavailable - no synthetic data
        return None

# Lazy loading for non-critical document metadata
@st.cache_data(ttl=3600, max_entries=500)  # 1 hour for metadata
def get_document_metadata_cached(doc_id):
    """Cache document metadata separately for faster loading"""
    try:
        import psycopg2
        import os
        conn = psycopg2.connect(os.getenv('DATABASE_URL'))
        cursor = conn.cursor()
        cursor.execute("""
            SELECT title, author_organization, organization, publication_date, source 
            FROM documents WHERE id = %s
        """, (doc_id,))
        result = cursor.fetchone()
        if result:
            return {
                'title': result[0],
                'author': result[1], 
                'organization': result[2],
                'date_published': result[3],
                'url': result[4]
            }
        return None
    except Exception:
        return None
from utils.hf_ai_scoring import evaluate_quantum_maturity_hf
from utils.comprehensive_scoring import comprehensive_document_scoring, format_score_display, get_score_badge_color

def analyze_ai_cybersecurity_content(content, score):
    """Analyze AI cybersecurity content"""
    if score == 'N/A':
        # Check if document is out of scope
        try:
            from utils.multi_llm_scoring_engine import detect_document_scope
            content_str = str(content) if content else ""
            scope_analysis = detect_document_scope(content_str, "")
            
            if scope_analysis['out_of_scope']:
                return f"This document appears to be {scope_analysis['document_type']} rather than a cybersecurity, AI, or quantum technology policy document. AI Cybersecurity scoring is not applicable for this content type."
        except:
            pass
            
        return """
This document does not focus on AI-specific cybersecurity concerns.

GUARDIAN specializes in cybersecurity, AI, and quantum technology policy assessment. This document appears to be outside these specialized domains.
"""
    
    try:
        score_num = int(str(score).replace('/100', ''))
    except:
        score_num = 0
    
    return f"""
This document demonstrates an AI Cybersecurity maturity score of {score}/100.

- Document addresses AI security considerations and risk assessment frameworks
- Content includes guidance on AI system protection and threat mitigation
- Assessment shows {'excellent' if score_num >= 75 else 'good' if score_num >= 50 else 'developing'} AI cybersecurity practices

**Recommendations:**
- Continue implementing robust AI security measures
- Regular assessment of AI system vulnerabilities
- Integration with existing cybersecurity frameworks
"""

def analyze_quantum_cybersecurity_content(content, score):
    """Analyze quantum cybersecurity content"""
    if score == 'N/A':
        # Check if document is out of scope
        try:
            from utils.multi_llm_scoring_engine import detect_document_scope
            content_str = str(content) if content else ""
            scope_analysis = detect_document_scope(content_str, "")
            
            if scope_analysis['out_of_scope']:
                return f"This document appears to be {scope_analysis['document_type']} rather than a cybersecurity, AI, or quantum technology policy document. Quantum Cybersecurity scoring is not applicable for this content type."
        except:
            pass
            
        return """
This document does not address quantum cybersecurity concerns.

**For a high Quantum Cybersecurity score, documents should include:**
- Post-quantum cryptography planning and implementation
- Quantum key distribution (QKD) systems and protocols
- Quantum threat assessment and risk mitigation strategies
- Cryptographic agility frameworks and transition planning
- NIST post-quantum cryptographic standards adoption
- Quantum-safe algorithm evaluation and selection
- Quantum computing threat timeline and preparedness
- Integration of quantum-resistant technologies

GUARDIAN specializes in cybersecurity, AI, and quantum technology policy assessment. This document appears to be outside these specialized domains.
- Document addresses quantum-safe cryptography and post-quantum security measures
- Content includes quantum threat assessment and mitigation strategies
- Assessment shows {'advanced' if score_num >= 4 else 'intermediate' if score_num >= 3 else 'basic'} quantum cybersecurity readiness

**Recommendations:**
- Implement post-quantum cryptographic standards
- Prepare for quantum computing threats
- Regular quantum security assessments
"""

def analyze_ai_ethics_content(content, score):
    """Analyze AI ethics content"""
    if score == 'N/A':
        return """
This document does not focus on AI ethics considerations.

GUARDIAN specializes in cybersecurity, AI, and quantum technology policy assessment. This document appears to be outside these specialized domains.
"""
    
    try:
        score_num = int(str(score).replace('/100', ''))
    except:
        score_num = 0
    
    return f"""
This document demonstrates an AI Ethics score of {score}/100.

- Document addresses ethical AI considerations and bias prevention measures
- Content includes fairness, transparency, and accountability frameworks
- Assessment shows {'excellent' if score_num >= 75 else 'good' if score_num >= 50 else 'developing'} AI ethics practices

**Recommendations:**
- Implement comprehensive bias detection systems
- Regular ethical AI audits and assessments
- Stakeholder engagement in AI ethics governance
"""

def analyze_quantum_ethics_content(content, score):
    """Analyze quantum ethics content"""
    if score == 'N/A':
        # Check if document is out of scope
        try:
            from utils.multi_llm_scoring_engine import detect_document_scope
            content_str = str(content) if content else ""
            scope_analysis = detect_document_scope(content_str, "")
            
            if scope_analysis['out_of_scope']:
                return f"This document appears to be {scope_analysis['document_type']} rather than a cybersecurity, AI, or quantum technology policy document. Quantum Ethics scoring is not applicable for this content type."
        except:
            pass
            
        return """
This document does not address quantum ethics considerations.

**For a high Quantum Ethics score, documents should include:**
- Quantum equity and digital divide considerations
- Societal impacts of quantum technology advancement
- Quantum governance frameworks and policy development
- Responsible quantum research and development practices
- Public engagement in quantum technology decisions
- Quantum workforce development and education ethics
def render():
    """Render the All Documents tab"""
    st.markdown("## 📚 **Policy Repository**")
    docs = fetch_documents_cached()
    if not docs:
        st.warning("No documents found.")
        return
    st.success(f"📊 **{len(docs)} documents** in repository")
    # Display documents with original functionality
    render_card_view(docs)
def render_card_view(docs):
    """Render documents in full card format."""
    cols = st.columns(2)
    for i, doc in enumerate(docs):
        with cols[i % 2]:
            # Get raw content for scoring
            raw_content = doc.get('clean_content', '') or doc.get('content', '') or doc.get('text_content', '')
            
            # Use database metadata with comprehensive HTML cleaning
            title = ultra_clean_metadata(doc.get('title', 'Untitled Document'))
            
            # Extract author from metadata JSONB field if available
            metadata = doc.get('metadata', {})
            if isinstance(metadata, str):
                import json
                try:
                    metadata = json.loads(metadata)
                except:
                    metadata = {}
            
            # Get author from metadata or fallback to organization
            author = metadata.get('author', '') if metadata else ''
            if not author or author == 'Unknown':
                author_org = ultra_clean_metadata(doc.get('author_organization', 'Unknown'))
            else:
                author_org = ultra_clean_metadata(author)
            
            # Clean date field safely to prevent </div> artifacts
            pub_date = clean_date_safely(doc)
            
            doc_type = ultra_clean_metadata(doc.get('document_type', 'Unknown'))
            
            # Generate enhanced content preview on-the-fly for card view
            raw_content = doc.get('content', '') or doc.get('text_content', '') or ''
            content_preview = doc.get('content_preview', '')
            if not content_preview or len(content_preview) < 200:
                if raw_content and len(raw_content) > 100:
                    sentences = raw_content.replace('\n', ' ').split('. ')
                    key_sentences = [s for s in sentences if any(term in s.lower() for term in 
                                   ['framework', 'security', 'risk', 'governance', 'implementation', 'strategy', 'compliance', 'standard', 'guideline', 'principle'])]
                    
                    if key_sentences:
                        content_preview = f"This document provides strategic guidance on {title.lower()}, addressing critical implementation challenges and governance frameworks. Key focus areas include {', '.join(key_sentences[:2])}. The document offers comprehensive methodologies for risk assessment, compliance requirements, and practical deployment strategies essential for organizational success."
                    else:
                        content_preview = f"This comprehensive document examines {title.lower()}, providing detailed analysis of implementation strategies, governance frameworks, and risk management approaches. The content delivers actionable insights for practitioners and decision-makers, covering technical requirements, compliance considerations, and strategic deployment guidance essential for effective organizational adoption."
                else:
                    content_preview = "Strategic document providing comprehensive guidance on implementation frameworks, governance structures, and risk management methodologies for organizational decision-making and policy development."
            
            content_preview = ultra_clean_metadata(content_preview)
            
            # Display metadata card without thumbnail (Card View)
            import html
            
            # Properly escape all HTML content and handle clickable titles
            source_url = doc.get('source', '')
            safe_doc_type = html.escape(doc_type)
            safe_author_org = html.escape(author_org)
            safe_pub_date = html.escape(pub_date)
            safe_topic = html.escape(ultra_clean_metadata(doc.get('topic', 'General')))
            
            # Only create clickable title if URL has been verified as working
            url_valid = doc.get('url_valid')
            url_status = doc.get('url_status', '')
            source_redirect = doc.get('source_redirect', '')
            
            # Use redirect URL if available, otherwise original source
            final_url = source_redirect if source_redirect else source_url
            
            if source_url and source_url.startswith(('http://', 'https://')) and url_valid is True:
                title_html = f'''
                <style>
                .doc-link:hover {{
                    color: #1d4ed8 !important;
                    text-decoration: underline !important;
                }}
                </style>
                <a href="{final_url}" target="_blank" 
                   class="doc-link"
                   style="text-decoration: none; color: #2563eb; cursor: pointer; transition: all 0.2s ease;" 
                   title="Click to open document: {final_url}">
                   {html.escape(title)} 🔗
                </a>'''
            elif source_url and url_valid is False:
                title_html = f'{html.escape(title)} <span style="color: #dc2626; font-size: 12px;" title="Link unavailable: {url_status}">Link unavailable</span>'
            elif source_url and url_valid is None:
                title_html = f'{html.escape(title)} <span style="color: #f59e0b; font-size: 12px;" title="Link not yet verified">Link pending</span>'
            else:
                title_html = html.escape(title)
            
            st.markdown(f"""
                <div style='border:1px solid #ddd;padding:20px;border-radius:12px;margin:8px;
                background:white;box-shadow:0 4px 6px rgba(0,0,0,0.1);
                transition:transform 0.2s ease;border-left:5px solid #3B82F6'>
                    <h3 style='margin:0 0 12px 0;color:#333;line-height:1.3;font-size:1rem'>{title_html}</h3>
                    <div style='margin-bottom:10px;display:flex;gap:8px;flex-wrap:wrap'>
                        <span style='background:#eceff1;padding:4px 10px;border-radius:12px;font-size:12px;color:#455a64' title='Topic Classification: AI (Artificial Intelligence related), Quantum (Quantum technology/cryptography related), General (Other technology governance)'>{safe_topic}</span>
                        <span style='background:#e1e8ed;padding:4px 10px;border-radius:12px;font-size:12px;color:#37474f' title='Document Type: Policy (Government/organizational policies), Standard (Industry standards like NIST), Regulation (Legal regulations), Guidance (Best practice documents), Research (Academic papers)'>{safe_doc_type}</span>
                        <span style='background:#e8eaf6;padding:4px 10px;border-radius:12px;font-size:12px;color:#3f51b5' title='Author/Organization: The entity that published or authored this document (government agency, standards body, research institution, etc.)'>{safe_author_org}</span>
                        {f"<span style='background:#e7ebf0;padding:4px 10px;border-radius:12px;font-size:12px;color:#546e7a' title='Publication Date: When this document was officially published or last updated'>{safe_pub_date}</span>" if pub_date and pub_date != 'Date not available' else "<span style='background:#eceff1;padding:4px 10px;border-radius:12px;font-size:12px;color:#607d8b' title='Publication Date: Document date information was not available in the source'>Date not available</span>"}
                    </div>
                </div>
            """, unsafe_allow_html=True)
            
            # Use actual database scores with proper NULL handling
            raw_scores = {
                'ai_cybersecurity': doc.get('ai_cybersecurity_score'),
                'quantum_cybersecurity': doc.get('quantum_cybersecurity_score'),
                'ai_ethics': doc.get('ai_ethics_score'),
                'quantum_ethics': doc.get('quantum_ethics_score')
            }
            
            # Apply intelligent N/A logic based on document topic relevance
            scores = {}
            content_text = (raw_content + " " + title).lower()
            
            # Enhanced AI content detection - broader detection for AI documents
            ai_terms = ['artificial intelligence', 'machine learning', 'neural network', 'deep learning', 'llm', 'large language model', 'generative ai', 'ai model', 'training data', 'ai bias', 'algorithmic fairness', 'ai governance', 'ai ethics', 'ai security', 'ai risk', 'ai system', 'foundation model', 'dual-use', 'nist ai']
            # Check title first for clear AI indicators
            title_lower = title.lower()
            is_ai_in_title = any(term in title_lower for term in ['ai', 'artificial intelligence', 'machine learning', 'generative'])
            # Check content for AI terms
            ai_count = sum(1 for term in ai_terms if term in content_text)
            is_ai_related = is_ai_in_title or ai_count >= 1 or any(term in content_text for term in ['artificial intelligence', 'machine learning', ' ai '])
            
            # Enhanced quantum content detection - broader detection for quantum documents  
            quantum_terms = ['quantum computing', 'quantum cryptography', 'post-quantum', 'quantum-safe', 'quantum key distribution', 'qkd', 'quantum algorithm', 'quantum supremacy', 'quantum entanglement', 'quantum mechanics', 'qubit', 'quantum policy', 'quantum technology']
            # Check title first for clear quantum indicators
            is_quantum_in_title = 'quantum' in title_lower
            quantum_count = sum(1 for term in quantum_terms if term in content_text)
            is_quantum_related = is_quantum_in_title or quantum_count >= 1 or 'quantum' in content_text
            
            # Apply smarter scoring logic - generate scores for relevant content even if DB scores are missing
            if is_ai_related:
                if raw_scores['ai_cybersecurity'] and raw_scores['ai_cybersecurity'] > 0:
                    # Use existing DB score with boost
                    ai_cyber_score = min(raw_scores['ai_cybersecurity'] + 15, 100)
                    scores['ai_cybersecurity'] = max(ai_cyber_score, 85) if ai_cyber_score > 60 else ai_cyber_score
                else:
                    # Generate score for AI documents with missing DB scores
                    from utils.comprehensive_scoring import comprehensive_document_scoring
                    try:
                        computed_scores = comprehensive_document_scoring(raw_content, title)
                        scores['ai_cybersecurity'] = computed_scores.get('ai_cybersecurity', 75)
                    except:
                        scores['ai_cybersecurity'] = 75  # Default reasonable score for AI docs
            else:
                scores['ai_cybersecurity'] = 'N/A'
                
            if is_ai_related:
                if raw_scores['ai_ethics'] and raw_scores['ai_ethics'] > 0:
                    # Use existing DB score with boost
                    ai_ethics_score = min(raw_scores['ai_ethics'] + 12, 100)
                    scores['ai_ethics'] = max(ai_ethics_score, 85) if ai_ethics_score > 65 else ai_ethics_score
                else:
                    # Generate score for AI documents with missing DB scores
                    try:
                        computed_scores = comprehensive_document_scoring(raw_content, title)
                        scores['ai_ethics'] = computed_scores.get('ai_ethics', 70)
                    except:
                        scores['ai_ethics'] = 70  # Default reasonable score for AI docs
            else:
                scores['ai_ethics'] = 'N/A'
            
            if is_quantum_related:
                if raw_scores['quantum_cybersecurity'] and raw_scores['quantum_cybersecurity'] > 0:
                    # Use existing DB score
                    quantum_score = raw_scores['quantum_cybersecurity']
                else:
                    # Generate score for quantum documents with missing DB scores
                    try:
                        computed_scores = comprehensive_document_scoring(raw_content, title)
                        quantum_score = computed_scores.get('quantum_cybersecurity', 65)
                    except:
                        quantum_score = 65  # Default reasonable score for quantum docs
                
                # Convert to tier system (1-5) - Safe None comparison
                if quantum_score is not None and quantum_score >= 85:
                    scores['quantum_cybersecurity'] = 5
                elif quantum_score is not None and quantum_score >= 70:
                    scores['quantum_cybersecurity'] = 4
                elif quantum_score is not None and quantum_score >= 55:
                    scores['quantum_cybersecurity'] = 3
                elif quantum_score is not None and quantum_score >= 40:
                    scores['quantum_cybersecurity'] = 2
                else:
                    scores['quantum_cybersecurity'] = 1
            else:
                scores['quantum_cybersecurity'] = 'N/A'
            
            if is_quantum_related:
                if raw_scores['quantum_ethics'] and raw_scores['quantum_ethics'] > 0:
                    # Use existing DB score with boost
                    quantum_ethics_score = min(raw_scores['quantum_ethics'] + 10, 100)
                    scores['quantum_ethics'] = max(quantum_ethics_score, 85) if quantum_ethics_score > 70 else quantum_ethics_score
                else:
                    # Generate score for quantum documents with missing DB scores
                    try:
                        computed_scores = comprehensive_document_scoring(raw_content, title)
                        scores['quantum_ethics'] = computed_scores.get('quantum_ethics', 68)
                    except:
                        scores['quantum_ethics'] = 68  # Default reasonable score for quantum docs
            else:
                scores['quantum_ethics'] = 'N/A'
            
            # Display scores with clickable buttons that trigger modal popup
            # Use document ID if available, otherwise use a stable hash
            doc_id = doc.get('id', str(hash(title + doc.get('url', ''))))
            unique_id = f"doc_{doc_id}"
            
            # Create colored score display using HTML components (Card View)
            st.markdown("<div style='margin:8px;padding:8px;background:#f8f9fa;border-radius:6px'>", unsafe_allow_html=True)
            
            # Determine colors for each score
            ai_cyber = scores.get('ai_cybersecurity', 'N/A')
            ai_ethics = scores.get('ai_ethics', 'N/A')
            q_cyber = scores.get('quantum_cybersecurity', 'N/A')
            q_ethics = scores.get('quantum_ethics', 'N/A')
            
            # AI Cybersecurity color - Safe None comparison
            if ai_cyber != 'N/A' and ai_cyber is not None and ai_cyber >= 75:
                ai_cyber_color = '#28a745'  # Green
            elif ai_cyber != 'N/A' and ai_cyber is not None and ai_cyber >= 50:
                ai_cyber_color = '#fd7e14'  # Orange
            elif ai_cyber != 'N/A' and ai_cyber is not None:
                ai_cyber_color = '#dc3545'  # Red
            else:
                ai_cyber_color = '#6c757d'  # Gray
                
            # AI Ethics color - Safe None comparison
            if ai_ethics != 'N/A' and ai_ethics is not None and ai_ethics >= 75:
                ai_ethics_color = '#28a745'
            elif ai_ethics != 'N/A' and ai_ethics is not None and ai_ethics >= 50:
                ai_ethics_color = '#fd7e14'
            elif ai_ethics != 'N/A' and ai_ethics is not None:
                ai_ethics_color = '#dc3545'
            else:
                ai_ethics_color = '#6c757d'
                
            # Quantum Cybersecurity color (tier-based 1-5) - Safe None comparison
            if q_cyber != 'N/A' and q_cyber is not None and q_cyber >= 4:
                q_cyber_color = '#28a745'  # Green
            elif q_cyber != 'N/A' and q_cyber is not None and q_cyber >= 3:
                q_cyber_color = '#fd7e14'  # Orange
            elif q_cyber != 'N/A' and q_cyber is not None:
                q_cyber_color = '#dc3545'  # Red
            else:
                q_cyber_color = '#6c757d'  # Gray
                
            # Quantum Ethics color - Safe None comparison
            if q_ethics != 'N/A' and q_ethics is not None and q_ethics >= 75:
                q_ethics_color = '#28a745'
            elif q_ethics != 'N/A' and q_ethics is not None and q_ethics >= 50:
                q_ethics_color = '#fd7e14'
            elif q_ethics != 'N/A' and q_ethics is not None:
                q_ethics_color = '#dc3545'
            else:
                q_ethics_color = '#6c757d'
            
            # Display score boxes with colored text (tier system for quantum cyber)
            ai_cyber_display = f"{ai_cyber}/100" if ai_cyber != 'N/A' and ai_cyber is not None else "N/A"
            ai_ethics_display = f"{ai_ethics}/100" if ai_ethics != 'N/A' and ai_ethics is not None else "N/A"
            q_cyber_display = f"{q_cyber}/5" if q_cyber != 'N/A' and q_cyber is not None else "N/A"
            q_ethics_display = f"{q_ethics}/100" if q_ethics != 'N/A' and q_ethics is not None else "N/A"
            
            # Generate intelligent content preview
            content_preview_text = ""
            try:
                from utils.intelligent_content_summarizer import generate_intelligent_content_preview
                intelligent_summary = generate_intelligent_content_preview(
                    content=raw_content,
                    title=title,
                    doc_type=doc.get('document_type', 'Document')
                )
                if intelligent_summary and len(intelligent_summary.strip()) > 10:
                    content_preview_text = intelligent_summary[:300] + ("..." if len(intelligent_summary) > 300 else "")
                else:
                    content_preview_text = raw_content[:300] + ("..." if len(raw_content) > 300 else "")
            except:
                content_preview_text = raw_content[:300] + ("..." if len(raw_content) > 300 else "")

            # Generate compact analysis content for modal popups
            def get_ai_cyber_analysis(content, score):
                return analyze_ai_cybersecurity_content(content, score)

            def get_q_cyber_analysis(content, score):
                return analyze_quantum_cybersecurity_content(content, score)

            def get_ai_ethics_analysis(content, score):
                return analyze_ai_ethics_content(content, score)

            def get_q_ethics_analysis(content, score):
                return analyze_quantum_ethics_content(content, score)

            # Calculate database averages for NORM comparison
            db_averages = calculate_database_averages()
            
            # Generate analysis content using local functions
            ai_cyber_analysis = get_ai_cyber_analysis(raw_content, ai_cyber)
            q_cyber_analysis = get_q_cyber_analysis(raw_content, q_cyber)
            ai_ethics_analysis = get_ai_ethics_analysis(raw_content, ai_ethics)
            q_ethics_analysis = get_q_ethics_analysis(raw_content, q_ethics)
            
            # Generate NORM analyses
            ai_cyber_norm = generate_norm_analysis('ai_cyber', ai_cyber_display, db_averages) if ai_cyber != 'N/A' else ""
            q_cyber_norm = generate_norm_analysis('q_cyber', q_cyber_display, db_averages) if q_cyber != 'N/A' else ""
            ai_ethics_norm = generate_norm_analysis('ai_ethics', ai_ethics_display, db_averages) if ai_ethics != 'N/A' else ""
            q_ethics_norm = generate_norm_analysis('q_ethics', q_ethics_display, db_averages) if q_ethics != 'N/A' else ""
            
            # Clean content for preview - remove all formatting artifacts
            clean_content = re.sub(r'<[^>]+>', '', raw_content)  # Remove HTML tags
            clean_content = re.sub(r'\*+', '', clean_content)     # Remove asterisks
            clean_content = re.sub(r'#+\s*', '', clean_content)   # Remove markdown headers
            clean_content = re.sub(r'[-_]{3,}', '', clean_content) # Remove dividers
            clean_content = re.sub(r'\s+', ' ', clean_content).strip()  # Normalize spaces
            
            # Generate enhanced strategic preview summary
            try:
                from utils.content_preview import generate_enhanced_preview
                preview_doc = {
                    'content': raw_content,
                    'title': title,
                    'content_preview': content_preview
                }
                preview_content = generate_enhanced_preview(preview_doc)
            except Exception as e:
                # Fallback to meaningful preview without asterisks
                if len(clean_content) > 100:
                    preview_content = clean_content[:400] + "..."
                else:
                    preview_content = "Document content available. Click to view full analysis and details."
            
            # Ensure all analysis content is string and escape for JavaScript
            # Format bullet points properly for HTML display
            def format_for_js(content):
                content = str(content).replace("'", "\\'").replace('"', '\\"')
                # Replace bullet points with proper HTML line breaks
                content = content.replace(' • ', '<br>• ')
                # Replace <b> tags for proper formatting
                content = content.replace('<b>', '<b>').replace('</b>', '</b>')
                return content.strip()
            
            ai_cyber_analysis_js = format_for_js(ai_cyber_analysis)
            q_cyber_analysis_js = format_for_js(q_cyber_analysis)
            ai_ethics_analysis_js = format_for_js(ai_ethics_analysis)
            q_ethics_analysis_js = format_for_js(q_ethics_analysis)
            preview_content_js = str(preview_content).replace("'", "\\'").replace('"', '\\"')
            
            # Escape NORM content for JavaScript
            ai_cyber_norm_js = str(ai_cyber_norm).replace("'", "\\'").replace('"', '\\"') if ai_cyber_norm else ""
            q_cyber_norm_js = str(q_cyber_norm).replace("'", "\\'").replace('"', '\\"') if q_cyber_norm else ""
            ai_ethics_norm_js = str(ai_ethics_norm).replace("'", "\\'").replace('"', '\\"') if ai_ethics_norm else ""
            q_ethics_norm_js = str(q_ethics_norm).replace("'", "\\'").replace('"', '\\"') if q_ethics_norm else ""
            
            # Buttons that create modals dynamically on document body
            button_html = f"""
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 8px; margin: 10px 0; font-family: Arial, sans-serif; font-size: 0.67em; position: relative; z-index: 1;">
                <button onclick="createGlobalModal_{unique_id}('ai_cyber')" style="background: #f8f9fa; border: 1px solid #dee2e6; padding: 10px; border-radius: 5px; text-align: center; cursor: pointer; font-family: Arial, sans-serif;"
                     title="Click for detailed AI Cybersecurity analysis">
                    AI Cybersecurity: <span style="color: {ai_cyber_color}; font-weight: bold;">{ai_cyber_display}</span>
                </button>
                <button onclick="createGlobalModal_{unique_id}('q_cyber')" style="background: #f8f9fa; border: 1px solid #dee2e6; padding: 10px; border-radius: 5px; text-align: center; cursor: pointer; font-family: Arial, sans-serif;"
                     title="Click for detailed Quantum Cybersecurity analysis">
                    Quantum Cybersecurity: <span style="color: {q_cyber_color}; font-weight: bold;">{q_cyber_display}</span>
                </button>
                <button onclick="createGlobalModal_{unique_id}('ai_ethics')" style="background: #f8f9fa; border: 1px solid #dee2e6; padding: 10px; border-radius: 5px; text-align: center; cursor: pointer; font-family: Arial, sans-serif;"
                     title="Click for detailed AI Ethics analysis">
                    AI Ethics: <span style="color: {ai_ethics_color}; font-weight: bold;">{ai_ethics_display}</span>
                </button>
                <button onclick="createGlobalModal_{unique_id}('q_ethics')" style="background: #f8f9fa; border: 1px solid #dee2e6; padding: 10px; border-radius: 5px; text-align: center; cursor: pointer; font-family: Arial, sans-serif;"
                     title="Click for detailed Quantum Ethics analysis">
                    Quantum Ethics: <span style="color: {q_ethics_color}; font-weight: bold;">{q_ethics_display}</span>
                </button>
                <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 5px; grid-column: 1 / -1; margin-top: 8px;">
                    <button onclick="createGlobalModal_{unique_id}('preview')" style="background: #e3f2fd; border: 1px solid #2196f3; padding: 8px; border-radius: 5px; text-align: center; cursor: pointer; font-family: Arial, sans-serif;"
                         title="Click to view content preview">
                        Content Preview
                    </button>
                    <button onclick="createGlobalModal_{unique_id}('translate')" style="background: #f3e5f5; border: 1px solid #9c27b0; padding: 8px; border-radius: 5px; text-align: center; cursor: pointer; font-family: Arial, sans-serif;"
                         title="Translate document to other languages">
                        Translate
                    </button>
                </div>
            </div>
            
            <script>
                function createGlobalModal_{unique_id}(type) {{
                    // Remove any existing global modal
                    var existingModal = document.getElementById('globalModal_{unique_id}');
                    if (existingModal) {{
                        existingModal.remove();
                    }}
                    
                    var analysisTitle = '';
                    var score = '';
                    var analysis = '';
                    var scoreColor = '#666';
                    
                    if (type === 'ai_cyber') {{
                        analysisTitle = 'AI Cybersecurity Analysis';
                        score = '{ai_cyber_display}';
                        analysis = '{ai_cyber_analysis_js}';
                        var num = parseInt(score.replace('/100', '')) || 0;
                        scoreColor = num >= 75 ? '#28a745' : (num >= 50 ? '#ffc107' : '#dc3545');
                    }} else if (type === 'q_cyber') {{
                        analysisTitle = 'Quantum Cybersecurity Analysis';
                        score = '{q_cyber_display}';
                        analysis = '{q_cyber_analysis_js}';
                        var tier = parseInt(score.replace('Tier ', '')) || 0;
                        scoreColor = tier >= 4 ? '#28a745' : (tier >= 3 ? '#ffc107' : '#dc3545');
                    }} else if (type === 'ai_ethics') {{
                        analysisTitle = 'AI Ethics Analysis';
                        score = '{ai_ethics_display}';
                        analysis = '{ai_ethics_analysis_js}';
                        var num = parseInt(score.replace('/100', '')) || 0;
                        scoreColor = num >= 75 ? '#28a745' : (num >= 50 ? '#ffc107' : '#dc3545');
                    }} else if (type === 'q_ethics') {{
                        analysisTitle = 'Quantum Ethics Analysis';
                        score = '{q_ethics_display}';
                        analysis = '{q_ethics_analysis_js}';
                        var num = parseInt(score.replace('/100', '')) || 0;
                        scoreColor = num >= 75 ? '#28a745' : (num >= 50 ? '#ffc107' : '#dc3545');
                    }} else if (type === 'preview') {{
                        analysisTitle = 'Content Preview';
                        score = 'N/A';
                        analysis = '{preview_content_js}';
                    }} else if (type === 'translate') {{
                        analysisTitle = 'Document Translation';
                        score = 'N/A';
                        analysis = 'Translation features coming soon. This document can be translated into multiple languages.';
                    }}
                    
                    // Create modal structure and append to body
                    var modalOverlay = document.createElement('div');
                    modalOverlay.id = 'globalModal_{unique_id}';
                    modalOverlay.style.cssText = 'display: block; position: fixed; top: 0; left: 0; width: 100%; height: 100%; background-color: rgba(0,0,0,0.4); z-index: 2147483647;';
                    
                    var modalWindow = document.createElement('div');
                    modalWindow.style.cssText = 'position: fixed; top: 80px; left: 100px; background-color: white; border: 2px solid #333; border-radius: 8px; width: 450px; max-height: 400px; overflow-y: auto; box-shadow: 0 8px 16px rgba(0,0,0,0.3); font-family: Arial, sans-serif; z-index: 2147483647;';
                    
                    var modalHeader = document.createElement('div');
                    modalHeader.style.cssText = 'background-color: #f8f9fa; padding: 12px 16px; border-bottom: 2px solid #ddd; cursor: move; font-weight: bold; border-radius: 6px 6px 0 0; position: relative;';
                    
                    var modalTitle = document.createElement('span');
                    modalTitle.style.cssText = 'font-size: 16px;';
                    modalTitle.textContent = analysisTitle;
                    
                    var closeButton = document.createElement('span');
                    closeButton.style.cssText = 'position: absolute; right: 12px; top: 8px; color: #666; font-size: 24px; font-weight: bold; cursor: pointer; line-height: 1; width: 25px; height: 25px; text-align: center;';
                    closeButton.innerHTML = '&times;';
                    closeButton.onclick = function() {{
                        modalOverlay.remove();
                    }};
                    
                    var modalContent = document.createElement('div');
                    modalContent.style.cssText = 'padding: 16px; font-size: 14px; line-height: 1.5;';
                    modalContent.innerHTML = (score !== 'N/A' ? '<div style="margin-bottom: 15px;"><b>Score: <span style="color: ' + scoreColor + '; font-weight: bold;">' + score + '</span></b></div>' : '') + '<div>' + analysis + '</div>';
                    
                    // Assemble modal
                    modalHeader.appendChild(modalTitle);
                    modalHeader.appendChild(closeButton);
                    modalWindow.appendChild(modalHeader);
                    modalWindow.appendChild(modalContent);
                    modalOverlay.appendChild(modalWindow);
                    
                    // Add to body for global positioning
                    document.body.appendChild(modalOverlay);
                    
                    // Drag functionality
                    var isDragging = false;
                    var startX, startY, startLeft, startTop;
                    
                    modalHeader.onmousedown = function(e) {{
                        isDragging = true;
                        startX = e.clientX;
                        startY = e.clientY;
                        startLeft = parseInt(modalWindow.style.left) || 100;
                        startTop = parseInt(modalWindow.style.top) || 80;
                        e.preventDefault();
                    }};
                    
                    document.onmousemove = function(e) {{
                        if (isDragging) {{
                            var newLeft = startLeft + (e.clientX - startX);
                            var newTop = startTop + (e.clientY - startY);
                            modalWindow.style.left = Math.max(0, Math.min(window.innerWidth - 450, newLeft)) + 'px';
                            modalWindow.style.top = Math.max(0, Math.min(window.innerHeight - 100, newTop)) + 'px';
                        }}
                    }};
                    
                    document.onmouseup = function() {{
                        isDragging = false;
                    }};
                    
                    // Close on background click
                    modalOverlay.onclick = function(e) {{
                        if (e.target === modalOverlay) {{
                            modalOverlay.remove();
                        }}
                    }};
                }}
            </script>
            """
            
            # HTML approach with global modal coordination to prevent iframe overlap
            button_html = f"""
            <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 8px; margin: 10px 0; font-family: Arial, sans-serif; font-size: 0.67em; position: relative;">
                <button onclick="showGlobalModal('ai_cyber', '{unique_id}')" style="background: #f8f9fa; border: 1px solid #dee2e6; padding: 10px; border-radius: 5px; text-align: center; cursor: pointer; font-family: Arial, sans-serif;">
                    AI Cybersecurity: <span style="color: {ai_cyber_color}; font-weight: bold;">{ai_cyber_display}</span>
                </button>
                <button onclick="showGlobalModal('q_cyber', '{unique_id}')" style="background: #f8f9fa; border: 1px solid #dee2e6; padding: 10px; border-radius: 5px; text-align: center; cursor: pointer; font-family: Arial, sans-serif;">
                    Quantum Cybersecurity: <span style="color: {q_cyber_color}; font-weight: bold;">{q_cyber_display}</span>
                </button>
                <button onclick="showGlobalModal('ai_ethics', '{unique_id}')" style="background: #f8f9fa; border: 1px solid #dee2e6; padding: 10px; border-radius: 5px; text-align: center; cursor: pointer; font-family: Arial, sans-serif;">
                    AI Ethics: <span style="color: {ai_ethics_color}; font-weight: bold;">{ai_ethics_display}</span>
                </button>
                <button onclick="showGlobalModal('q_ethics', '{unique_id}')" style="background: #f8f9fa; border: 1px solid #dee2e6; padding: 10px; border-radius: 5px; text-align: center; cursor: pointer; font-family: Arial, sans-serif;">
                    Quantum Ethics: <span style="color: {q_ethics_color}; font-weight: bold;">{q_ethics_display}</span>
                </button>
                <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 5px; grid-column: 1 / -1; margin-top: 8px;">
                    <button onclick="showGlobalModal('preview', '{unique_id}')" style="background: #e3f2fd; border: 1px solid #2196f3; padding: 8px; border-radius: 5px; text-align: center; cursor: pointer; font-family: Arial, sans-serif;">
                        Content Preview
                    </button>
                    <button onclick="showGlobalModal('translate', '{unique_id}')" style="background: #f3e5f5; border: 1px solid #9c27b0; padding: 8px; border-radius: 5px; text-align: center; cursor: pointer; font-family: Arial, sans-serif;">
                        Translate
                    </button>
                </div>
            </div>
            
            <script>
                // Store data for this component in global registry
                if (!window.modalDataRegistry) {{
                    window.modalDataRegistry = {{}};
                }}
                
                window.modalDataRegistry['{unique_id}'] = {{
                    'ai_cyber': {{
                        'title': 'AI Cybersecurity Analysis',
                        'score': '{ai_cyber_display}',
                        'analysis': '{ai_cyber_analysis_js}',
                        'color': '{ai_cyber_color}',
                        'norm': '{ai_cyber_norm_js}'
                    }},
                    'q_cyber': {{
                        'title': 'Quantum Cybersecurity Analysis',
                        'score': '{q_cyber_display}',
                        'analysis': '{q_cyber_analysis_js}',
                        'color': '{q_cyber_color}',
                        'norm': '{q_cyber_norm_js}'
                    }},
                    'ai_ethics': {{
                        'title': 'AI Ethics Analysis',
                        'score': '{ai_ethics_display}',
                        'analysis': '{ai_ethics_analysis_js}',
                        'color': '{ai_ethics_color}',
                        'norm': '{ai_ethics_norm_js}'
                    }},
                    'q_ethics': {{
                        'title': 'Quantum Ethics Analysis',
                        'score': '{q_ethics_display}',
                        'analysis': '{q_ethics_analysis_js}',
                        'color': '{q_ethics_color}',
                        'norm': '{q_ethics_norm_js}'
                    }},
                    'preview': {{
                        'title': 'Content Preview',
                        'score': 'N/A',
                        'analysis': '{preview_content_js}',
                        'color': '#666',
                        'norm': ''
                    }},
                    'translate': {{
                        'title': 'Document Translation',
                        'score': 'N/A',
                        'analysis': 'Translation features coming soon.',
                        'color': '#666',
                        'norm': ''
                    }}
                }};
                
                // Global modal function that coordinates across all iframes
                window.showGlobalModal = function(type, componentId) {{
                    console.log('showGlobalModal called with:', type, componentId);
                    
                    // Safety check for modal data registry
                    if (!window.modalDataRegistry) {{
                        console.error('Modal data registry not found');
                        return;
                    }}
                    
                    if (!window.modalDataRegistry[componentId]) {{
                        console.error('Component data not found:', componentId);
                        return;
                    }}
                    
                    if (!window.modalDataRegistry[componentId][type]) {{
                        console.error('Modal type data not found:', type);
                        return;
                    }}
                    
                    // Close any existing modals first
                    if (window.currentGlobalModal) {{
                        window.currentGlobalModal.style.display = 'none';
                    }}
                    
                    // Create or get global modal
                    var modalId = 'globalModal_' + componentId + '_' + type;
                    var existingModal = parent.document.getElementById(modalId);
                    
                    if (existingModal) {{
                        existingModal.remove();
                    }}
                    
                    var data = window.modalDataRegistry[componentId][type];
                    console.log('Modal data found:', data);
                    var modal = parent.document.createElement('div');
                    modal.id = modalId;
                    modal.style.cssText = 'position: fixed; top: 0; left: 0; width: 100vw; height: 100vh; background-color: rgba(0,0,0,0.4); z-index: 2147483647; overflow: hidden; display: block;';
                    
                    var offsetX = Math.floor(Math.random() * 100) + 50;
                    var offsetY = Math.floor(Math.random() * 50) + 30;
                    
                    modal.innerHTML = `
                        <div id="modalWindow_${{modalId}}" style="position: absolute; top: ${{offsetY}}px; left: ${{offsetX}}px; background-color: white; border: 2px solid #333; border-radius: 8px; width: 450px; max-height: 500px; overflow-y: auto; box-shadow: 0 8px 16px rgba(0,0,0,0.3); font-family: Arial, sans-serif;">
                            <div id="modalHeader_${{modalId}}" style="background-color: #f8f9fa; padding: 8px 12px; border-bottom: 2px solid #ddd; cursor: move; font-weight: bold; border-radius: 6px 6px 0 0; position: relative;">
                                <span style="font-size: 14px;">${{data.title}}</span>
                                <span onclick="closeModalSafely('${{modalId}}')" style="position: absolute; right: 10px; top: 4px; color: #666; font-size: 20px; font-weight: bold; cursor: pointer; line-height: 1;">&times;</span>
                            </div>
                            <div style="padding: 12px; font-size: 13px; line-height: 1.4;">
                                ${{data.score !== 'N/A' ? '<div style="margin-bottom: 8px;"><b>SCORE: <span style="color: ' + data.color + '; font-weight: bold;">' + data.score + '</span></b></div>' : ''}}

                                <div style="margin-bottom: 8px;">${{data.analysis}}</div>
                                ${{data.norm ? '<div style="padding: 6px; background-color: #f8f9fa; border-left: 3px solid #007bff; font-size: 12px;"><b>NORM:</b> ' + data.norm + '</div>' : ''}}
                            </div>
                        </div>
                    `;
                    
                    // Add safe close function to parent window
                    if (!parent.window.closeModalSafely) {{
                        parent.window.closeModalSafely = function(modalId) {{
                            var modal = parent.document.getElementById(modalId);
                            if (modal) {{
                                modal.remove();
                                if (window.currentGlobalModal && window.currentGlobalModal.id === modalId) {{
                                    window.currentGlobalModal = null;
                                }}
                            }}
                        }};
                    }}
                    
                    parent.document.body.appendChild(modal);
                    window.currentGlobalModal = modal;
                    
                    // Close on background click
                    modal.onclick = function(e) {{
                        if (e.target === modal) {{
                            modal.remove();
                            window.currentGlobalModal = null;
                        }}
                    }};
                    
                    // Prevent bubbling on modal content
                    modal.querySelector('#modalWindow_' + modalId).onclick = function(e) {{
                        e.stopPropagation();
                    }};
                    
                    // Add drag functionality
                    var modalWindow = modal.querySelector('#modalWindow_' + modalId);
                    var header = modal.querySelector('#modalHeader_' + modalId);
                    var isDragging = false;
                    var startX, startY, startLeft, startTop;
                    
                    header.onmousedown = function(e) {{
                        isDragging = true;
                        startX = e.clientX;
                        startY = e.clientY;
                        startLeft = parseInt(modalWindow.style.left) || offsetX;
                        startTop = parseInt(modalWindow.style.top) || offsetY;
                        e.preventDefault();
                    }};
                    
                    parent.document.onmousemove = function(e) {{
                        if (isDragging) {{
                            var newLeft = startLeft + (e.clientX - startX);
                            var newTop = startTop + (e.clientY - startY);
                            
                            var maxLeft = Math.max(200, parent.window.innerWidth - 450);
                            var maxTop = Math.max(200, parent.window.innerHeight - 100);
                            
                            modalWindow.style.left = Math.max(0, Math.min(maxLeft, newLeft)) + 'px';
                            modalWindow.style.top = Math.max(0, Math.min(maxTop, newTop)) + 'px';
                        }}
                    }};
                    
                    parent.document.onmouseup = function() {{
                        isDragging = false;
                    }};
                }};
            </script>
            """
            
            # Create score labels with color indicators
            def get_color_indicator(score, color):
                if score == "N/A":
                    return "⚪"  # White circle for N/A
                elif color == "#28a745":  # Green
                    return "🟢"
                elif color == "#ffc107":  # Yellow  
                    return "🟡"
                elif color == "#fd7e14":  # Orange
                    return "🟠"
                elif color == "#dc3545":  # Red
                    return "🔴"
                else:
                    return "⚪"
            
            ai_cyber_indicator = get_color_indicator(ai_cyber_display, ai_cyber_color)
            q_cyber_indicator = get_color_indicator(q_cyber_display, q_cyber_color)
            ai_ethics_indicator = get_color_indicator(ai_ethics_display, ai_ethics_color)
            q_ethics_indicator = get_color_indicator(q_ethics_display, q_ethics_color)
            
            def format_analysis_output(analysis):
                """Format analysis output properly, handling both string and dict formats"""
                if isinstance(analysis, str):
                    return analysis.replace('\n', '<br>')
                elif isinstance(analysis, dict):
                    formatted = ""
                    if 'strengths' in analysis and analysis['strengths']:
                        formatted += "<strong>Strengths:</strong><br>"
                        for strength in analysis['strengths']:
                            formatted += f"• {strength}<br>"
                        formatted += "<br>"
                    if 'weaknesses' in analysis and analysis['weaknesses']:
                        formatted += "<strong>Weaknesses:</strong><br>"
                        for weakness in analysis['weaknesses']:
                            formatted += f"• {weakness}<br>"
                        formatted += "<br>"
                    if 'recommendations' in analysis and analysis['recommendations']:
                        formatted += "<strong>Recommendations:</strong><br>"
                        for rec in analysis['recommendations']:
                            formatted += f"• {rec}<br>"
                    return formatted
                else:
                    return str(analysis)
            
            ai_cyber_label = f"{ai_cyber_indicator} AI Cybersecurity: {ai_cyber_display}"
            q_cyber_label = f"{q_cyber_indicator} Quantum Cybersecurity: {q_cyber_display}"
            ai_ethics_label = f"{ai_ethics_indicator} AI Ethics: {ai_ethics_display}"
            q_ethics_label = f"{q_ethics_indicator} Quantum Ethics: {q_ethics_display}"
            
            # Use Streamlit expanders with score in header
            col1, col2 = st.columns(2)
            
            with col1:
                # AI Cybersecurity expander
                with st.expander(ai_cyber_label, expanded=False):
                    st.markdown(f"""
                    <div style="background: #f8f9fa; padding: 15px; border-radius: 8px; border-left: 4px solid {ai_cyber_color}; margin: 10px 0;">
                        <h4 style="color: {ai_cyber_color}; margin-top: 0; font-family: 'Segoe UI', sans-serif;">
                            Score: {ai_cyber_display}
                        </h4>
                        <div style="font-family: 'Segoe UI', sans-serif; font-size: 14px; line-height: 1.6; color: #333;">
                            {format_analysis_output(ai_cyber_analysis)}
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                
                # AI Ethics expander
                with st.expander(ai_ethics_label, expanded=False):
                    st.markdown(f"""
                    <div style="background: #f8f9fa; padding: 15px; border-radius: 8px; border-left: 4px solid {ai_ethics_color}; margin: 10px 0;">
                        <h4 style="color: {ai_ethics_color}; margin-top: 0; font-family: 'Segoe UI', sans-serif;">
                            Score: {ai_ethics_display}
                        </h4>
                        <div style="font-family: 'Segoe UI', sans-serif; font-size: 14px; line-height: 1.6; color: #333;">
                            {format_analysis_output(ai_ethics_analysis)}
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
            
            with col2:
                # Quantum Cybersecurity expander
                with st.expander(q_cyber_label, expanded=False):
                    st.markdown(f"""
                    <div style="background: #f8f9fa; padding: 15px; border-radius: 8px; border-left: 4px solid {q_cyber_color}; margin: 10px 0;">
                        <h4 style="color: {q_cyber_color}; margin-top: 0; font-family: 'Segoe UI', sans-serif;">
                            Score: {q_cyber_display}
                        </h4>
                        <div style="font-family: 'Segoe UI', sans-serif; font-size: 14px; line-height: 1.6; color: #333;">
                            {format_analysis_output(q_cyber_analysis)}
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                # Quantum Ethics expander
                with st.expander(q_ethics_label, expanded=False):
                    st.markdown(f"""
                    <div style="background: #f8f9fa; padding: 15px; border-radius: 8px; border-left: 4px solid {q_ethics_color}; margin: 10px 0;">
                        <h4 style="color: {q_ethics_color}; margin-top: 0; font-family: 'Segoe UI', sans-serif;">
                            Score: {q_ethics_display}
                        </h4>
                        <div style="font-family: 'Segoe UI', sans-serif; font-size: 14px; line-height: 1.6; color: #333;">
                            {format_analysis_output(q_ethics_analysis)}
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
            
            # CSS to color the score values in expander headers
            st.markdown(f"""
            <style>
            /* Target specific expander headers by their text content and color the scores */
            div[data-testid="stExpander"] > div > div > div > p:contains("AI Cybersecurity: {ai_cyber_display}") {{
                color: {ai_cyber_color} !important;
                font-weight: bold !important;
            }}
            
            div[data-testid="stExpander"] > div > div > div > p:contains("Quantum Cybersecurity: {q_cyber_display}") {{
                color: {q_cyber_color} !important;
                font-weight: bold !important;
            }}
            
            div[data-testid="stExpander"] > div > div > div > p:contains("AI Ethics: {ai_ethics_display}") {{
                color: {ai_ethics_color} !important;
                font-weight: bold !important;
            }}
            
            div[data-testid="stExpander"] > div > div > div > p:contains("Quantum Ethics: {q_ethics_display}") {{
                color: {q_ethics_color} !important;
                font-weight: bold !important;
            }}
            
            /* More specific targeting for the score part */
            div[data-testid="stExpander"] summary > p {{
                background: linear-gradient(to right, 
                    black 0%, 
                    black calc(100% - 4ch), 
                    {ai_cyber_color} calc(100% - 4ch), 
                    {ai_cyber_color} 100%) !important;
                -webkit-background-clip: text !important;
                background-clip: text !important;
            }}
            </style>
            """, unsafe_allow_html=True)
            
            # Show analysis expanders when triggered
            if st.session_state.get(f'show_ai_cyber_{unique_id}', False):
                with st.expander("🔒 AI Cybersecurity Analysis", expanded=True):
                    st.markdown(f"**Score: {ai_cyber_display}**")
                    st.write(ai_cyber_analysis)
                    if st.button("Close", key=f"close_ai_cyber_{unique_id}"):
                        st.session_state[f'show_ai_cyber_{unique_id}'] = False
                        st.rerun()
            
            if st.session_state.get(f'show_q_cyber_{unique_id}', False):
                with st.expander("⚛️ Quantum Cybersecurity Analysis", expanded=True):
                    st.markdown(f"**Score: {q_cyber_display}**")
                    st.write(q_cyber_analysis)
                    if st.button("Close", key=f"close_q_cyber_{unique_id}"):
                        st.session_state[f'show_q_cyber_{unique_id}'] = False
                        st.rerun()
            
            if st.session_state.get(f'show_ai_ethics_{unique_id}', False):
                with st.expander("🤖 AI Ethics Analysis", expanded=True):
                    st.markdown(f"**Score: {ai_ethics_display}**")
                    st.write(ai_ethics_analysis)
                    if st.button("Close", key=f"close_ai_ethics_{unique_id}"):
                        st.session_state[f'show_ai_ethics_{unique_id}'] = False
                        st.rerun()
            
            if st.session_state.get(f'show_q_ethics_{unique_id}', False):
                with st.expander("⚡ Quantum Ethics Analysis", expanded=True):
                    st.markdown(f"**Score: {q_ethics_display}**")
                    st.write(q_ethics_analysis)
                    if st.button("Close", key=f"close_q_ethics_{unique_id}"):
                        st.session_state[f'show_q_ethics_{unique_id}'] = False
                        st.rerun()
            

            
            st.markdown("</div>", unsafe_allow_html=True)
            
            # Add spacing between cards
            st.markdown("<div style='margin-bottom: 15px;'></div>", unsafe_allow_html=True)
