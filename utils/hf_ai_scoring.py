import os
import re
try:
    from transformers import pipeline
    HF_AVAILABLE = True
except ImportError:
    HF_AVAILABLE = False

# Initialize the classifier once to avoid repeated loading
classifier = None

def get_classifier():
    """
    Get or initialize the Hugging Face zero-shot classifier.
    """
    global classifier
    if not HF_AVAILABLE:
        return None
    if classifier is None:
        try:
            # Use a lightweight model for zero-shot classification with proper device mapping
            classifier = pipeline(
                "zero-shot-classification",
                model="facebook/bart-large-mnli",
                device_map="auto",
                torch_dtype="auto"
            )
        except Exception as e:
            print(f"Error initializing classifier: {e}")
            try:
                # Fallback to CPU-only mode
                classifier = pipeline(
                    "zero-shot-classification",
                    model="facebook/bart-large-mnli",
                    device="cpu"
                )
            except Exception as e2:
                print(f"Fallback classifier also failed: {e2}")
                classifier = None
    return classifier

def evaluate_quantum_maturity_hf(text):
    """
    Evaluate quantum maturity using Hugging Face transformers.
    """
    # Define quantum maturity labels with different categories
    labels = [
        "quantum-aware-basic",
        "quantum-aware-advanced", 
        "quantum-ready-planning",
        "quantum-ready-testing",
        "quantum-controls-implemented",
        "quantum-controls-validated",
        "post-quantum-cryptography",
        "quantum-risk-assessment",
        "quantum-migration-strategy"
    ]
    
    # Define weights for different maturity levels
    weights = {
        "quantum-aware-basic": 0.8,
        "quantum-aware-advanced": 0.8,
        "quantum-ready-planning": 1.2,
        "quantum-ready-testing": 1.2,
        "quantum-controls-implemented": 1.5,
        "quantum-controls-validated": 1.5,
        "post-quantum-cryptography": 1.8,
        "quantum-risk-assessment": 1.3,
        "quantum-migration-strategy": 1.4
    }
    
    try:
        clf = get_classifier()
        if clf is None:
            # Fallback to basic text analysis if HF classifier fails
            return _fallback_analysis(text)
        
        # Perform zero-shot classification
        result = clf(text, labels)
        
        # Extract results
        raw_scores = dict(zip(result['labels'], result['scores']))
        
        # Calculate weighted patent score
        patent_score = _calculate_patent_score(raw_scores, weights)
        
        # Generate narrative
        narrative = _generate_narrative(raw_scores, text)
        
        # Detect maturity traits
        traits = _detect_maturity_traits(text)
        
        # Determine primary label
        primary_label = result['labels'][0] if result['labels'] else "unknown"
        
        return {
            "patent_score": patent_score,
            "label": primary_label,
            "narrative": narrative,
            "raw": raw_scores,
            "traits": traits
        }
        
    except Exception as e:
        print(f"Error in HF evaluation: {e}")
        return _fallback_analysis(text)

def _calculate_patent_score(raw_scores, weights):
    """
    Calculate the final patent score based on weighted classifications.
    """
    if not raw_scores:
        return 0
    
    total_weight = 0
    weighted_sum = 0
    
    for label, score in raw_scores.items():
        weight = weights.get(label, 1.0)
        # Convert confidence to percentage and apply weight
        score_contribution = score * 100 * weight
        weighted_sum += score_contribution
        total_weight += weight
    
    if total_weight == 0:
        return 0
    
    # Normalize to 0-100 scale
    final_score = (weighted_sum / total_weight) / len(raw_scores)
    return min(100, max(0, round(final_score, 1)))

def _generate_narrative(raw_scores, text):
    """
    Generate narrative insights based on classification results.
    """
    narrative = []
    
    # Sort scores by confidence
    sorted_scores = sorted(raw_scores.items(), key=lambda x: x[1], reverse=True)
    
    # Add top scoring categories to narrative
    for label, score in sorted_scores[:3]:
        if score > 0.1:  # Only include confident predictions
            narrative.append(f"Strong indication of {label.replace('-', ' ')} (confidence: {score:.2f})")
    
    # Add text-based insights
    text_lower = text.lower()
    
    if any(term in text_lower for term in ['nist', 'post-quantum', 'pqc']):
        narrative.append("References to NIST post-quantum cryptography standards")
    
    if any(term in text_lower for term in ['migration', 'roadmap', 'timeline']):
        narrative.append("Contains migration planning or timeline elements")
    
    if any(term in text_lower for term in ['implementation', 'deploy', 'rollout']):
        narrative.append("Discusses implementation strategies")
    
    return narrative

def _detect_maturity_traits(text):
    """
    Detect specific maturity indicators in the text.
    """
    text_lower = text.lower()
    
    traits = {
        'implementation_plan': any(term in text_lower for term in [
            'implementation plan', 'deployment plan', 'rollout strategy',
            'migration plan', 'execution plan'
        ]),
        'standards_reference': any(term in text_lower for term in [
            'nist', 'fips', 'iso', 'rfc', 'standard', 'specification',
            'pqc', 'post-quantum cryptography'
        ]),
        'roadmap_timeline': any(term in text_lower for term in [
            'roadmap', 'timeline', 'schedule', 'milestone', 'phase',
            'quarter', 'year', 'deadline', 'target date'
        ])
    }
    
    return traits

def _fallback_analysis(text):
    """
    Fallback analysis when HF classifier is not available.
    """
    text_lower = text.lower()
    
    # Basic keyword matching for quantum-related content
    quantum_keywords = [
        'quantum', 'post-quantum', 'pqc', 'cryptography', 'encryption',
        'quantum-safe', 'quantum-resistant', 'nist', 'lattice-based'
    ]
    
    matches = sum(1 for keyword in quantum_keywords if keyword in text_lower)
    
    # Simple scoring based on keyword density
    score = min(100, matches * 15)
    
    narrative = []
    if matches > 0:
        narrative.append(f"Found {matches} quantum-related keywords")
    
    traits = _detect_maturity_traits(text)
    
    return {
        "patent_score": score,
        "label": "keyword-based",
        "narrative": narrative,
        "raw": {"quantum-content": score / 100},
        "traits": traits
    }
