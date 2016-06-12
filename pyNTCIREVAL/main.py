import click
import numpy as np
from logging import getLogger, StreamHandler, DEBUG, INFO
logger = getLogger(__name__)
handler = StreamHandler()
handler.setLevel(INFO)
logger.setLevel(INFO)
logger.addHandler(handler)
from .utils import (read_grades, read_stops, read_cutoffs, read_rel_file,
    count_judged, read_labelled_ranked_list,
    output_labelled_ranked_list,
    compute_validation)
from .metrics import nDCG, MSnDCG

@click.group(context_settings={"help_option_names": ['-h', '--help']})
def cli():
    pass

@cli.command()
@click.argument('labelled_ranked_list', required=False,
    type=click.File('r'), metavar='[labelled ranked list]')
@click.option('-r', type=click.File('r'), metavar='<relfile>', required=True,
    help='''A rel (relevance assessments) file''')
@click.option('-j', is_flag=True, default=False,
    help='''Treat the input as a condensed list (unjudged docs removed), '''\
    + '''and compute condensed-list metrics including bpref.''')
@click.option('--ec', is_flag=True, default=False,
    help='''Equivalence class mode''')
@click.option('--sep', default=' ', metavar='<separator>',
    help='''Input/output field separator (default: ' ').''')
@click.option('--truncate', metavar='<rank>',
    help='''Truncate a ranked list at <rank> if specified.''')
def label(labelled_ranked_list, r, j, ec, sep, truncate):
    # parsing parameters
    try:
        truncate = int(truncate) if truncate is not None else None
        if truncate is not None:
            assert truncate > 0
    except (ValueError, AssertionError):
        raise ValueError(
            "'%s' is an invalid option value for 'truncate'" % truncate)

    # processing the rel file
    qrels = read_rel_file(r, sep)
    # TODO: count_ec_judged
    if ec:
        raise Exception("EC has not been implemented yet")

    # processing labelled ranked list
    sysdoclab = read_labelled_ranked_list(labelled_ranked_list)

    output_labelled_ranked_list(j, truncate, qrels, sysdoclab)

@cli.command()
@click.argument('labelled_ranked_list', required=False,
    type=click.File('r'), metavar='[labelled ranked list]')
@click.option('-r', type=click.File('r'), metavar='<relfile>', required=True,
    help='''A rel (relevance assessments) file''')
@click.option('-g', metavar='<gainL1:gainL2...>', required=True,
    help='''How many relevance levels there are (excluding L0) '''\
    + '''and the gain value for each relevance level.''')
@click.option('--verbose', '-v', is_flag=True, default=False,
    help='Verbose output.')
@click.option('-j', is_flag=True, default=False,
    help='''Treat the input as a condensed list (unjudged docs removed), '''\
    + '''and compute condensed-list metrics including bpref.''')
@click.option('--ec', is_flag=True, default=False,
    help='''Equivalence class mode''')
@click.option('--gap', is_flag=True, default=False,
    help='''Compute Robertson/Kanoulas/Yilmaz GAP.''')
@click.option('--sep', default=' ', metavar='<separator>',
    help='''Input/output field separator (default: ' ').''')
@click.option('--out', default='', metavar='<string>',
    help='''Prefix string for each output line. '''\
    + '''Including a topicID here would be useful.''')
@click.option('--beta', default=1.0, metavar=' <positive value>',
    help='''Q-measure's beta (default: 1.00).''')
@click.option('--gamma', default=0.95, metavar='<positive value <=1 >',
    help='''Gamma for rank-biased NCU (default: 0.95).''')
@click.option('--logb', default=2.0, metavar='<value >=0 >',
    help='''Log base for DCG (default: 2.00). '''\
	+ '''If you want natural log, set this value to zero.''')
@click.option('--rbp', default=0.95, metavar='<positive value <=1 >',
    help='''Persistence for RBP (default: 0.95).''')
@click.option('--cutoffs', default='',
    metavar='<document rank[,document rank,...]>',
    help='''Cutoffs for P@n, Hit@n, nDCG@n... (default: 1000).''')
@click.option('-s', default='', metavar='<stopL1:stopL2...>',
    help='''Stop values for graded-uniform NCU '''\
    + '''(default: same as gain values).''')
def compute(labelled_ranked_list, r, g, verbose, j, ec, gap,
    sep, out, beta, gamma, logb, rbp, cutoffs, s):

    # verbose?
    if verbose:
        handler.setLevel(DEBUG)
        logger.setLevel(DEBUG)

    # parsing parameters
    grades = read_grades(g)
    maxrel = len(grades)
    stops = read_stops(s) if len(s.strip()) > 0 else list(grades)
    cutoffs = read_cutoffs(cutoffs)
    logb = np.exp(1) if logb == 0 else logb # if logb == 0, then e

    # processing the rel file
    qrels = read_rel_file(r, sep)
    xrelnum, jrelnum = count_judged(maxrel, qrels)
    # TODO: count_ec_judged
    if ec:
        raise Exception("EC has not been implemented yet")

    # processing labelled ranked list
    sysdoclab = read_labelled_ranked_list(labelled_ranked_list)
    syslen = len(sysdoclab)
    maxlen = syslen if syslen > jrelnum else jrelnum

    # validation
    compute_validation(j, grades, stops, beta, gamma, logb, rbp,
        xrelnum, jrelnum)

    # verbose
    logger.debug("%s # Grades\t" % out + ', '.join(['L%s:%s' % (i+1, grade)
        for i, grade in enumerate(grades)]))
    logger.debug("%s # Stops\t" % out + ', '.join(['L%s:%s' % (i+1, stop)
        for i, stop in enumerate(stops)]))
    logger.debug("%s # X-Rel nums\t" % out + ', '.join(['L%s:%s' % (i, num)
        for i, num in enumerate(xrelnum)]))

    # output
    print("%s # syslen=%d jrel=%d jnonrel=%d" 
        % (out, syslen, jrelnum, xrelnum[0]))

    # compute metrics
    metrics = []
    for cutoff in cutoffs:
        metrics.append(MSnDCG(xrelnum, grades, logb, cutoff))

    for metric in metrics:
        score = metric.compute(sysdoclab)
        print(metric.__class__.__name__, score)
