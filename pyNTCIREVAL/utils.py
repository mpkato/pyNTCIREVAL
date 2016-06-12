import click
import csv
import re

GRADE = re.compile("^L([0-9]+)$")
SEP_LABELLED_RANKED_LIST = ' '
DEFAULT_CUTOFFS = [1000]

def read_grades(string):
    result = _read_ints(string, ':', '-g')
    _validate_order(string, result, '-g')
    _validate_positive(string, result, '-g')
    return result

def read_stops(string):
    result = _read_ints(string, ':', '-s')
    _validate_order(string, result, '-s')
    _validate_positive(string, result, '-s')
    return result

def read_cutoffs(string):
    if len(string) == 0:
        return DEFAULT_CUTOFFS
    return _read_ints(string, ',', '--cutoffs')

def read_rel_file(f, sep):
    rows = csv.reader(f, delimiter=sep)
    result = {}
    for idx, row in enumerate(rows):
        if len(row) != 2:
            raise Exception(
                "The rel file contains an invalid line at Line %s" % (idx+1))
        did, grade = row
        if did in result:
            raise Exception(
                "The rel file contains different grades for the same document.")
        grade = _parse_grade(grade, idx)
        result[did] = grade
    f.close()
    return result

def read_labelled_ranked_list(f):
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
            did, grade = ls[:2]
            if grade is not None:
                grade = _parse_grade(grade, idx)
            result.append([did, grade] + ls[2:])
    stream.close()
    return result

def count_judged(maxrel, qrels):
    '''
    Read relevance assessments and return
    - the number of judged X-rel docs (including 0-rel=judged nonrel)
    - the total number of judged rel docs
    '''
    xrelnum = [0] * (maxrel+1)
    for grade in qrels.values():
        xrelnum[grade] += 1
    jrelnum = sum(xrelnum[1:])
    return xrelnum, jrelnum

def output_labelled_ranked_list(j, truncate, qrels, sysdoclab):
    syslen = 0
    for idx, didgrade in enumerate(sysdoclab):
        if len(didgrade) != 2:
            raise Exception("Invalid line format at Line %s" % (idx+1))
        did, grade = didgrade
        if grade is not None:
            raise Exception("Already labelled at Line %s" % (idx+1))
        grade = qrels.get(did, None)
        if j and grade is None:
            pass # do not output documents without rel judge
        else:
            print(did + (" L" + str(grade) if grade is not None else ""))
            syslen += 1
        if truncate is not None and syslen >= truncate:
            break

def compute_validation(j, grades, stops, beta, gamma, logb, rbp,
    xrelnum, jrelnum):
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

    string: option value
    sep: separator character
    name: option name
    '''
    try:
        ints = [int(i) for i in string.split(sep)]
    except:
        raise click.BadParameter(
            "'%s' for option '%s'" % (string, name))
    return ints

def _validate_order(string, values, name):
    '''
    Validate values that must be in ascending order

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
    Validate values that must be positive

    string: option value
    values: values to be positive
    name: option name
    '''
    if any([v < 0 for v in values]):
        raise click.BadParameter(
            "'%s' for option '%s' must be positive" % (string, name))

def _parse_grade(grade, idx):
    m = GRADE.match(grade)
    if m:
        grade = int(m.group(1))
    else:
        raise Exception(
            "An invalid grade at Line %s" % (idx+1))
    return grade
