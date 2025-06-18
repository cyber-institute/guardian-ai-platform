#!/usr/bin/env python3
"""
Metadata Integrity Validator
Automated system to verify metadata extraction remains intact during code changes
"""

import os
import psycopg2
import json
from typing import Dict, List, Tuple, Optional

class MetadataIntegrityValidator:
    """Validates that critical metadata extraction functionality remains intact"""
    
    def __init__(self):
        self.critical_test_cases = {
            58: {
                'title': 'Quantum Science for Inclusion and Sustainability',
                'organization': 'UNESCO',
                'author_organization': 'UNESCO'
            },
            63: {
                'title': 'Recommendation on the Ethics of Artificial Intelligence',
                'organization': 'UNESCO',
                'author_organization': 'UNESCO',
                'publication_date': '2021-11-23'
            }
        }
    
    def validate_metadata_integrity(self) -> Dict[str, bool]:
        """Validate that critical documents maintain correct metadata"""
        
        results = {
            'all_tests_passed': True,
            'individual_tests': {},
            'errors': []
        }
        
        try:
            conn = psycopg2.connect(os.getenv('DATABASE_URL'))
            cursor = conn.cursor()
            
            for doc_id, expected_metadata in self.critical_test_cases.items():
                test_result = self._validate_single_document(cursor, doc_id, expected_metadata)
                results['individual_tests'][doc_id] = test_result
                
                if not test_result['passed']:
                    results['all_tests_passed'] = False
                    results['errors'].extend(test_result['errors'])
            
            cursor.close()
            conn.close()
            
        except Exception as e:
            results['all_tests_passed'] = False
            results['errors'].append(f"Database connection error: {str(e)}")
        
        return results
    
    def _validate_single_document(self, cursor, doc_id: int, expected: Dict) -> Dict:
        """Validate a single document's metadata"""
        
        result = {
            'passed': True,
            'errors': [],
            'actual_values': {}
        }
        
        try:
            cursor.execute("""
                SELECT title, organization, author_organization, publication_date, publish_date
                FROM documents WHERE id = %s
            """, (doc_id,))
            
            row = cursor.fetchone()
            if not row:
                result['passed'] = False
                result['errors'].append(f"Document {doc_id} not found")
                return result
            
            actual = {
                'title': row[0],
                'organization': row[1],
                'author_organization': row[2],
                'publication_date': str(row[3]) if row[3] else None,
                'publish_date': str(row[4]) if row[4] else None
            }
            
            result['actual_values'] = actual
            
            # Validate each expected field
            for field, expected_value in expected.items():
                if field in actual:
                    if actual[field] != expected_value:
                        result['passed'] = False
                        result['errors'].append(
                            f"Document {doc_id} {field}: expected '{expected_value}', got '{actual[field]}'"
                        )
                else:
                    result['passed'] = False
                    result['errors'].append(f"Document {doc_id} missing field: {field}")
            
            # Special validation for date fields synchronization
            if doc_id == 63:  # UNESCO ethics document should have synchronized dates
                if actual['publication_date'] != actual['publish_date']:
                    result['passed'] = False
                    result['errors'].append(
                        f"Document {doc_id} date fields not synchronized: "
                        f"publication_date={actual['publication_date']}, publish_date={actual['publish_date']}"
                    )
        
        except Exception as e:
            result['passed'] = False
            result['errors'].append(f"Validation error for document {doc_id}: {str(e)}")
        
        return result
    
    def generate_integrity_report(self) -> str:
        """Generate a comprehensive integrity report"""
        
        validation_results = self.validate_metadata_integrity()
        
        report = ["METADATA INTEGRITY VALIDATION REPORT"]
        report.append("=" * 50)
        
        if validation_results['all_tests_passed']:
            report.append("✅ ALL TESTS PASSED - Metadata extraction integrity maintained")
        else:
            report.append("❌ TESTS FAILED - Metadata extraction integrity compromised")
        
        report.append("")
        report.append("Individual Test Results:")
        
        for doc_id, test_result in validation_results['individual_tests'].items():
            expected = self.critical_test_cases[doc_id]
            
            if test_result['passed']:
                report.append(f"✅ Document {doc_id}: PASSED")
                report.append(f"   Title: {test_result['actual_values'].get('title', 'N/A')}")
                report.append(f"   Organization: {test_result['actual_values'].get('organization', 'N/A')}")
            else:
                report.append(f"❌ Document {doc_id}: FAILED")
                for error in test_result['errors']:
                    report.append(f"   ERROR: {error}")
        
        if validation_results['errors']:
            report.append("")
            report.append("System Errors:")
            for error in validation_results['errors']:
                report.append(f"❌ {error}")
        
        report.append("")
        report.append("=" * 50)
        
        return "\n".join(report)
    
    def create_emergency_restore_point(self) -> bool:
        """Create an emergency restore point with current working metadata"""
        
        try:
            conn = psycopg2.connect(os.getenv('DATABASE_URL'))
            cursor = conn.cursor()
            
            restore_data = {}
            
            for doc_id in self.critical_test_cases.keys():
                cursor.execute("""
                    SELECT title, organization, author_organization, publication_date, publish_date
                    FROM documents WHERE id = %s
                """, (doc_id,))
                
                row = cursor.fetchone()
                if row:
                    restore_data[doc_id] = {
                        'title': row[0],
                        'organization': row[1],
                        'author_organization': row[2],
                        'publication_date': str(row[3]) if row[3] else None,
                        'publish_date': str(row[4]) if row[4] else None
                    }
            
            # Save restore point
            with open('metadata_restore_point.json', 'w') as f:
                json.dump(restore_data, f, indent=2, default=str)
            
            cursor.close()
            conn.close()
            
            return True
            
        except Exception as e:
            print(f"Failed to create restore point: {str(e)}")
            return False

def run_integrity_check():
    """Run the integrity check and display results"""
    
    validator = MetadataIntegrityValidator()
    report = validator.generate_integrity_report()
    print(report)
    
    # Create restore point if tests pass
    validation_results = validator.validate_metadata_integrity()
    if validation_results['all_tests_passed']:
        if validator.create_emergency_restore_point():
            print("\n✅ Emergency restore point created successfully")
        else:
            print("\n❌ Failed to create emergency restore point")
    
    return validation_results['all_tests_passed']

if __name__ == "__main__":
    run_integrity_check()