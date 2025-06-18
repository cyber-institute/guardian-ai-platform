# METADATA EXTRACTION & SCORING ENGINE PROTECTION SYSTEM
## CRITICAL: DO NOT MODIFY THESE COMPONENTS WITHOUT EXPLICIT PERMISSION
## BOTH METADATA EXTRACTION AND SCORING ENGINE ARE NOW PROTECTED

## Protected Components (HANDS OFF)
These files contain WORKING metadata extraction logic that correctly identifies:
- UNESCO documents and proper titles
- Organization detection from URLs and content
- Date field mapping synchronization

### Core Protected Files:
1. `utils/enhanced_metadata_extractor.py` - Universal title and organization extraction
2. `universal_metadata_extraction_fix.py` - Retroactive metadata correction system
3. Database field mappings for `publication_date` and `publish_date` synchronization

### Enhanced Scoring System (PROTECTED):
4. `utils/enhanced_content_analyzer.py` - Content depth analysis engine
5. `utils/comprehensive_scoring.py` - Enhanced scoring with content analysis
6. `utils/metadata_integrity_validator.py` - Automated integrity validation

### Protected Functions:
- `_extract_title()` - Contains UNESCO and NIST document patterns
- `_extract_organization()` - URL and content-based organization detection
- Date field synchronization logic
- `analyze_document_content_depth()` - Content depth analysis
- Enhanced scoring functions with content multipliers
- `score_ai_cybersecurity()` - AI cybersecurity scoring with content analysis
- `score_ai_ethics()` - AI ethics scoring with content analysis
- `score_quantum_cybersecurity()` - Quantum cybersecurity scoring
- `score_quantum_ethics()` - Quantum ethics scoring
- `analyze_document_applicability()` - Document topic applicability analysis

### Scoring Engine Protection Rules:
1. NEVER revert to keyword-only scoring
2. NEVER remove content depth analysis
3. NEVER modify content multipliers without testing
4. ALWAYS preserve N/A scoring for documents with minimal topic coverage
5. ALWAYS maintain protection against AI drift in scoring logic

## Working Test Cases (DO NOT BREAK):
- Document ID 58: "Quantum Science for Inclusion and Sustainability" | UNESCO
- Document ID 63: "Recommendation on the Ethics of Artificial Intelligence" | UNESCO | 2021-11-23

## Future Modification Rules:
1. **SCORING FIXES**: Only modify `utils/comprehensive_scoring.py` and scoring-related functions
2. **NEW FEATURES**: Create new files, do not modify existing metadata extraction logic
3. **TESTING**: Always verify UNESCO documents retain correct metadata after any changes
4. **ROLLBACK PLAN**: Keep `universal_metadata_extraction_fix.py` as emergency restore tool

## Verification Commands:
```bash
# Verify metadata integrity after any changes
python -c "
import psycopg2
import os
conn = psycopg2.connect(os.getenv('DATABASE_URL'))
cursor = conn.cursor()
cursor.execute('SELECT id, title, organization FROM documents WHERE id IN (58, 63)')
docs = cursor.fetchall()
for doc in docs:
    print(f'ID {doc[0]}: {doc[1]} | {doc[2]}')
cursor.close()
conn.close()
"
```

## Emergency Restore:
If metadata extraction breaks, run: `python universal_metadata_extraction_fix.py`

---
**REMINDER**: These fixes solved critical metadata misidentification issues. 
Any changes to metadata extraction must preserve UNESCO document recognition patterns.