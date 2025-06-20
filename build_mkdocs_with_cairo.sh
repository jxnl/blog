#!/bin/bash
# Build script with cairo library path fix for macOS

# Set cairo library path for macOS
if [[ "$OSTYPE" == "darwin"* ]]; then
    export DYLD_FALLBACK_LIBRARY_PATH="/opt/homebrew/lib:$DYLD_FALLBACK_LIBRARY_PATH"
fi

# Build the MkDocs site
mkdocs build "$@"