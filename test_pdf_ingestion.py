"""
Test PDF Ingestion with Thumbnail Extraction
Demonstrates the complete PDF processing workflow
"""

import os
import base64
from utils.pdf_ingestion_thumbnails import process_uploaded_pdf_with_thumbnail

def test_pdf_processing():
    """Test PDF processing with sample document."""
    print("Testing PDF ingestion system...")
    
    # Check if we have any PDF files to test with
    pdf_files = []
    for filename in os.listdir('attached_assets'):
        if filename.lower().endswith('.pdf'):
            pdf_files.append(filename)
    
    if not pdf_files:
        print("No PDF files found in attached_assets directory for testing.")
        return
    
    test_pdf = pdf_files[0]
    print(f"Testing with: {test_pdf}")
    
    # Simulate uploaded file processing
    class MockUploadedFile:
        def __init__(self, file_path, name):
            self.file_path = file_path
            self.name = name
            self._content = None
            
        def read(self):
            if self._content is None:
                with open(self.file_path, 'rb') as f:
                    self._content = f.read()
            return self._content
            
        def seek(self, pos):
            pass  # Mock seek operation
    
    # Test PDF processing
    try:
        mock_file = MockUploadedFile(f'attached_assets/{test_pdf}', test_pdf)
        doc_id = 999999  # Test document ID
        
        result = process_uploaded_pdf_with_thumbnail(mock_file, doc_id)
        
        print(f"Processing results:")
        print(f"- Text extracted: {len(result['text_content'])} characters")
        print(f"- Thumbnail generated: {result['thumbnail_data'] is not None}")
        print(f"- File type: {result['file_type']}")
        print(f"- Filename: {result['filename']}")
        
        # Check if thumbnail file was created
        thumbnail_path = f"thumbnails/ingested_thumb_{doc_id}.png"
        if os.path.exists(thumbnail_path):
            print(f"- Thumbnail saved to: {thumbnail_path}")
            
            # Get file size for verification
            size = os.path.getsize(thumbnail_path)
            print(f"- Thumbnail size: {size} bytes")
        else:
            print("- Thumbnail file not found")
        
        print("\n✓ PDF ingestion test completed successfully!")
        
    except Exception as e:
        print(f"✗ PDF processing failed: {e}")

if __name__ == "__main__":
    test_pdf_processing()