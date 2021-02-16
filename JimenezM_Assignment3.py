import re
import sys
import textwrap


def get_header(record):
    """
    This function parses for the VERSION and DEFINITION values within the genbank record and
    stitches them together to form a FASTA header. Once converted, it returns the header

    Args:
        record(str): a genbank record

    Returns:
        header(str): FASTA header in a single line, starts with ">"
    """
    lines = record.splitlines()
    version = None
    definition = None
    for line in lines:
        line_parts = line.split(' ', 1)
        if len(line_parts) == 2:
            if line_parts[0] == 'VERSION':
                version = line_parts[1].strip()
            elif line_parts[0] == 'DEFINITION':
                # Remove all trailing punctuation
                definition = line_parts[1].strip().rstrip(
                    '!"#$%&\'()*+,-./:;<=>?@[\\]^_`{|}~')

        # if we have found both version and definition then no need to process the rest of the record
        if version is not None and definition is not None:
            break

    return '>%s %s' % (version, definition)


def get_sequence(record):
    """
    Function that parses for the ORIGIN value within the record and
    converts the sequence into a FASTA-formatted sequence. Returns the sequence.

    When the function is called the ORIGIN line should have been just read. It reads the
    sequence lines until the "//" at the end.

    Args:
        record(str): a genbank file

    Returns:
        sequence(str): Fasta-formatted sequence
    """
    sequence = ''
    origin_began = False
    lines = record.splitlines()
    for line in lines:
        line = line.strip()
        if line == '//':
            break
        elif origin_began:
            line_parts = line.split(' ', 1)
            sequence += line_parts[1].replace(' ', '').upper()
        elif line == 'ORIGIN':
            origin_began = True
    return '\n'.join(textwrap.wrap(sequence, 70))


def split_records(filename):
    """
    Function that opens the GenBank file and reads it and splits it into individual GenBank entries. 
    '//' marks the end of each entry. Returns the separated entries as a list. If the file cannot be found, 
    it returns an empty list

    Args:
        filename(str): a file path to the input GenBank file

    Returns:
        data(list): the separated Genbank entries in a list format. 
        Multiple lines (list of lines), spanning an entire entry (including the final "//")

    The function should return the separated entries as a list.  If the file cannot be found, return an empty list.
    """
    try:
        record_file = open(filename, 'r')
    except:
        print('File not found: "%s"' % filename)
        return []

    entries = []
    current_entry = ''
    for line in record_file:
        current_entry += line
        if line == '//\n':
            entries.append(current_entry)
            current_entry = ''

    return entries


def main(argv):
    try:
        input_filename = sys.argv[1]
        output_filename = sys.argv[2]
    except:
        print('Required arguments: <input_file> <output_file>')
        return

    records = split_records(input_filename)
    with open(output_filename, 'w') as output_file:
        for record in records:
            output_file.write(get_header(record))
            output_file.write('\n')
            output_file.write(get_sequence(record))
            output_file.write('\n\n')


if __name__ == '__main__':
    main(sys.argv)
