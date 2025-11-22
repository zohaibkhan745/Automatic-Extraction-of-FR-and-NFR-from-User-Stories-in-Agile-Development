"""
Main application file for FR/NFR Extraction System
Command-line interface for testing the system
"""

import sys
from requirement_classifier import RequirementClassifier

def main():
    """Main function to run the FR/NFR extraction system"""
    
    print("\n" + "=" * 60)
    print("FR/NFR EXTRACTION SYSTEM")
    print("Automatic Extraction of Functional and Non-Functional Requirements")
    print("=" * 60 + "\n")
    
    classifier = RequirementClassifier()
    
    # Check if file input is provided
    if len(sys.argv) > 1:
        filename = sys.argv[1]
        try:
            with open(filename, 'r', encoding='utf-8') as f:
                text = f.read()
            print(f"Processing file: {filename}\n")
        except FileNotFoundError:
            print(f"Error: File '{filename}' not found.")
            return
        except Exception as e:
            print(f"Error reading file: {e}")
            return
    else:
        # Interactive input
        print("Enter your user stories (press Enter twice when done):")
        print("-" * 60)
        
        lines = []
        empty_count = 0
        
        while True:
            try:
                line = input()
                if line.strip() == "":
                    empty_count += 1
                    if empty_count >= 2:
                        break
                else:
                    empty_count = 0
                    lines.append(line)
            except EOFError:
                break
        
        text = "\n".join(lines)
    
    if not text.strip():
        print("No input provided. Exiting.")
        return
    
    # Classify requirements
    print("\nProcessing...\n")
    results = classifier.classify_text(text)
    
    # Display results
    output = classifier.format_output(results)
    print(output)
    
    # Option to save results
    save = input("\nWould you like to save the results to a file? (y/n): ")
    if save.lower() == 'y':
        output_file = input("Enter output filename (default: results.txt): ").strip()
        if not output_file:
            output_file = "results.txt"
        
        try:
            with open(output_file, 'w', encoding='utf-8') as f:
                f.write(output)
            print(f"\nResults saved to {output_file}")
        except Exception as e:
            print(f"Error saving file: {e}")


if __name__ == "__main__":
    main()
