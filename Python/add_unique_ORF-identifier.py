input_file_path = 'PATH/TO/INPUT FILE'
output_file_path = 'PATH/TO/OUTPUT FILE'

# Open the input GTF file
with open(input_file_path, 'r') as input_file:
    # Open the output file for writing
    with open(output_file_path, 'w') as output_file:
        # Iterate over each line in the input file
        for line in input_file:
            columns = line.split('\t')  # Assuming columns are separated by tabs
            columns[3] = columns[0] + 'rcs'+ columns[1]  # Replace the value in the desired column AND name identifier
        
            modified_line = '\t'.join(columns)
            output_file.write(modified_line)

# Print a message to indicate the process is completed
print("Modified GTF file has been saved.")
