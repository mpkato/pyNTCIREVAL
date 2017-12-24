import click
import numpy as np

from .utils import (read_grades, read_stops, read_cutoffs, read_rel_file,
    read_ranked_list, read_labelled_ranked_list, output_labelled_ranked_list,
    compute_validation)
from .labeler import Labeler
from .metrics import (Metric, RR, OMeasure, PMeasure, PPlusMeasure,
    AP, QMeasure, NCUguP, NCUguBR, NCUrbP, NCUrbBR,
    RBP, ERR, nERR, nDCG, MSnDCG, Precision, Hit)

# Log settings
from logging import getLogger, StreamHandler, DEBUG, INFO
logger = getLogger(__name__)
handler = StreamHandler()
handler.setLevel(INFO)
logger.setLevel(INFO)
logger.addHandler(handler)

LEFT_PADDING = 21

@click.group(context_settings={"help_option_names": ['-h', '--help']})
def cli():
    pass

# label command
@cli.command()
@click.argument('ranked_list', required=False,
    type=click.File('r'), metavar='[ranked list]')
@click.option('-r', type=click.File('r'), metavar='<relfile>', required=True,
    help='''A rel (relevance assessments) file''')
@click.option('-j', is_flag=True, default=False,
    help='''Treat the input as a condensed list (unjudged docs removed)''')
@click.option('--ec', is_flag=True, default=False,
    help='''Equivalence class mode''')
@click.option('--sep', default=' ', metavar='<separator>',
    help='''Input/output field separator (default: ' ').''')
@click.option('--truncate', metavar='<rank>',
    help='''Truncate a ranked list at <rank> if specified.''')
def label(ranked_list, r, j, ec, sep, truncate):
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
    labeler = Labeler(qrels, truncate=truncate, is_condensed=j)

    # processing a ranked list
    sysdocs = read_ranked_list(ranked_list)

    # label documents with their relevance level
    sysdoclab = labeler.label(sysdocs)

    # output the ranked list of documents with their relevance level
    output_labelled_ranked_list(sysdoclab)

# compute command
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
    rel_level_num = len(grades) + 1 # the number of grades here does not include level 0.
    stops = read_stops(s) if len(s.strip()) > 0 else list(grades)
    cutoffs = read_cutoffs(cutoffs)
    logb = np.exp(1) if logb == 0 else logb # if logb == 0, then e

    # processing the rel file
    qrels = read_rel_file(r, sep)
    labeler = Labeler(qrels, is_condensed=j)
    xrelnum = labeler.compute_per_level_doc_num(rel_level_num)
    jrelnum = labeler.compute_rel_num()
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
    print("%s # r1=%d rp=%d"
        % (out, Metric.find_first_rel_rank(sysdoclab),
            Metric.find_first_max_rank(sysdoclab)))

    # compute metrics
    metrics = []
    metrics.append(RR())
    metrics.append(OMeasure(xrelnum, grades, beta))
    metrics.append(PMeasure(xrelnum, grades, beta))
    metrics.append(PPlusMeasure(xrelnum, grades, beta))
    metrics.append(AP(xrelnum, grades))
    metrics.append(QMeasure(xrelnum, grades, beta))
    metrics.append(NCUguP(xrelnum, grades, stops))
    metrics.append(NCUguBR(xrelnum, grades, stops, beta))
    metrics.append(NCUrbP(xrelnum, grades, gamma))
    metrics.append(NCUrbBR(xrelnum, grades, gamma, beta))
    metrics.append(RBP(xrelnum, grades, rbp))
    metrics.append(ERR(xrelnum, grades))
    for cutoff in cutoffs:
        metrics.append(AP(xrelnum, grades, cutoff))
        metrics.append(QMeasure(xrelnum, grades, beta, cutoff))
        metrics.append(nDCG(xrelnum, grades, logb, cutoff))
        metrics.append(MSnDCG(xrelnum, grades, cutoff))
        metrics.append(Precision(cutoff))
        metrics.append(nERR(xrelnum, grades, cutoff))
        metrics.append(Hit(cutoff))

    for metric in metrics:
        score = metric.compute(sysdoclab)
        print(("%s " % out +"%s=" % metric).ljust(LEFT_PADDING)
            + "%0.4f" % score)
