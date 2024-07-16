import io

import pytest

from genetic_forensic_portal.app.utils import validate_input_file

LEGAL_HEADER = "MatchID\t" + "\t".join(validate_input_file.MSAT_NAMES)
LEGAL_LINE = (
    "sample1\t"
    + "\t".join(["1"] * (len(validate_input_file.MSAT_NAMES) - 1))
    + "\t-999"
)


def test_legal_file_throw_no_errors():
    file_data = LEGAL_HEADER + "\n" + LEGAL_LINE + "\n" + LEGAL_LINE + "\n"
    testfile = io.StringIO(file_data)

    validate_input_file.validate_input_file(testfile)


def test_illegal_header_throw_error():
    file_data = "notMatchId\t" + "\t".join(validate_input_file.MSAT_NAMES)
    testfile = io.StringIO(file_data)

    expected_error = validate_input_file.ERROR_TEMPLATE.format(
        lineno=1, error=validate_input_file.HEADER_MUST_START_WITH_MATCHID
    )

    with pytest.raises(ValueError, match=expected_error):
        validate_input_file.validate_input_file(testfile)


def test_incorrect_number_of_msats_in_header_throws():
    file_data = "MatchID\t" + "\t".join(validate_input_file.MSAT_NAMES[:-1])
    testfile = io.StringIO(file_data)

    expected_error = validate_input_file.ERROR_TEMPLATE.format(
        lineno=1,
        error=validate_input_file.INCORRECT_NUM_MSATS_IN_HEADER.format(
            num_msats_found=len(validate_input_file.MSAT_NAMES) - 1
        ),
    )

    with pytest.raises(ValueError, match=expected_error):
        validate_input_file.validate_input_file(testfile)


def test_incorrect_msat_names_in_header_throws():
    file_data = "MatchID\t" + "\t".join(
        ["incorrect" + msat for msat in validate_input_file.MSAT_NAMES]
    )
    testfile = io.StringIO(file_data)

    expected_error = validate_input_file.ERROR_TEMPLATE.format(
        lineno=1, error=validate_input_file.INCORRECT_MSAT_NAMES
    )

    with pytest.raises(ValueError, match=expected_error):
        validate_input_file.validate_input_file(testfile)


def test_incorrect_number_of_msats_in_line_throws():
    illegal_line = "sample1\t" + "\t".join(
        ["1"] * (len(validate_input_file.MSAT_NAMES) - 1)
    )
    file_data = LEGAL_HEADER + "\n" + illegal_line
    testfile = io.StringIO(file_data)

    expected_error = validate_input_file.ERROR_TEMPLATE.format(
        lineno=2,
        error=validate_input_file.INCORRECT_NUM_MSATS.format(
            num_msats_found=len(validate_input_file.MSAT_NAMES) - 1
        ),
    )

    with pytest.raises(ValueError, match=expected_error):
        validate_input_file.validate_input_file(testfile)


def test_illegal_msat_value_throws():
    illegal_line = "sample1\t" + "\t".join(
        ["-100"] * len(validate_input_file.MSAT_NAMES)
    )
    file_data = LEGAL_HEADER + "\n" + illegal_line
    testfile = io.StringIO(file_data)

    expected_error = validate_input_file.ERROR_TEMPLATE.format(
        lineno=2, error=validate_input_file.ILLEGAL_MSAT_VALUE.format(msat_value="-100")
    )

    with pytest.raises(ValueError, match=expected_error):
        validate_input_file.validate_input_file(testfile)


def test_nonnumeric_msat_value_throws():
    illegal_line = "sample1\t" + "\t".join(["A"] * len(validate_input_file.MSAT_NAMES))
    file_data = LEGAL_HEADER + "\n" + illegal_line
    testfile = io.StringIO(file_data)

    expected_error = validate_input_file.ERROR_TEMPLATE.format(
        lineno=2, error=validate_input_file.ILLEGAL_MSAT_VALUE.format(msat_value="A")
    )

    with pytest.raises(ValueError, match=expected_error):
        validate_input_file.validate_input_file(testfile)


def test_only_1_haplotype_for_sid_throws():
    file_data = LEGAL_HEADER + "\n" + LEGAL_LINE
    testfile = io.StringIO(file_data)
    expected_error = validate_input_file.ERROR_TEMPLATE.format(
        lineno=2,
        error=validate_input_file.ONLY_ONE_HAPLOTYPE_FOR_SID.format(
            sid="sample1", count=1
        ),
    )

    with pytest.raises(ValueError, match=expected_error):
        validate_input_file.validate_input_file(testfile)


def test_more_than_2_haplotypes_for_sid_throws():
    file_data = LEGAL_HEADER + "\n" + LEGAL_LINE + "\n" + LEGAL_LINE + "\n" + LEGAL_LINE
    testfile = io.StringIO(file_data)
    expected_error = validate_input_file.ERROR_TEMPLATE.format(
        lineno="2,3,4",
        error=validate_input_file.TOO_MANY_HAPLOTYPES_FOR_SID.format(
            sid="sample1", count=3
        ),
    )

    with pytest.raises(ValueError, match=expected_error):
        validate_input_file.validate_input_file(testfile)
