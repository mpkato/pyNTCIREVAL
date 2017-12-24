import click
import csv
import re

LEVEL = re.compile("^L([0-9]+)$")
SEP_LABELLED_RANKED_LIST = ' '
DEFAULT_CUTOFFS = [1000]

def read_grades(string):
    """
    Read grades from string '-g <g1>:<g2>:...'

    Args:
        string: '-g <g1>:<g2>:...'

    Returns:
        A list of grades. The i-th element is a grade for the i-th relevance level.
    """
    result = _read_ints(string, ':', '-g')
    _validate_order(string, result, '-g')
    _validate_positive(string, result, '-g')
    return result

def read_stops(string):
    """
    Read stop values for graded-uniform NCU from string '-s <s1>:<s2>:...'

    Args:
        string: '-s <s1>:<s2>:...'

    Returns:
        A list of stop values. The i-th element is a stop value for the i-th relevance level.
    """
    result = _read_ints(string, ':', '-s')
    _validate_order(string, result, '-s')
    _validate_positive(string, result, '-s')
    return result

def read_cutoffs(string):
    """
    Read a cutoff value from string '--cutoffs <document rank>[,<document rank>]*'

    Args:
        string: '--cutoffs <document rank>[,<document rank>]*'

    Returns:
        A list of cutoff values. Returns DEFAULT_CUTOFFS if not specified.
    """
    if len(string) == 0:
        return DEFAULT_CUTOFFS
    return _read_ints(string, ',', '--cutoffs')

def read_rel_file(f, sep):
    """
    Read the content of a relevance file.
    LINE FORMAT: <document id><SEPARATOR><relevance level>
        where <relevance level> := L[0-9]+

    Args:
        f: file stream
        sep: a string that separates the document ID and relevance level.

    Returns:
        A dict of a document ID and a relevance level (int)
    """
    rows = csv.reader(f, delimiter=sep)
    result = {}
    for idx, row in enumerate(rows):
        if len(row) != 2:
            raise Exception(
                "The rel file contains an invalid line at Line %s" % (idx+1))
        did, level = row
        if did in result:
            raise Exception(
                "The rel file contains different relevance levels for the same document.")
        level = _parse_level(level, idx)
        result[did] = level
    f.close()
    return result

def read_ranked_list(f):
    """
    Read the content of a ranked list file.
    LINE FORMAT: <document id>

    Args:
        f: file stream. If f is None, use stdin.

    Returns:
        A ranked list of document IDs.
    """
    result = []
    if f:
        stream = f
    else:
        import sys
        stream = sys.stdin
    for idx, line in enumerate(stream):
        did = line.strip()
        result.append(did)
    stream.close()
    return result

def read_labelled_ranked_list(f):
    """
    Read the content of a labelled ranked list.
    LINE FORMAT: <document id><SEP_LABELLED_RANKED_LIST><relevance level>
        where <relevance level> := L[0-9]+

    Args:
        f: file stream. If f is None, use stdin.

    Returns:
        A ranked list of tuples of a document ID and a relevance level (int).
    """
    result = []
    if f:
        stream = f
    else:
        import sys
        stream = sys.stdin
    for idx, line in enumerate(stream):
        ls = line.strip().split(SEP_LABELLED_RANKED_LIST)
        if len(ls) == 1:
            ls.append(None)
        if len(ls) > 0:
            did, level = ls[:2]
            if level is not None:
                level = _parse_level(level, idx)
            result.append((did, level))
    stream.close()
    return result

def output_labelled_ranked_list(sysdoclab):
    """
    Output a ranked list of documents with a relevance level.

    Args:
        sysdoclab: a ranked list of tuples of a document ID and a relevance level.
    """
    for did, grade in sysdoclab:
        print(did + (" L" + str(grade) if grade is not None else ""))

def compute_validation(j, grades, stops, beta, gamma, logb, rbp,
    xrelnum, jrelnum):
    '''
    Validate the args for the 'compute' command.

    Args:
        j:
        grades: a list of the gain value for each relevance level.
        stops: a list of the stop value for each relevance level.
        beta: Q-measure's beta.
        gamma: rank-biased NCU's gamma.
        logb: log base for DCG
        rbp: persistence for RBP
        xrelnum: the number of judged X-rel docs (including 0-rel=judged nonrel)
        jrelnum: the total number of judged rel docs
    '''

    if len(stops) != len(grades):
        raise click.BadParameter("the size of '-s' must be the same as '-g'")
    if beta < 0:
        raise click.BadParameter("the value of '--beta' must be positive")
    if gamma < 0 or gamma > 1:
        raise click.BadParameter("the value of '--gamma' must range from 0 to 1")
    if logb < 0:
        raise click.BadParameter(
            "the value of '--logb' must be 0 (natural log) or more")
    if rbp < 0 or rbp > 1:
        raise click.BadParameter("the value of '--rbp' must range from 0 to 1")
    # TODO: bug report
    # THIS EXCEPTION SHOULD NOT BE RAISED
    #if j and xrelnum[0] == 0:
    #    raise Exception("No judged nonrel: bpref etc. not computable")
    if jrelnum == 0:
        raise Exception(
            "No relevance document found in the relevance assessment file")

def _read_ints(string, sep, name):
    '''
    Return a list of int values

    Args:
        string: option value
        sep: separator character
        name: option name

    Returns:
        [i1, i2, ...] for string '-<name> <i1><sep><i2><sep>...'
    '''
    try:
        ints = [int(i) for i in string.split(sep)]
    except:
        raise click.BadParameter(
            "'%s' for option '%s'" % (string, name))
    return ints

def _validate_order(string, values, name):
    '''
    Validate values that must be in ascending order.

    Args:
        string: option value
        values: values to be in ascending order
        name: option name
    '''
    for small, large in zip(values[:-1], values[1:]):
        if small > large:
            raise click.BadParameter(
                "'%s' for option '%s' must be in ascending order" % (string, name))

def _validate_positive(string, values, name):
    '''
    Validate values that must be positive.

    Args:
        string: option value
        values: values to be positive
        name: option name
    '''
    if any([v < 0 for v in values]):
        raise click.BadParameter(
            "'%s' for option '%s' must be positive" % (string, name))

def _parse_level(level, idx):
    '''
    Parse the relevance level string.

    Args:
        level: 'L[0-9]+'.
        idx: line index for exception report.

    Returns:
        a level converted to int.
    '''
    m = LEVEL.match(level)
    if m:
        level = int(m.group(1))
    else:
        raise Exception(
            "An invalid relevance level at Line %s" % (idx+1))
    return level
