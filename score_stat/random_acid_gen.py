#!/bin/usr python3
import argparse
from random import choices

class AcidGenerator:

    def __init__(self, length):
        self.length = length
        self.acid_dist = {"A": 0.095070,
                          "C": 0.011560,
                          "D": 0.051634,
                          "E": 0.039081,
                          "F": 0.039081,
                          "G": 0.073548,
                          "H": 0.022629,
                          "I": 0.060123,
                          "K": 0.043981,
                          "L": 0.106769,
                          "M": 0.028008,
                          "N": 0.039309,
                          "P": 0.044342,
                          "Q": 0.044409,
                          "R": 0.055342,
                          "S": 0.058097,
                          "T": 0.053810,
                          "V": 0.070647,
                          "W": 0.015378,
                          "Y": 0.028498}

    def generate_acid(self, weights=None):
        """
        requires dictionary of amino acid distribution {"acid": probability}
        returns list in specified size of randomly selected acids
        """
        if not weights:
            random_seq = choices(list(self.acid_dist.keys()),
                                 weights=list(self.acid_dist.values()),
                                 k=self.length)
        else:
            random_seq = choices(list(self.acid_dist.keys()),
                                 k=self.length)
        # convert list of letters into proper string
        return "".join(random_seq)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Generate Acid from distribution ")
    parser.add_argument("-l", "--length", type=int, help="length of generated sequence")
    parser.add_argument("-o", "--output", type=str, default="generated_db", help="path of output file")
    parser.add_argument("-b", "--batch", type=int, help="mark if acid should be generated in batches")
    parser.add_argument("-w", "--weights", type=bool, default=False, help="set flag to supress underlying probability distribution")
    args = parser.parse_args()
    # default value
    db_size = 1335035
    acid_gen = AcidGenerator(db_size) if not args.length else AcidGenerator(args.length)

    if args.batch:
        total_seq = []
        for _id in range(args.batch):
            line_indent = "\n>{id}ACID\n".format(id=_id)
            total_seq.append(line_indent)
            total_seq.append(acid_gen.generate_acid(weights=args.weights))
        generated_sequence = ''.join(total_seq)
    if not args.batch:
        generated_sequence = acid_gen.generate_acid(weights=args.weights)
        
    with open(args.output, "w") as out_file:
        out_file.write(generated_sequence)    
