#!/usr/bin/env python3
"""
Fix quantum cybersecurity scoring to use tier system (1-5) instead of 0-100
"""

def fix_quantum_tier_system():
    """Fix quantum cybersecurity scoring in all_docs_tab.py"""
    
    # Read the file
    with open('all_docs_tab.py', 'r') as f:
        content = f.read()
    
    # Replace all instances of quantum cybersecurity 0-100 scoring with tier system
    # Pattern 1: Card view quantum scoring
    old_pattern_1 = """                if raw_scores['quantum_cybersecurity'] and raw_scores['quantum_cybersecurity'] > 0:
                    # Use existing DB score with boost
                    quantum_cyber_score = min(raw_scores['quantum_cybersecurity'] + 18, 100)
                    scores['quantum_cybersecurity'] = max(quantum_cyber_score, 85) if quantum_cyber_score > 60 else quantum_cyber_score
                else:
                    # Generate score for quantum documents with missing DB scores
                    try:
                        computed_scores = comprehensive_document_scoring(raw_content, title)
                        scores['quantum_cybersecurity'] = computed_scores.get('quantum_cybersecurity', 65)
                    except:
                        scores['quantum_cybersecurity'] = 65  # Default reasonable score for quantum docs"""
    
    new_pattern_1 = """                if raw_scores['quantum_cybersecurity'] and raw_scores['quantum_cybersecurity'] > 0:
                    # Use existing DB score
                    quantum_score = raw_scores['quantum_cybersecurity']
                else:
                    # Generate score for quantum documents with missing DB scores
                    try:
                        computed_scores = comprehensive_document_scoring(raw_content, title)
                        quantum_score = computed_scores.get('quantum_cybersecurity', 65)
                    except:
                        quantum_score = 65  # Default reasonable score for quantum docs
                
                # Convert to tier system (1-5)
                if quantum_score >= 85:
                    scores['quantum_cybersecurity'] = 5
                elif quantum_score >= 70:
                    scores['quantum_cybersecurity'] = 4
                elif quantum_score >= 55:
                    scores['quantum_cybersecurity'] = 3
                elif quantum_score >= 40:
                    scores['quantum_cybersecurity'] = 2
                else:
                    scores['quantum_cybersecurity'] = 1"""
    
    # Replace all occurrences
    content = content.replace(old_pattern_1, new_pattern_1)
    
    # Fix the color logic for quantum cybersecurity (tier-based)
    old_color_pattern = """            # Quantum Cybersecurity color (same as other views)
            if q_cyber != 'N/A' and q_cyber >= 75:
                q_cyber_color = '#28a745'  # Green
            elif q_cyber != 'N/A' and q_cyber >= 50:
                q_cyber_color = '#fd7e14'  # Orange
            elif q_cyber != 'N/A':
                q_cyber_color = '#dc3545'  # Red
            else:
                q_cyber_color = '#6c757d'  # Gray"""
    
    new_color_pattern = """            # Quantum Cybersecurity color (tier-based 1-5)
            if q_cyber != 'N/A' and q_cyber >= 4:
                q_cyber_color = '#28a745'  # Green
            elif q_cyber != 'N/A' and q_cyber >= 3:
                q_cyber_color = '#fd7e14'  # Orange
            elif q_cyber != 'N/A':
                q_cyber_color = '#dc3545'  # Red
            else:
                q_cyber_color = '#6c757d'  # Gray"""
    
    content = content.replace(old_color_pattern, new_color_pattern)
    
    # Fix the display format for quantum cybersecurity (back to /5)
    old_display_pattern = """            # Display score boxes with colored text only (consistent 0-100 format)
            ai_cyber_display = f"{ai_cyber}/100" if ai_cyber != 'N/A' else "N/A"
            ai_ethics_display = f"{ai_ethics}/100" if ai_ethics != 'N/A' else "N/A"
            q_cyber_display = f"{q_cyber}/100" if q_cyber != 'N/A' else "N/A"
            q_ethics_display = f"{q_ethics}/100" if q_ethics != 'N/A' else "N/A" """
    
    new_display_pattern = """            # Display score boxes with colored text (tier system for quantum cyber)
            ai_cyber_display = f"{ai_cyber}/100" if ai_cyber != 'N/A' else "N/A"
            ai_ethics_display = f"{ai_ethics}/100" if ai_ethics != 'N/A' else "N/A"
            q_cyber_display = f"{q_cyber}/5" if q_cyber != 'N/A' else "N/A"
            q_ethics_display = f"{q_ethics}/100" if q_ethics != 'N/A' else "N/A" """
    
    content = content.replace(old_display_pattern, new_display_pattern)
    
    # Also fix compact cards display format
    old_compact_display = """            # Display compact colored scores (consistent 0-100 format)
            ai_cyber_display = f"{ai_cyber}/100" if ai_cyber != 'N/A' else "N/A"
            ai_ethics_display = f"{ai_ethics}/100" if ai_ethics != 'N/A' else "N/A"
            q_cyber_display = f"{q_cyber}/100" if q_cyber != 'N/A' else "N/A"
            q_ethics_display = f"{q_ethics}/100" if q_ethics != 'N/A' else "N/A" """
    
    new_compact_display = """            # Display compact colored scores (tier system for quantum cyber)
            ai_cyber_display = f"{ai_cyber}/100" if ai_cyber != 'N/A' else "N/A"
            ai_ethics_display = f"{ai_ethics}/100" if ai_ethics != 'N/A' else "N/A"
            q_cyber_display = f"{q_cyber}/5" if q_cyber != 'N/A' else "N/A"
            q_ethics_display = f"{q_ethics}/100" if q_ethics != 'N/A' else "N/A" """
    
    content = content.replace(old_compact_display, new_compact_display)
    
    # Write the file back
    with open('all_docs_tab.py', 'w') as f:
        f.write(content)
    
    print("✓ Fixed quantum cybersecurity to use tier system (1-5)")
    print("✓ Updated color logic for tier-based scoring")
    print("✓ Fixed display format to show /5 for quantum cybersecurity")

if __name__ == "__main__":
    fix_quantum_tier_system()