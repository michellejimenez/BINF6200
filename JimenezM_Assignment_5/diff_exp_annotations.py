import re


def blast_parse(blast_file):
    """
    Parse out the BLAST results file from a tabular format into a dictionary
    Load transcript IDs of query sequence (qseqid) and SwissProt IDs of subject
    sequence (sseqid) without version number to the dictionary.

    Args:
        blast_file (File): File object representing tabular BLAST results file 
    Returns:
        dictionary containing the transcript ID as key and as value a tuple containing the SwissProt ID
    """
    output_dict = {}
    for line in blast_file:
        qseqid, sseqid, pident, length, mismatch, gapopen, qstart, qend, sstart, send, evalue, bitscore = line.rstrip().split("\t")
        transcript, isoform = qseqid.split("|")
        gi_type, gi, sp_type, sp, sp_name = sseqid.split("|")
        sp_id, sp_version = sp.split(".")
        if transcript not in output_dict and float(pident) > 99:
            output_dict[transcript] = sp_id
    return output_dict


def process_gaf(gene_to_go_file):
    """
    Process a GAF file and returns a dictionary containing the mapping relationship between the gene
    ID (object_id) and its GO ID (go_id)

    Args:
        gene_to_go_file (File): File object representing GAF file
    Returns:
        dictionary containing object_id (keys) and a list of go_id (values)
    """
    gene_to_go = {}
    # Load protein IDs and corresponding GO terms to the dictionary.
    for line in gene_to_go_file:
        db, object_id, object_symbol, qualifier, go_id, * \
            others = line.split("\t")

        # Check if both protein and GO IDs have a value before adding.
        if object_id and go_id:
            go_ids = gene_to_go.get(object_id, set())
            go_ids.add(go_id)
            gene_to_go[object_id] = go_ids

    return gene_to_go


def process_go_terms(go_terms):
    """

    Args:
        go_terms (String): The unprocessed contents of a OBO file.

    Returns:
        dictionary containing go ID (keys) and go name (value)
    """
    go_to_desc = {}

    # Load GO IDs and their names to the dictionary.
    terms = re.findall(r"\[Term]\n(.*?)\n\n", go_terms, re.DOTALL)

    for term in terms:
        go_id = re.search(r"^id:\s+(GO:\d+?)\n", term)
        go_name = re.search(r"^name:\s+(.+?)\n", term, re.M)

        # Check if both ID and name have a value before adding.
        if go_id and go_name:
            go_to_desc[go_id.group(1)] = go_name.group(1)

    return go_to_desc


def create_report(diff_exp_file, output_report_file, transcript_to_protein, gene_to_go, go_to_desc):
    """
    Create a report in TSV format for each entry in the given differential expression file by annotating them with the
    corresponding protein ID, GO ID, and GO descriptions if they exist. The results are written to the File given in output_report_file.

    Args:
        diff_exp_file (File): File object representing a differential expression file
        output_report_file (File): File object representing the output file that the report will be written to
        transcript_to_protein (dictionary): Mapping from transcript to protein ID
        gene_to_go (dictionary): Mapping from protein ID to a list of matching GO terms
        go_to_desc (dictionary): Mapping from GO term to GO description
    """
    # Loop through differential expression file; lookup the protein ID and
    # GO term + GO name; print results to REPORT output.
    diff_exp_file.readline()  # skip header
    for line in diff_exp_file:
        transcript, sp_ds, sp_hs, sp_log, sp_plat = line.rstrip().split("\t")

        protein = transcript_to_protein.get(transcript, "NA")
        go_ids = gene_to_go.get(protein, None)

        if go_ids is None:
            output_report_file.write("\t".join(
                [transcript, protein, sp_ds, sp_hs, sp_log, sp_plat, "NA", "NA"]) + "\n")
        else:
            first_line = True
            for go_id in sorted(go_ids):
                go_desc = go_to_desc.get(go_id, "NA")
                if first_line:
                    output_report_file.write("\t".join(
                        [transcript, protein, sp_ds, sp_hs, sp_log, sp_plat, go_id, go_desc]) + "\n")
                    first_line = False
                else:
                    output_report_file.write(
                        "\t".join(['', '', '', '', '', '', go_id, go_desc]) + "\n")


def main():
    blast_filename = "blastp.outfmt6"
    gene_to_go_filename = "gene_association_subset.gaf"
    go_terms_filename = "go-basic.obo"
    diff_exp_filename = "diffExpr.P1e-3_C2.matrix"
    output_filename = "report.tsv"

    # open all the files
    try:
        blast_file = open(blast_filename, "r")
        gene_to_go_file = open(gene_to_go_filename, "r")
        go_terms_file = open(go_terms_filename, "r")
        diff_exp_file = open(diff_exp_filename, "r")
    except Exception as e:
        print('Failed to open input file: ' + str(e))

    with open(output_filename, "w") as output_file:
        transcript_to_protein = blast_parse(blast_file)
        gene_to_go = process_gaf(gene_to_go_file)
        go_to_desc = process_go_terms(go_terms_file.read())

        create_report(diff_exp_file, output_file,
                      transcript_to_protein, gene_to_go, go_to_desc)


if __name__ == '__main__':
    main()
