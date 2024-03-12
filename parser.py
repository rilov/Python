import re

def is_division_line(line):
    # A simple check for division headers. Might need adjustments for edge cases.
    return re.match(r'\s{6}[A-Z]+ DIVISION\.', line)

def count_tokens(line):
    # A simple approximation of token counting; adjust as needed.
    return len(line.strip().split())

def write_buffer_to_file(filename, buffer):
    with open(filename, 'w') as out_file:
        out_file.write(buffer)
    print(f"Written to {filename}")

def split_cobol_file(file_path):
    max_tokens = 15000
    token_count = 0
    buffer = ''
    file_count = 1
    division_count = 1
    
    with open(file_path, 'r') as file:
        lines = file.readlines()
    
    for i, line in enumerate(lines):
        if is_division_line(line):
            if buffer:
                # Write the current buffer to file before starting a new division
                write_buffer_to_file(f"{file_path}_part{file_count}_div{division_count}.cob", buffer)
                file_count += 1
                buffer = ''
                token_count = 0
            division_count += 1
            
        tokens_in_line = count_tokens(line)
        if token_count + tokens_in_line > max_tokens:
            # If adding this line exceeds max tokens, write buffer to file and reset
            write_buffer_to_file(f"{file_path}_part{file_count}_div{division_count}.cob", buffer)
            file_count += 1
            buffer = line
            token_count = tokens_in_line
        else:
            buffer += line
            token_count += tokens_in_line
    
    if buffer:
        # Write any remaining buffer to file
        write_buffer_to_file(f"{file_path}_part{file_count}_div{division_count}.cob", buffer)

# Replace 'your_cobol_file.cob' with the path to your COBOL code file
split_cobol_file('your_cobol_file.cob')
