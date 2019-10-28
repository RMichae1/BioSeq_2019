from fuzzywuzzy import process

miRNA_FILENAME="miRNA160.txt"
RNA_FILENAME="ARF10_seq.txt"

pairing = {"U":"A", "A":"U", "G":"C", "C":"G"}


def read_sequence(filename):
    """
    reads input sequence as string from provided filename
    :return string of input sequence:
    """
    with open(filename, 'r') as infile:
        rna_str = "".join(infile.read().splitlines())
    return rna_str


def invert_seq(seq):
    inv_list = [pairing.get(base) for base in list(seq)[:-1]]
    return "".join(inv_list)


def explode_seq(seq, length=16):
    """
    create subsequences from sequence of a given length
    :return list of sequences:
    """
    seq_list = []
    for ix, _ in enumerate(list(seq)):
        partial_seq = seq[ix:ix+length]
        seq_list.append(partial_seq)
    # discard the last sequences as they are no potential binding sites
    return seq_list[:-12]


def fuzzy_matching(template, sequence_list):
    """
    find the complementary sequence through fuzzy matching 
    :return list of matched sequences: with the shortest distances
    """
    seq_matches = process.extract(template, sequence_list)
    # extract string from returned tuple (string, distance)
    seqs = [s[0] for s in seq_matches]
    positions = [sequence_list.index(match) for match in seqs]
    return seq_matches, positions


def pretty_print(seq_list, pos_list):
    for seq, pos in zip(seq_list, seq_pos):
        print("{seq} --- at position --- {position} --- has {percent}% match".format(seq=seq[0], position=pos, percent=seq[1]))
    


if __name__ == "__main__":
    mirna_seq = read_sequence(miRNA_FILENAME)
    # miRNA is the reverse complement 3'-5'
    mirna_complement_seq = invert_seq(mirna_seq)[::-1]

    # binding between 2nd and 16th position:
    short_mirna_complement_seq = mirna_complement_seq[1:16]

    print("Complete miRNA160 complement:")
    print(mirna_complement_seq)
    print("miRNA160 pos.2-16 complement:")
    print(short_mirna_complement_seq)
    
    rna_seq = read_sequence(RNA_FILENAME)
    # explode the RNA into possible matches of comparable length
    rna_list = explode_seq(rna_seq, 15)
    long_rna_list = explode_seq(rna_seq, 21)

    # now that we have a binding string calculate Levenstein distance between RNA-Sequences and miRNA-complement
    seq_list, seq_pos = fuzzy_matching(mirna_complement_seq, long_rna_list)
    short_seq_list, short_seq_pos = fuzzy_matching(short_mirna_complement_seq, rna_list)

    print("For a complete match there are: ")
    pretty_print(seq_list, seq_pos)
    print("For a pos. 2-16 match there are: ")
    pretty_print(short_seq_list, short_seq_pos)
