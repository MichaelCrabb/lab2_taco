#!/bin/bash

# search_schedules.sh - Script to search through TACO schedule files
# Usage: ./search_schedules.sh [options] [search_pattern]
#   or:  ./search_schedules.sh -d [directory_path] [other_options]
#   or:  ./search_schedules.sh -s [specific_operation] -l [loop_var]
#   or:  ./search_schedules.sh --seq "unroll unroll"   # Find schedules starting with two unrolls
#
# Examples:
#   ./search_schedules.sh -d ../path/to/complex "unroll"     # Search in specific directory
#   ./search_schedules.sh -s split -l i                      # Find splits of loop i
#   ./search_schedules.sh "interchange i0 j0"                # Find specific interchange
#   ./search_schedules.sh -c                                 # Count operations per schedule

# Default directory is "./complex"
SCHEDULE_DIR="./complex"

# Function to check if directory exists and contains .schedule files
check_directory() {
    local dir="$1"
    if [ ! -d "$dir" ]; then
        echo "Error: Directory '$dir' not found!"
        exit 1
    fi
    
    if ! ls "$dir"/*.schedule >/dev/null 2>&1; then
        echo "Error: No .schedule files found in '$dir'"
        exit 1
    fi
}

# Function to count operations in each schedule
count_operations() {
    local dir="$1"
    echo "Operation counts per schedule in $dir:"
    echo "-----------------------------"
    for file in "$dir"/*.schedule; do
        if [ -f "$file" ]; then
            echo -n "$(basename "$file"): "
            wc -l < "$file"
        fi
    done
}

# Function to show statistics about operations
show_stats() {
    local dir="$1"
    echo "Operation Statistics in $dir:"
    echo "-------------------"
    echo "Unroll operations:"
    grep -r "unroll" "$dir"/ | wc -l
    echo "Split operations:"
    grep -r "split" "$dir"/ | wc -l
    echo "Interchange operations:"
    grep -r "interchange" "$dir"/ | wc -l
}

# Function to search for sequences of operations
search_sequence() {
    local dir="$1"
    local sequence="$2"
    echo "Searching for schedules with sequence: $sequence"
    echo "In directory: $dir"
    echo "Found files:"
    
    # Split sequence into operations
    read -ra ops <<< "$sequence"
    
    for file in "$dir"/*.schedule; do
        if [ -f "$file" ]; then
            # Read first N lines based on sequence length
            head -n ${#ops[@]} "$file" > /tmp/schedule_head.txt
            match=true
            
            # Check if each line matches corresponding operation
            for i in "${!ops[@]}"; do
                line=$(sed -n "$((i+1))p" /tmp/schedule_head.txt)
                if ! [[ "$line" == *"${ops[$i]}"* ]]; then
                    match=false
                    break
                fi
            done
            
            if [ "$match" = true ]; then
                echo "$(basename "$file")"
                echo "First ${#ops[@]} operations:"
                cat /tmp/schedule_head.txt
                echo "-----------------------"
            fi
        fi
    done
    
    rm -f /tmp/schedule_head.txt
}

# Parse command line arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        -d|--directory)
            SCHEDULE_DIR="$2"
            shift 2
            ;;
        -s|--specific)
            operation="$2"
            shift 2
            ;;
        -l|--loop)
            loop="$2"
            shift 2
            ;;
        -c|--count)
            check_directory "$SCHEDULE_DIR"
            count_operations "$SCHEDULE_DIR"
            exit 0
            ;;
        --seq|--sequence)
            check_directory "$SCHEDULE_DIR"
            search_sequence "$SCHEDULE_DIR" "$2"
            exit 0
            ;;
        -h|--help)
            echo "Usage:"
            echo "  ./search_schedules.sh -d [directory]              Specify directory containing schedules"
            echo "  ./search_schedules.sh [search_pattern]           Search for a pattern"
            echo "  ./search_schedules.sh -s [operation] -l [loop]   Search specific operation and loop"
            echo "  ./search_schedules.sh -c                         Count operations per schedule"
            echo "  ./search_schedules.sh --stats                    Show operation statistics"
            echo "  ./search_schedules.sh --seq \"op1 op2\"            Find schedules with specific operation sequence"
            echo ""
            echo "The script will look for schedules in './complex' by default."
            echo "Use -d option to specify a different directory."
            exit 0
            ;;
        --stats)
            check_directory "$SCHEDULE_DIR"
            show_stats "$SCHEDULE_DIR"
            exit 0
            ;;
        *)
            # Direct pattern search
            check_directory "$SCHEDULE_DIR"
            echo "Searching for: $1"
            echo "In directory: $SCHEDULE_DIR"
            echo "Found in:"
            grep -l "$1" "$SCHEDULE_DIR"/*.schedule
            echo -e "\nMatching lines:"
            grep -n "$1" "$SCHEDULE_DIR"/*.schedule
            exit 0
            ;;
    esac
done

# If specific operation and loop are provided
if [ ! -z "$operation" ] && [ ! -z "$loop" ]; then
    check_directory "$SCHEDULE_DIR"
    echo "Searching for ${operation} operations on loop ${loop}"
    echo "In directory: $SCHEDULE_DIR"
    echo "Found in:"
    grep -l "${operation}.*${loop}" "$SCHEDULE_DIR"/*.schedule
    echo -e "\nMatching lines:"
    grep -n "${operation}.*${loop}" "$SCHEDULE_DIR"/*.schedule
fi 