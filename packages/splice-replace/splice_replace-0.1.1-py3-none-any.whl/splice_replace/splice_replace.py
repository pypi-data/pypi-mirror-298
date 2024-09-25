#!/usr/bin/env python
import sys
import subprocess

def extract_text(file_path, start_line, start_col, end_line, end_col):
    """Extract the text from the specified section of the file."""
    with open(file_path, 'r') as file:
        lines = file.readlines()

    selected_text = []
    if start_line == end_line:
        selected_text.append(lines[start_line][start_col:end_col])
    else:
        selected_text.append(lines[start_line][start_col:])
        for i in range(start_line + 1, end_line):
            selected_text.append(lines[i])
        selected_text.append(lines[end_line][:end_col])

    return ''.join(selected_text)

def replace_text_in_file(file_path, start_line, start_col, end_line, end_col, new_text):
    file_contents = ""
    with open(file_path, 'r') as file:
        file_contents = file.readlines()

    file_part1 = ""
    line_iter = 0
    while line_iter < start_line:
        file_part1 += file_contents[line_iter]
        line_iter += 1

    col_iter = 0
    while col_iter < start_col:
        file_part1 += file_contents[line_iter][col_iter]
        col_iter += 1

    while line_iter < end_line:
        line_iter += 1

    file_part2 = ""
    col_iter = end_col

    file_part2 += file_contents[line_iter][col_iter:]
    line_iter += 1

    while line_iter < len(file_contents):
        file_part2 += file_contents[line_iter]
        line_iter += 1

    with open(file_path, 'w') as file:
        file.write(file_part1 + new_text + file_part2)


def run_script(script_to_run, input_text):
    """Run the given script with the extracted text as input."""
    result = subprocess.run([script_to_run], input=input_text, text=True, capture_output=True, shell=True)
    return result.stdout

def main():
    #Check if the correct number of arguments are provided
    if len(sys.argv) != 7:
        print("Usage: python3 splice_replace.py <script_to_run> <file_path> <start_line> <start_col> <end_line> <end_col>")

    # Get the arguments: script_to_run, file_path, start_line, start_col, end_line, end_col
    script_to_run = sys.argv[1]
    file_path = sys.argv[2]
    start_line = int(sys.argv[3]) - 1
    start_col = int(sys.argv[4]) - 1
    end_line = int(sys.argv[5]) - 1
    end_col = int(sys.argv[6]) - 1

    # Step 1: Extract the selected text from the file
    selected_text = extract_text(file_path, start_line, start_col, end_line, end_col)

    # Step 2: Run the given script with the selected text passed as stdin
    processed_text = run_script(script_to_run, selected_text)

    # Step 3: Replace the selected text in the file with the processed output
    replace_text_in_file(file_path, start_line, start_col, end_line, end_col, processed_text)

if __name__ == "__main__":
    main()
