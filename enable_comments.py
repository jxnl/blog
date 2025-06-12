#!/usr/bin/env python3
"""
Enable comments in blog posts by adding 'comments: true' to front matter.
This script automatically adds the comments setting to any blog post that doesn't have it.
"""

import os
import re
import sys
from pathlib import Path


def has_comments_setting(content: str) -> bool:
    """Check if the front matter already has a comments setting."""
    # Look for comments: anywhere in the front matter (between --- blocks)
    frontmatter_pattern = r'^---\n(.*?)\n---'
    match = re.search(frontmatter_pattern, content, re.DOTALL | re.MULTILINE)
    
    if not match:
        return False
    
    frontmatter = match.group(1)
    return bool(re.search(r'^comments:\s*', frontmatter, re.MULTILINE))


def add_comments_to_frontmatter(content: str) -> str:
    """Add 'comments: true' to the front matter if it doesn't exist."""
    if has_comments_setting(content):
        return content
    
    # Pattern to match the front matter
    frontmatter_pattern = r'^(---\n)(.*?)(\n---)(.*)$'
    match = re.search(frontmatter_pattern, content, re.DOTALL | re.MULTILINE)
    
    if not match:
        print("Warning: No front matter found in file")
        return content
    
    start_delimiter = match.group(1)
    frontmatter_content = match.group(2)
    end_delimiter = match.group(3)
    rest_of_content = match.group(4)
    
    # Add comments: true after the existing front matter content
    new_frontmatter = frontmatter_content + "\ncomments: true"
    
    return start_delimiter + new_frontmatter + end_delimiter + rest_of_content


def process_blog_posts():
    """Process all blog posts and add comments setting where missing."""
    blog_posts_dir = Path("docs/writing/posts")
    
    if not blog_posts_dir.exists():
        print(f"Blog posts directory not found: {blog_posts_dir}")
        return 1
    
    modified_files = []
    
    for md_file in blog_posts_dir.glob("*.md"):
        try:
            with open(md_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            if not has_comments_setting(content):
                print(f"Adding comments setting to: {md_file}")
                new_content = add_comments_to_frontmatter(content)
                
                with open(md_file, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                
                modified_files.append(str(md_file))
        
        except Exception as e:
            print(f"Error processing {md_file}: {e}")
            return 1
    
    if modified_files:
        print(f"Modified {len(modified_files)} files:")
        for file in modified_files:
            print(f"  - {file}")
    else:
        print("No files needed modification - all blog posts already have comments setting")
    
    return 0


if __name__ == "__main__":
    sys.exit(process_blog_posts()) 