from diff_exp_annotations import blast_parse, process_gaf, process_go_terms

# Tests for blast_parse


def test_blast_parse_empty_input():
    output = blast_parse([])
    assert(output == {})


def test_blast_parse_one_entry():
    output = blast_parse(
        ["c0_g1_i1|m.1	gi|74665200|sp|Q9HGP0.1|PVG4_SCHPO	100.00	372	0	0	1	372	1	372	0.0	  754"])
    assert(output == {"c0_g1_i1": "Q9HGP0"})


def test_blast_parse_exclude_pident_at_or_below_99():
    output = blast_parse(
        ["c0_g1_i1|m.1	gi|74665200|sp|Q9HGP0.1|PVG4_SCHPO	99.00	372	0	0	1	372	1	372	0.0	  754"])
    assert(output == {})


def test_blast_parse_pick_first_entry_above_99():
    output = blast_parse(
        ["c0_g1_i1|m.1	gi|74665200|sp|TEST_PROTEIN1.1|PVG4_SCHPO	99.00	372	0	0	1	372	1	372	0.0	  754",
         "c0_g1_i1|m.1	gi|74665200|sp|TEST_PROTEIN2.1|PVG4_SCHPO	100.00	372	0	0	1	372	1	372	0.0	  754",
         "c0_g1_i1|m.1	gi|74665200|sp|TEST_PROTEIN3.1|PVG4_SCHPO	100.00	372	0	0	1	372	1	372	0.0	  754"])
    assert(output == {"c0_g1_i1": "TEST_PROTEIN2"})


# Tests for process_gaf


def test_process_gaf_object_id_missing():
    output = process_gaf(
        ["UniProtKB		SPBC460.03		GO:1234	PMID:20944394	"])
    assert(output == {})


def test_process_gaf_go_id_missing():
    output = process_gaf(
        ["UniProtKB	TEST_PROTEIN	SPBC460.03			PMID:20944394	"])
    assert(output == {})


def test_process_gaf_one_entry():
    output = process_gaf(
        ["UniProtKB	TEST_PROTEIN	SPBC460.03		GO:1234	PMID:20944394	"])
    assert(output == {"TEST_PROTEIN": {"GO:1234"}})


def test_process_gaf_duplicate_go_ids():
    output = process_gaf(
        ["UniProtKB	TEST_PROTEIN	SPBC460.03		GO:1234	PMID:20944394	",
         "UniProtKB	TEST_PROTEIN	SPBC460.03		GO:1234	PMID:20944394	"])
    assert(output == {"TEST_PROTEIN": {"GO:1234"}})


def test_process_gaf_multiple_go_ids():
    output = process_gaf(
        ["UniProtKB	TEST_PROTEIN	SPBC460.03		GO:1234	PMID:20944394	",
         "UniProtKB	TEST_PROTEIN	SPBC460.03		GO:4567	PMID:20944394	"])
    assert(output == {"TEST_PROTEIN": {"GO:1234", "GO:4567"}})


def test_process_gaf_multiple_proteins():
    output = process_gaf(
        ["UniProtKB	TEST_PROTEIN1	SPBC460.03		GO:1234	PMID:20944394	",
         "UniProtKB	TEST_PROTEIN1	SPBC460.03		GO:4567	PMID:20944394	",
         "UniProtKB	TEST_PROTEIN2	SPBC460.03		GO:9876	PMID:20944394	",
         "UniProtKB	TEST_PROTEIN3	SPBC460.03		GO:1234	PMID:20944394	"])
    assert(output == {"TEST_PROTEIN1": {"GO:1234", "GO:4567"},
                      "TEST_PROTEIN2": {"GO:9876"},
                      "TEST_PROTEIN3": {"GO:1234"}})

# Tests for process_go_terms


def test_process_go_terms_empty_input():
    output = process_go_terms("")
    assert(output == {})


def test_process_go_terms_no_id_or_name():
    input = "[Term]\n"
    output = process_go_terms(input)
    assert(output == {})


def test_process_go_terms_no_id():
    input = """
[Term]
name: test name
namespace: biological_process
"""
    output = process_go_terms(input)
    assert(output == {})


def test_process_go_terms_no_name():
    input = """
[Term]
id: GO:1234
namespace: biological_process
"""
    output = process_go_terms(input)
    assert(output == {})


def test_process_go_terms_basic_entry_with_id_and_name():
    input = """
[Term]
id: GO:1234
name: test name
namespace: biological_process

"""
    output = process_go_terms(input)
    assert(output == {"GO:1234": "test name"})


def test_process_go_terms_multiple():
    input = """
[Term]
id: GO:12345
name: mitochondrion inheritance
namespace: biological_process
def: Test Definition
synonym: "mitochondrial inheritance" EXACT []
is_a: GO:0048308 ! organelle inheritance
is_a: GO:0048311 ! mitochondrion distribution

[Term]
id: GO:67890
name: some test name
namespace: biological_process
def: Test Definition
synonym: "mitochondrial inheritance" EXACT []
is_a: GO:0048308 ! organelle inheritance
is_a: GO:0048311 ! mitochondrion distribution

[Term]
id: GO:54321
name: some other thing
namespace: biological_process
def: Test Definition
synonym: "mitochondrial inheritance" EXACT []
is_a: GO:0048308 ! organelle inheritance
is_a: GO:0048311 ! mitochondrion distribution

"""
    output = process_go_terms(input)
    assert(output == {"GO:12345": "mitochondrion inheritance",
                      "GO:67890": "some test name",
                      "GO:54321": "some other thing"})
