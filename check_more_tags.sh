#!/bin/bash

# Check that all blog posts have the <!-- more --> tag

missing_tag_files=()

echo "🔍 Checking blog posts for <!-- more --> tags..."

for file in docs/writing/posts/*.md; do
    if [ -f "$file" ]; then
        if ! grep -q "<!-- more -->" "$file"; then
            missing_tag_files+=("$file")
            echo "❌ Missing <!-- more --> tag in: $file"
        fi
    fi
done

if [ ${#missing_tag_files[@]} -eq 0 ]; then
    echo "✅ All blog posts have <!-- more --> tags"
    exit 0
else
    echo ""
    echo "🚨 Found ${#missing_tag_files[@]} blog post(s) missing <!-- more --> tags"
    echo "Please add <!-- more --> tags to separate the excerpt from the full content."
    exit 1
fi 