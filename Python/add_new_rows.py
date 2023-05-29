import csv

#write a function that takes rows
def process_row(row):
    chrom = row[0]
    start_codon = int(row[1])
    stop_codon = int(row[2])
    transcript_id = row[3]

    row1 = [chrom, 'genome','5UTR', start_codon - 50, start_codon - 1,'.', '+', '.',  f'ORF_id "{transcript_id}"; gene_id "{transcript_id}";']
    row2 = [chrom, 'genome', 'start_codon', start_codon, start_codon + 2, '.', '+', '.', f'ORF_id "{transcript_id}"; gene_id "{transcript_id}";']
    row3 = [chrom, 'genome', 'exon', start_codon, stop_codon - 3, '.', '+', '.', f'ORF_id "{transcript_id}"; gene_id "{transcript_id}";']
    row4 = [chrom, 'genome', 'CDS', start_codon, stop_codon - 3, '.', '+', '.', f'ORF_id "{transcript_id}"; gene_id "{transcript_id}";']
    row5 = [chrom, 'genome', 'stop_codon', stop_codon - 2, stop_codon, '.', '+', '.', f'ORF_id "{transcript_id}"; gene_id "{transcript_id}";']
    row6 = [chrom, 'genome', '3UTR', stop_codon + 1, stop_codon + 50, '.', '+', '.', f'ORF_id "{transcript_id}"; gene_id "{transcript_id}";']

    return [row1, row2, row3, row4, row5, row6]
 
#Read input and output file  
input_file = 'PATH/TO/INPUT FILE'
output_file = 'PATH/TO/OUTPUT FILE'

#open input file and read each row
with open(input_file, 'r') as file:
    reader = csv.reader(file, delimiter='\t')
    rows = [row for row in reader if not row[0].startswith('#')]

#apply function on the rows of input file
output_rows = []
for row in rows:
    processed_rows = process_row(row)
    output_rows.extend(processed_rows)

#write the processed rows in output file
with open(output_file, 'w', newline='') as file:
    writer = csv.writer(file, delimiter='\t')
    writer.writerows(output_rows)

print('Output file generated successfully.')
