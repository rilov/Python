def count_tokens(text):
    # Simple token counter based on word boundaries
    return len(re.findall(r'\w+', text))

def identify_division_start(line):
    # Enhanced detection for the start of a division
    match = re.match(r'^\s{6}([A-Z]+ DIVISION)\.', line)
    return match.group(1) if match else None

def split_cobol_file(file_path, max_tokens):
    division_regex = re.compile(r'^\s{6}[A-Z]+ DIVISION\.')
    current_division_lines = []
    current_division_name = ""
    part_number = 1

    with open(file_path, 'r') as cobol_file:
        for line in cobol_file:
            division_start = identify_division_start(line)
            if division_start:
                # When a new division starts, process the current division if it exists
                if current_division_lines:
                    process_division(current_division_name, current_division_lines, part_number, max_tokens)
                    current_division_lines = []
                    part_number = 1  # Reset part number for the new division
                current_division_name = division_start
            current_division_lines.append(line)

    # Process the last collected division
    if current_division_lines:
        process_division(current_division_name, current_division_lines, part_number, max_tokens)

def process_division(division_name, division_lines, part_number, max_tokens):
    buffer = ""
    buffer_token_count = 0
    for line in division_lines:
        line_token_count = count_tokens(line)
        if buffer_token_count + line_token_count > max_tokens:
            write_to_file(f"{division_name}_part{part_number}.cob", buffer)
            buffer = line  # Start new buffer with current line
            buffer_token_count = line_token_count
            part_number += 1
        else:
            buffer += line
            buffer_token_count += line_token_count

    if buffer:  # Write the remaining buffer for the division
        write_to_file(f"{division_name}_part{part_number}.cob", buffer)

def write_to_file(filename, content):
    filename = filename.replace(" ", "_")  # Ensure filename is file-system friendly
    with open(filename, 'w') as file:
        file.write(content)
    print(f"Written to {filename}")

# Example usage
file_path = 'your_cobol_file.cob'
max_tokens = 15000  # Adjust based on token limit
split_cobol_file(file_path, max_tokens)
