#!/bin/bash

# organizer.sh - Archive CSV files with timestamp and log actions

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Log file
LOG_FILE="organizer.log"

# Function to log messages
log_message() {
    local timestamp=$(date '+%Y-%m-%d %H:%M:%S')
    echo "[$timestamp] $1" >> "$LOG_FILE"
    echo -e "${GREEN}[$timestamp]${NC} $1"
}

# Function to log file content
log_file_content() {
    local file_path="$1"
    local new_name="$2"
    
    echo "=== Content of $file_path -> $new_name ===" >> "$LOG_FILE"
    if [[ -f "$file_path" ]]; then
        cat "$file_path" >> "$LOG_FILE"
    else
        echo "FILE NOT FOUND" >> "$LOG_FILE"
    fi
    echo "=== End of content ===" >> "$LOG_FILE"
    echo "" >> "$LOG_FILE"
}

# Main script
main() {
    echo "=== CSV File Organizer ==="
    
    # Create archive directory if it doesn't exist
    if [[ ! -d "archive" ]]; then
        mkdir -p archive
        log_message "Created archive directory"
    else
        log_message "Archive directory already exists"
    fi
    
    # Find all CSV files in current directory
    csv_files=$(find . -maxdepth 1 -name "*.csv" -type f | grep -v "/archive/")
    
    if [[ -z "$csv_files" ]]; then
        log_message "No CSV files found to archive"
        return 0
    fi
    
    # Count files for reporting
    file_count=$(echo "$csv_files" | wc -l)
    log_message "Found $file_count CSV file(s) to process"
    
    # Process each CSV file
    processed_count=0
    while IFS= read -r csv_file; do
        if [[ -z "$csv_file" ]]; then
            continue
        fi
        
        # Remove ./ prefix if present
        csv_file=$(echo "$csv_file" | sed 's|^\./||')
        
        # Skip if file is in archive directory
        if [[ "$csv_file" == archive/* ]]; then
            continue
        fi
        
        # Generate timestamp
        timestamp=$(date '+%Y%m%d-%H%M%S')
        
        # Extract filename without path
        filename=$(basename "$csv_file")
        
        # Create new filename with timestamp
        name_part="${filename%.*}"
        extension="${filename##*.}"
        new_filename="${name_part}-${timestamp}.${extension}"
        
        log_message "Processing: $csv_file -> archive/$new_filename"
        
        # Log file content before moving
        log_file_content "$csv_file" "$new_filename"
        
        # Move and rename file
        if mv "$csv_file" "archive/$new_filename"; then
            log_message "Successfully archived: $csv_file to archive/$new_filename"
            ((processed_count++))
        else
            log_message "Failed to archive: $csv_file"
        fi
        
    done <<< "$csv_files"
    
    log_message "Archiving complete. Processed $processed_count file(s)"
    echo "=== Organizer finished ==="
}

# Run main function
main "$@"
