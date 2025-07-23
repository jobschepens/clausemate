#!/usr/bin/env python3
"""
Check the format of the gotofiles/2.tsv file.
"""

def check_file_format():
    try:
        with open("data/input/gotofiles/2.tsv", 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        print(f"File has {len(lines)} lines")
        print("\nFirst 20 lines:")
        for i, line in enumerate(lines[:20]):
            print(f"{i+1:2d}: {line.rstrip()}")
        
        print("\nLines with #Text=:")
        for i, line in enumerate(lines):
            if line.startswith("#Text="):
                print(f"Line {i+1}: {line.rstrip()}")
                # Show next few lines to see sentence numbers
                for j in range(1, 5):
                    if i + j < len(lines):
                        next_line = lines[i + j].rstrip()
                        if next_line and not next_line.startswith("#"):
                            print(f"    Next: {next_line}")
                            break
                print()
        
    except Exception as e:
        print(f"Error reading file: {e}")

if __name__ == '__main__':
    check_file_format()
