import gzip


def reverse_complement(seq):
    complement = {'A': 'T', 'C': 'G', 'G': 'C', 'T': 'A'}
    return ''.join(complement.get(base, base) for base in reversed(seq))

input_file_path = 'PATH/GENOME.fasta.gz'
output_file_path = 'PATH/GENOME_reverse_complement.fasta.gz'

with gzip.open(input_file_path, 'rt') as input_file, gzip.open(output_file_path, 'wt') as output_file:
    seq_name = ''
    seq_data = ''
    for line in input_file:
        if line.startswith('>'):
            if seq_name != '':
                output_file.write(seq_name + '\n')
                output_file.write(reverse_complement(seq_data) + '\n')
            seq_name = line.strip()
            seq_data = ''
        else:
            seq_data += line.strip()
    output_file.write(seq_name + '\n')
    output_file.write(reverse_complement(seq_data) + '\n')
