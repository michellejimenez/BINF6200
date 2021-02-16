#!/usr/bin/env python3
# assignment6_annotation.py

from matrix import Matrix
from blast import Blast


def tuple_to_string(transcript_info):
    """Accept a tuple and retrun it as a tab-separated string
    Arg:
        diff_exp_tuple(tuple): A differntial expression tuple
    Return:
        str: A tab separated string
    """

    return "\t".join(transcript_info.data_attributes())


def main():
    # Openfiles and create their objects
    blast_filename = "blastp.outfmt6"
    diff_exp_filename = "diffExpr.P1e-3_C2.matrix"
    blast = Blast(blast_filename)
    matrix = Matrix(diff_exp_filename)

    # Load transcript_id and sp_id within the good BlastHit into dict
    blast_dict = {blast.transcript_id: blast.sp_id
                  for blast in blast.blast_hit_list if blast.hit_good_match()}

    # Look-up and output file
    with open("output.txt", "w") as output:
        for info in matrix.expressions:
            matrix_info = blast_dict.get(info.transcript, info.transcript) \
                + "\t" + tuple_to_string(info)
            output.write(matrix_info + "\n")


if __name__ == "__main__":
    main()
