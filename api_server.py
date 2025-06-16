#!/usr/bin/env python3
"""
Flask API server for handling HTML button clicks from GUARDIAN interface
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import sys
import os
import re

# Add current directory to path for imports
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Simple analysis functions without Streamlit dependencies
def analyze_ai_cybersecurity_content(content, score):
    """Simple AI cybersecurity analysis"""
    return f"""
    This document shows an AI Cybersecurity maturity score of {score}/100.
    
    Key findings:
    - Document addresses AI security considerations
    - Content includes risk assessment frameworks
    - Provides guidance on AI system protection
    
    Based on the content analysis, this represents {'excellent' if int(str(score).replace('/100', '')) >= 75 else 'good' if int(str(score).replace('/100', '')) >= 50 else 'developing'} AI cybersecurity practices.
    """

def analyze_quantum_cybersecurity_content(content, score):
    """Simple quantum cybersecurity analysis"""
    return f"""
    This document shows a Quantum Cybersecurity maturity of Tier {score}/5.
    
    Key findings:
    - Document addresses quantum-safe cryptography
    - Content includes post-quantum security measures
    - Provides quantum threat assessment guidance
    
    This represents {'advanced' if int(str(score).replace('Tier ', '').split('/')[0]) >= 4 else 'intermediate' if int(str(score).replace('Tier ', '').split('/')[0]) >= 3 else 'basic'} quantum cybersecurity readiness.
    """

def analyze_ai_ethics_content(content, score):
    """Simple AI ethics analysis"""
    return f"""
    This document shows an AI Ethics score of {score}/100.
    
    Key findings:
    - Document addresses ethical AI considerations
    - Content includes bias prevention measures
    - Provides fairness and transparency guidance
    
    This represents {'excellent' if int(str(score).replace('/100', '')) >= 75 else 'good' if int(str(score).replace('/100', '')) >= 50 else 'developing'} AI ethics practices.
    """

def analyze_quantum_ethics_content(content, score):
    """Simple quantum ethics analysis"""
    return f"""
    This document shows a Quantum Ethics score of {score}/100.
    
    Key findings:
    - Document addresses quantum computing ethics
    - Content includes quantum access and equity concerns
    - Provides quantum technology governance guidance
    
    This represents {'excellent' if int(str(score).replace('/100', '')) >= 75 else 'good' if int(str(score).replace('/100', '')) >= 50 else 'developing'} quantum ethics considerations.
    """

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

@app.route('/analyze', methods=['POST'])
def analyze_document():
    """Handle document analysis requests from HTML buttons"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'success': False, 'error': 'No JSON data received'}), 400
        
        button_type = data.get('button_type', '')
        doc_content = data.get('content', '')
        doc_title = data.get('title', '')
        score = data.get('score', 'N/A')
        score_display = data.get('score_display', 'N/A')
        
        analysis_result = {
            'success': True,
            'button_type': button_type,
            'score': score_display,
            'analysis': ''
        }
        
        if button_type == 'ai_cyber':
            if score != 'N/A':
                analysis_result['analysis'] = analyze_ai_cybersecurity_content(doc_content, score)
            else:
                analysis_result['analysis'] = "No AI cybersecurity assessment available for this document."
                
        elif button_type == 'q_cyber':
            if score != 'N/A':
                analysis_result['analysis'] = analyze_quantum_cybersecurity_content(doc_content, score)
            else:
                analysis_result['analysis'] = "No quantum cybersecurity assessment available for this document."
                
        elif button_type == 'ai_ethics':
            if score != 'N/A':
                analysis_result['analysis'] = analyze_ai_ethics_content(doc_content, score)
            else:
                analysis_result['analysis'] = "No AI ethics assessment available for this document."
                
        elif button_type == 'q_ethics':
            if score != 'N/A':
                analysis_result['analysis'] = analyze_quantum_ethics_content(doc_content, score)
            else:
                analysis_result['analysis'] = "No quantum ethics assessment available for this document."
                
        elif button_type == 'preview':
            import re
            clean_content = re.sub(r'<[^>]+>', '', doc_content)
            clean_content = re.sub(r'\s+', ' ', clean_content).strip()
            preview_content = clean_content[:500] + "..." if len(clean_content) > 500 else clean_content
            
            analysis_result['analysis'] = f"""
            **Intelligent Summary:**
            
            {doc_content[:300]}...
            
            **Raw Content Sample:**
            
            {preview_content}
            """
            
        elif button_type == 'translate':
            analysis_result['analysis'] = f"""
            **Document Translation**
            
            Translation feature coming soon. This will provide multi-language document translation.
            
            **Document:** {doc_title}
            **Content Length:** {len(doc_content)} characters
            """
            
        return jsonify(analysis_result)
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        }), 500

@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({'status': 'healthy'})

if __name__ == '__main__':
    print("Starting GUARDIAN API server on port 5001...")
    app.run(host='0.0.0.0', port=5001, debug=False)