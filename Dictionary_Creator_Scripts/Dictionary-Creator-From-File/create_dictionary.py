#!/usr/bin/python3
import argparse
import sys


def extract_unique_words(input_file: str, output_file: str)->None:
    """
    Create dictionary from file
    """
    unique_words = set()
    
    with open(input_file, 'r') as infile:
        text = infile.read()
        words = text.split()
        
        unique_words.update(words)
    
    with open(output_file, 'w') as outfile:
        for word in sorted(unique_words):
            outfile.write(f"{word}\n")
    return


def main()->None:
    # Get arguments from user
    parser = argparse.ArgumentParser(description="Dictionary creator.")
    
    parser.add_argument('input_file', type=str, help="File to create dictionary.")
    parser.add_argument('output_file', type=str, help="File to save dictionary.")
    
    args = parser.parse_args()

    # Check arguments provided
    if len(sys.argv) != 3:
        print(f"Example usage: python3 {sys.argv[0]} <input_file_to_create_dictionary> <output_save_file>")
        sys.exit(1)
    
    # Create dictionary
    extract_unique_words(args.input_file, args.output_file)


if __name__ == "__main__":
    main()
