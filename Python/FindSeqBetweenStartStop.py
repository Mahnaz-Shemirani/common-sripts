import pandas as pd
import gzip


def find_start_stop_fasta(input_file):
    areas = []
    sequences = []
    with gzip.open(input_file, 'rt') as handle:
        seq_id = None
        seq = ''
        for line in handle:
            line = line.strip()
            if line.startswith('>'):
                if seq_id is not None:
                    # Process the previous sequence record
                    curr_areas, curr_sequences = process_sequence(seq_id, seq)
                    areas.extend(curr_areas)
                    sequences.extend(curr_sequences)
                seq_id = line[1:]
                seq = ''
            else:
                seq += line
        # Process the last sequence record in the file
        curr_areas, curr_sequences = process_sequence(seq_id, seq)
        areas.extend(curr_areas)
        sequences.extend(curr_sequences)
    return areas, sequences                

def process_sequence(seq_id, seq):
    areas = []
    sequences = []
    for start_idx in range(3):
        for i in range(start_idx, len(seq) - 2, 3):
            if seq[i:i+3] == 'ATG':
                for j in range(i+3, len(seq) - 2, 3):
                    codon = seq[j:j+3]
                    if codon in ['TAA', 'TAG', 'TGA']:
                        area = f"{seq_id}:{i+1}-{j+2}"
                        sequence = seq[i:j+3]
                        areas.append(area)
                        sequences.append(sequence)
                        break
    return areas, sequences



#run the function
input_file = 'PATH/GENOME.fasta.gz'
areas, sequences = find_start_stop_fasta(input_file)


df = pd.DataFrame({'Area': areas, 'Sequence': sequences})
df.to_csv('PATH RSULTS/frame123.csv', index=False)
