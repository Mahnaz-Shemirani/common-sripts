import csv

def process_row_cds(rows):
    output_rows = []

    # Sort the rows by start_codon
    rows.sort(key=lambda row: int(row[1]))

    chrom = rows[0][0]
    transcript_id = rows[0][3]
    gene_id = rows[0][4]
    strand = rows[0][6]

    last_stop_codon = None
    row_cds = None  # Initialize row_cds outside of if/else blocks

    for i, row in enumerate(rows):
        start_codon = int(row[1])
        stop_codon = int(row[2])
        score = row[7]
        rank = i + 1
        
        # Calculate exon coordinates
        if rank == 1:
            exon_start = start_codon - 50
        else:
            exon_start = start_codon
        
        if rank == len(rows):
            # For the last exon and CDS in multiple CDS case
            exon_end = stop_codon + 50
            if last_stop_codon is not None:
                last_stop_codon = stop_codon - 3  # Adjust the last CDS stop_codon
        else:
            exon_end = stop_codon

        # 5' UTR row for the first CDS
        if rank == 1:
            utr5_start = start_codon - 50
            utr5_end = start_codon - 1
            
            row_utr5 = [chrom, 'EuGene', "5UTR", utr5_start, utr5_end, '.', strand, '.', f'transcript_id {transcript_id}; gene_id {gene_id}']
            output_rows.append(row_utr5)
            # start_codon row
            row_start_codon = [chrom, 'EuGene', 'start_codon', start_codon, start_codon + 2, '.', strand, '.', f'transcript_id {transcript_id}; gene_id {gene_id}']
            output_rows.append(row_start_codon)

        # exon row
        row_exon = [chrom, 'EuGene', 'exon', exon_start, exon_end, '.', strand, '.', f'transcript_id {transcript_id}; gene_id {gene_id}']
        output_rows.append(row_exon)

        # CDS row
        if rank == len(rows):
            # For the last CDS, stop 3 bases before the regular stop_codon
            if last_stop_codon is not None:
                row_cds = [chrom, 'EuGene', 'CDS', start_codon, last_stop_codon, '.', strand, score, f'transcript_id {transcript_id}; gene_id {gene_id}']
        else:
            # For other CDS rows, use the regular stop_codon
            row_cds = [chrom, 'EuGene', 'CDS', start_codon, stop_codon, '.', strand, score, f'transcript_id {transcript_id}; gene_id {gene_id}']
        if row_cds is not None:
            output_rows.append(row_cds)

        # stop_codon row
        if rank == len(rows) and last_stop_codon is not None:
            row_stop_codon = [chrom, 'EuGene', 'stop_codon', last_stop_codon + 1, last_stop_codon + 3, '.', strand, '.', f'transcript_id {transcript_id}; gene_id {gene_id}']
            output_rows.append(row_stop_codon)

            # 3' UTR row for the last exon
            utr3_start = last_stop_codon + 4
            utr3_end = last_stop_codon + 53
            row_utr3 = [chrom, 'EuGene', '3UTR', utr3_start, utr3_end, '.', strand, '.', f'transcript_id {transcript_id}; gene_id {gene_id}']
            output_rows.append(row_utr3)

        last_stop_codon = stop_codon

    return output_rows

input_file = 'C:/Users/mzir0001/Downloads/reyes/data/Lalbus_CDS_pos_annot_semicolonEliminated.gtf'
output_file = 'C:/Users/mzir0001/Downloads/reyes/data/Lalbus_CDS_pos_annot_rowexpand.gtf'

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
