#!/usr/bin/env python3
"""
Script to extract text from all PDF files in the workshops directory using docling.
"""

from pathlib import Path
from docling.document_converter import DocumentConverter

def extract_pdf_to_markdown(pdf_path: str) -> str:
    """Extract text from PDF and convert to markdown."""
    converter = DocumentConverter()
    result = converter.convert(pdf_path)
    return result.document.export_to_markdown()

def main():
    workshops_dir = Path(__file__).parent
    pdf_files = list(workshops_dir.glob("*.pdf"))
    
    print(f"Found {len(pdf_files)} PDF files to process...")
    
    for pdf_file in sorted(pdf_files):
        chapter_name = pdf_file.stem  # e.g., "chapter6"
        output_file = workshops_dir / f"{chapter_name}-slides.md"
        
        print(f"Processing {pdf_file.name}...")
        
        try:
            markdown_content = extract_pdf_to_markdown(str(pdf_file))
            
            # Write to markdown file
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(f"# {chapter_name.title()} Slides\n\n")
                f.write("*Extracted from PDF slides using docling*\n\n")
                f.write("---\n\n")
                f.write(markdown_content)
            
            print(f"✓ Created {output_file.name}")
            
        except Exception as e:
            print(f"✗ Error processing {pdf_file.name}: {e}")
    
    print("\nDone!")

if __name__ == "__main__":
    main()