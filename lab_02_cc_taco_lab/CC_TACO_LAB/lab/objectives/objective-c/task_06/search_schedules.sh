#!/bin/bash

# search_schedules.sh - Script to search through TACO schedule files
# Usage: ./search_schedules.sh [search_pattern]
#   or:  ./search_schedules.sh -s [specific_operation] -l [loop_var]
#
# Examples:
#   ./search_schedules.sh "unroll"              # Find all unroll operations
#   ./search_schedules.sh -s split -l i         # Find splits of loop i
#   ./search_schedules.sh "interchange i0 j0"   # Find specific interchange
#   ./search_schedules.sh -c                    # Count operations per schedule

# Check if complex directory exists
if [ ! -d "complex" ]; then
    echo "Error: 'complex' directory not found!"
    exit 1
fi

# Function to count operations in each schedule
count_operations() {
    echo "Operation counts per schedule:"
    echo "-----------------------------"
    for file in complex/*.schedule; do
        if [ -f "$file" ]; then
            echo -n "$(basename "$file"): "
            wc -l < "$file"
        fi
    done
}

# Function to show statistics about operations
show_stats() {
    echo "Operation Statistics:"
    echo "-------------------"
    echo "Unroll operations:"
    grep -r "unroll" complex/ | wc -l
    echo "Split operations:"
    grep -r "split" complex/ | wc -l
    echo "Interchange operations:"
    grep -r "interchange" complex/ | wc -l
}

# Function to search for sequences of operations
search_sequence() {
    local sequence="$1"
    echo "Searching for schedules with sequence: $sequence"
    echo "Found files:"
    
    # Split sequence into operations
    read -ra ops <<< "$sequence"
    
    for file in complex/*.schedule; do
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
        -s|--specific)
            operation="$2"
            shift 2
            ;;
        -l|--loop)
            loop="$2"
            shift 2
            ;;
        -c|--count)
            count_operations
            exit 0
            ;;
        --seq|--sequence)
            search_sequence "$2"
            exit 0
            ;;
        -h|--help)
            echo "Usage:"
            echo "  ./search_schedules.sh [search_pattern]           Search for a pattern"
            echo "  ./search_schedules.sh -s [operation] -l [loop]   Search specific operation and loop"
            echo "  ./search_schedules.sh -c                         Count operations per schedule"
            echo "  ./search_schedules.sh --stats                    Show operation statistics"
            echo "  ./search_schedules.sh --seq \"op1 op2\"            Find schedules with specific operation sequence"
            exit 0
            ;;
        --stats)
            show_stats
            exit 0
            ;;
        *)
            # Direct pattern search
            echo "Searching for: $1"
            echo "Found in:"
            grep -l "$1" complex/*.schedule
            echo -e "\nMatching lines:"
            grep -n "$1" complex/*.schedule
            exit 0
            ;;
    esac
done

# If specific operation and loop are provided
if [ ! -z "$operation" ] && [ ! -z "$loop" ]; then
    echo "Searching for ${operation} operations on loop ${loop}"
    echo "Found in:"
    grep -l "${operation}.*${loop}" complex/*.schedule
    echo -e "\nMatching lines:"
    grep -n "${operation}.*${loop}" complex/*.schedule
fi 