"""Contains utility functions for validating that user-uploaded TSV files are in the correct format that can be processed.

This file originally from Mary (mkkuhner) @ UW's Center for Environmental Forensic Science"""

# This file originally from Mary (mkkuhner) @ UW's Center for Environmental Forensic Science

import io
import logging

# Check an input microsatellite file for legality

MSAT_NAMES = [
    "FH67",
    "FH71",
    "FH19",
    "FH129",
    "FH60",
    "FH127",
    "FH126",
    "FH153",
    "FH94",
    "FH48",
    "FH40",
    "FH39",
    "FH103",
    "FH102",
    "S03",
    "S04",
]
MSATS = len(MSAT_NAMES)

# Error constants:
ERROR_TEMPLATE = "Error in uploaded file line {lineno}:  {error}"
HEADER_MUST_START_WITH_MATCHID = "First entry in header must be MatchID"
INCORRECT_NUM_MSATS_IN_HEADER = (
    "Number of msat entries in header was {num_msats_found} but should be " + str(MSATS)
)
INCORRECT_MSAT_NAMES = "List of microsats in header is incorrect"
INCORRECT_NUM_MSATS = "Found {num_msats_found} microsats but expected " + str(MSATS)
ILLEGAL_MSAT_VALUE = "Illegal msat value {msat_value}"
ONLY_ONE_HAPLOTYPE_FOR_SID = "{sid} has {count} haplotype but should have 2"
TOO_MANY_HAPLOTYPES_FOR_SID = "{sid} has {count} haplotypes but should have 2"

logger = logging.getLogger(__name__)

# functions


def report_error(lineno: str | int, error: str) -> None:
    """Raise an error with a line number and error message."""
    raise ValueError(ERROR_TEMPLATE.format(lineno=lineno, error=error))


def legal_msat_value(msat: str | int) -> bool:
    """Converts an expected microsatellite value from a string to an int and check if said int is within the expected range (or -999).

    Args:
        msat (str | int): The microsatellite value to check.
    """
    try:
        msat = int(msat)
    except ValueError:
        return False
    if msat == -999:
        return True
    return 0 < msat <= 300


def validate_input_file(infile: io.StringIO) -> None:
    """Check that the input file is legal.

    That is to say, check the following:
    - The header starts with "MatchID"
    - The header contains the correct number of microsatellites
    - The header contains the correct microsatellites
    - Each line contains the correct number of microsatellites
    - Each microsatellite value is legal
    - Each SID (sample ID) is present exactly twice

    Args:
        infile (io.StringIO): The input file to check.
    """
    # read input file
    headerline = infile.readline()
    datalines = infile.readlines()

    # check header legality:
    lineno = 1
    header = headerline.rstrip().split("\t")

    if header[0] != "MatchID":
        errormsg = HEADER_MUST_START_WITH_MATCHID
        report_error(lineno, errormsg)

    msatnames = header[1:]
    num_msats = len(msatnames)
    if num_msats != MSATS:
        errormsg = INCORRECT_NUM_MSATS_IN_HEADER.format(num_msats_found=num_msats)
        report_error(lineno, errormsg)
    if msatnames != MSAT_NAMES:
        errormsg = INCORRECT_MSAT_NAMES
        report_error(lineno, errormsg)

    # check entry legality:
    sidlines: dict[str, list[int]] = {}
    for dataline in datalines:
        lineno += 1
        line = dataline.rstrip().split("\t")
        sid = line[0]
        if sid not in sidlines:
            sidlines[sid] = []
        sidlines[sid].append(lineno)
        msats = line[1:]
        if len(msats) != MSATS:
            errormsg = INCORRECT_NUM_MSATS.format(num_msats_found=len(msats))
            report_error(lineno, errormsg)

        for msat in msats:
            if not legal_msat_value(msat):
                errormsg = ILLEGAL_MSAT_VALUE.format(msat_value=msat)
                report_error(lineno, errormsg)

    # check that each SID present exactly twice
    for sid, lines in sidlines.items():
        count = len(lines)
        if count != 2:
            all_lines = [str(x) for x in lines]
            reporting_lines = ",".join(all_lines)
            if count == 1:
                errormsg = ONLY_ONE_HAPLOTYPE_FOR_SID.format(sid=sid, count=count)
            else:
                errormsg = TOO_MANY_HAPLOTYPES_FOR_SID.format(sid=sid, count=count)
            report_error(reporting_lines, errormsg)

    logger.info("No errors detected")
