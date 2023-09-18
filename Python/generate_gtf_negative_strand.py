import csv

def process_row_cds(rows):
    output_rows = []
    last_stop_codon = None  # Initialize last_stop_codon to None

    # Sort the rows by start_codon in descending order for negative strand genes
    rows.sort(key=lambda row: int(row[1]), reverse=True)

    chrom = rows[0][0]
    transcript_id = rows[0][3]
    gene_id = rows[0][4]
    strand = rows[0][6]

    for i, row in enumerate(rows):
        start_codon = int(row[1])
        stop_codon = int(row[2])
        score = row[7]
        rank = i + 1
        
        # Calculate exon coordinates
        if rank == 1:
            if len(rows) == 1:
                # Calculate exon coordinates based on the first ranked CDS when there's only one CDS
                exon_start = start_codon - 50
                exon_end = stop_codon + 50  # Exon coordinates for rank 1 with one CDS
            else:
                # Calculate exon coordinates based on the first ranked CDS when there are multiple CDS
                exon_start = start_codon
                exon_end = stop_codon + 50  # Exon coordinates for rank 1 with multiple CDS
        elif rank == len(rows):
            # Calculate exon coordinates for the last ranked CDS
            exon_start = start_codon - 50
            exon_end = stop_codon  # Adjust the end coordinate of the last exon
        else:
            exon_start = start_codon 
            exon_end = stop_codon  # Exon coordinates for other ranks

        
        # 5' UTR row for the first CDS
        if rank == 1:
            utr5_start = stop_codon + 1
            utr5_end = stop_codon + 50
            
            row_utr5 = [chrom, 'EuGene', "5UTR", utr5_start, utr5_end, '.', strand, '.', f'transcript_id {transcript_id}; gene_id {gene_id}']
            output_rows.append(row_utr5)
            
            # start_codon row
            row_start_codon = [chrom, 'EuGene', 'start_codon', stop_codon - 2, stop_codon, '.', strand, '.', f'transcript_id {transcript_id}; gene_id {gene_id}']
            output_rows.append(row_start_codon)

        # exon row
        row_exon = [chrom, 'EuGene', 'exon', exon_start, exon_end, '.', strand, '.', f'transcript_id {transcript_id}; gene_id {gene_id}']
        output_rows.append(row_exon)

        # CDS row
        if rank == 1:
            # For the first ranked CDS, use the stop_codon as the start of CDS
            row_cds = [chrom, 'EuGene', 'CDS', start_codon, stop_codon, '.', strand, score, f'transcript_id {transcript_id}; gene_id {gene_id}']
        elif rank == len(rows):
            # For the last ranked CDS, use the start_codon as the start of CDS
            row_cds = [chrom, 'EuGene', 'CDS', start_codon + 3, stop_codon, '.', strand, score, f'transcript_id {transcript_id}; gene_id {gene_id}']
        else:
            # For other CDS rows, use the regular CDS coordinates
            row_cds = [chrom, 'EuGene', 'CDS', start_codon, stop_codon, '.', strand, score, f'transcript_id {transcript_id}; gene_id {gene_id}']
        
        output_rows.append(row_cds)

    # stop_codon row
    row_stop_codon = [chrom, 'EuGene', 'stop_codon', start_codon, start_codon + 2, '.', strand, '.', f'transcript_id {transcript_id}; gene_id {gene_id}']
    output_rows.append(row_stop_codon)

    # 3' UTR row for the last CDS
    if rank == len(rows):
        utr3_start = start_codon - 50
        utr3_end = start_codon - 1
        row_utr3 = [chrom, 'EuGene', '3UTR', utr3_start, utr3_end, '.', strand, '.', f'transcript_id {transcript_id}; gene_id {gene_id}']
        output_rows.append(row_utr3)

    return output_rows


input_file = 'PATH/TO/DATA/CDS_NEG.gtf'
output_file = 'PATH/TO/DESTINATION/FOLDER/CDS_NEG_rowexpand.gtf'

# Store rows in a dictionary by transcript_id
rows_by_transcript = {}
current_transcript_id = None
current_rows = []

with open(input_file, 'r') as file:
    reader = csv.reader(file, delimiter='\t')
    for row in reader:
        if not row[0].startswith('#'):
            transcript_id = row[3]

            if transcript_id != current_transcript_id:
                if current_transcript_id:
                    rows_by_transcript[current_transcript_id] = current_rows
                current_transcript_id = transcript_id
                current_rows = []

            current_rows.append(row)

    if current_transcript_id:
        rows_by_transcript[current_transcript_id] = current_rows

output_rows_cds = []

for rows in rows_by_transcript.values():
    output_rows_cds.extend(process_row_cds(rows))

with open(output_file, 'w', newline='') as file:
    writer = csv.writer(file, delimiter='\t')
    writer.writerows(output_rows_cds)

print('Output file generated successfully.')
