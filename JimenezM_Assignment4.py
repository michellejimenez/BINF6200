import sys


def split_terms(filename):
    """
    This function opens the file and split the file into individual GO terms.  It returns
    the separated terms as a list; if the file cannot be found, it returns an empty list

    Args:
        filename(str): a file path to a GO terms file

    Returns:
        list of str: a list of GO terms
    """
    try:
        file = open(filename, "r")
    except:
        print('Failed to open GO terms file: ' + filename)
        return []
    terms = []
    current_term = None
    for line in file:
        if current_term is not None:
            if line == "\n":
                terms.append(current_term)
                current_term = None
            else:
                current_term += line
        elif line == "[Term]\n":
            current_term = ""
    return terms


def is_gaf_qualifier(value):
    """
    Returns True if `value` contains possible values in a GAF 'Qualifier' field.
    """
    return value.startswith("NOT") or \
        value.startswith("contributes_to") or \
        value.startswith("colocalizes_with")


def map_protein_to_go(filename):
    """
    Process a GAF file and returns a dictionary containing the mapping relationship between the protein
    ID (DB Object ID) and its list of associating GO terms. Returns an empty dictionary if the file cannot be opened.

    Args:
        filename(str): a file path to a gaf file

    Returns:
        A dictionary where keys are Protein IDs (str) and values are sets containing corresponding
        GO IDs.
    """
    try:
        file = open(filename, "r")
    except:
        print('Failed to open GO annotations file: ' + filename)
        return {}

    mapping = {}
    for line in file:
        if line.startswith('!'):
            continue
        columns = line.strip().split()
        protein_id = columns[1]

        # Column 4 can optionally contain a qualifier, in which case the GO ID is in column 5.
        go_id_index = 4 if is_gaf_qualifier(columns[3]) else 3
        go_id = columns[go_id_index]

        # Initialize the protein ID set in the dictionary if it doesn't exist.
        try:
            go_ids = mapping[protein_id]
        except KeyError:
            mapping[protein_id] = set()
            go_ids = mapping[protein_id]

        go_ids.add(go_id)

    return mapping


def parse_go_term(term):
    """
    Parses ID and is_a fields from the given GO term

    Args:
        term(str): Lines of a single GO term entry, excluding the beginning [Term] line.

    Returns:
       A tuple (str, list(str)), where the first entry is the ID and the second entry is a list containing each GO ID with a is_a relationship.
    """
    id = None
    is_as = []
    lines = term.split('\n')
    for line in lines:
        elements = line.strip().split()
        if not elements:
            continue
        if elements[0] == "id:":
            id = elements[1]
        elif elements[0] == "is_a:":
            is_as.append(elements[1])
    return (id, is_as)


def find_parent_terms(go_id, go_dict):
    """
    Find and return all direct and indirect parents of a given GO ID based on a mapping dictionary.

    Arguments:
        go_id(str): A string containing a single GO ID.
        go_dict(dict): A dictionary where each key is a GO ID and each value is a list of GO IDs that                   represents the key's parents.

    Returns:
        A set containing all direct and indirect parents of `go_id` based on is_a relationships.
    """
    parent_terms = set()
    try:
        direct_parents = go_dict[go_id]
    except KeyError:
        # If there are no parents then return the empty set
        return parent_terms

    for parent_id in direct_parents:
        parent_terms.add(parent_id)
        parent_terms.update(find_parent_terms(parent_id, go_dict))
    return parent_terms


def build_direct_parent_mapping(filename):
    """
    Process a GO term file a mapping between all present GO IDs and their direct parents based on is_a
    relationships.

    Arguments:
        filename(str): The path to a GO terms file.

    Returns:
        A dictionary where each key is a GO ID and each value is a list of GO IDs that                   represents the key's parents.
    """
    go_terms = split_terms(filename)
    go_dict = {}
    for term in go_terms:
        (id, direct_parents) = parse_go_term(term)
        go_dict[id] = direct_parents
    return go_dict


def main(argv):
    try:
        input_terms = sys.argv[1]
        input_annotations = sys.argv[2]
        if len(sys.argv) > 3:
            output_file = open(sys.argv[3] + '.tsv', 'w')
        else:
            output_file = sys.stdout
    except:
        print(
            'Arguments: <input_terms> <input_annotations> [<output_filename>]')
        return

    go_dict = build_direct_parent_mapping(input_terms)
    protein_id_to_go_ids = map_protein_to_go(input_annotations)
    for protein in sorted(protein_id_to_go_ids.keys()):
        go_ids = protein_id_to_go_ids[protein]
        print(protein, end='', file=output_file)
        for go_id in sorted(go_ids):
            parents = sorted(find_parent_terms(go_id, go_dict))

            # NOTE: The provided "expected_output.tsv" file simply skips the GO IDs without
            # printing a new line after the protein ID. I found this formatting strange since it
            # contains two concatenated protein IDs in the first column if no parents are found in the
            # GAF file, so instead I chose to print each direct parent and skip the parents.
            #
            # This can be changed to match the expected output by un-commenting the following snippet:
            # if not parents:
            #   continue
            print('\t' + go_id, end='', file=output_file)
            if not parents:
                print('', file=output_file)
            first_parent = True
            for parent in parents:
                if first_parent:
                    prefix = '\t'
                    first_parent = False
                else:
                    prefix = '\t\t'
                print(prefix + parent, file=output_file)


if __name__ == "__main__":
    main(sys.argv)
