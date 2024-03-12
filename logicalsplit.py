def split_cobol_file(input_file_path):
    # Known divisions and sections
    divisions = ['IDENTIFICATION DIVISION', 'ENVIRONMENT DIVISION', 'DATA DIVISION', 'PROCEDURE DIVISION']
    sections = ['CONFIGURATION SECTION', 'INPUT-OUTPUT SECTION', 'FILE SECTION', 'WORKING-STORAGE SECTION', 'LOCAL-STORAGE SECTION', 'LINKAGE SECTION']

    # Initialize tracking variables
    current_division = None
    current_section = None
    content = {}

    # Function to add content to the appropriate part
    def add_content(line, division, section=None):
        key = division if not section else f"{division}-{section}"
        if key not in content:
            content[key] = []
        content[key].append(line)

    with open(input_file_path, 'r') as file:
        for line in file:
            stripped_line = line.strip()
            # Check for division
            if any(div in stripped_line for div in divisions):
                current_division = [div for div in divisions if div in stripped_line][0]
                current_section = None  # Reset current section for new division
            # Check for section within the current division
            elif any(sec in stripped_line for sec in sections):
                current_section = [sec for sec in sections if sec in stripped_line][0]
            # Add content to the current division or section
            add_content(line, current_division, current_section)

    # Write the collected content to files
    for key, lines in content.items():
        filename_key = key.replace(' ', '_').lower()
        output_file_path = f"{filename_key}.txt"
        with open(output_file_path, 'w') as output_file:
            output_file.writelines(lines)
            print(f"Written {key} to {output_file_path}")

# Example usage
input_file_path = 'path/to/your/cobol/source/file.cbl'
split_cobol_file(input_file_path)
