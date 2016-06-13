# -*- coding:utf-8 -*-
import sys, os
import unittest
from click.testing import CliRunner
from pyNTCIREVAL.main import cli
from tests.helper import ntcireval_formatting

def p(path):
    return os.path.join(os.path.dirname(__file__), 'dat', path)

def r(name):
    return open(p("res_%s.txt" % name)).read()

class MainTestCase(unittest.TestCase):
    def setUp(self):
        pass

    def test_label(self):
        runner = CliRunner()
        result = runner.invoke(cli, ['label', 
            '-r', p('sample.rel'),
            p('sample.res')])
        self.assertEqual(result.output.strip(), 
            '''
dummy11 L0
dummy01 L3
dummy12
dummy04 L2
'''.strip())

    def test_compute(self):
        runner = CliRunner()
        result = runner.invoke(cli, ['compute', 
            '-r', p('sample.rel'),
            '-g', '1:2:3',
            p('sample.lab')])
        self.assertEqual(result.output.strip().replace(" ", ""),
            ntcireval_formatting(r("test_compute")))

    def test_compute_grade(self):
        runner = CliRunner()
        result = runner.invoke(cli, ['compute', 
            '-r', p('sample.rel'),
            '-g', '1:4:9',
            p('sample.lab')])
        self.assertEqual(result.output.strip().replace(" ", ""),
            ntcireval_formatting(r("test_compute_grade")))

    def test_compute_cutoff(self):
        runner = CliRunner()
        result = runner.invoke(cli, ['compute', 
            '-r', p('sample.rel'),
            '-g', '1:2:3',
            '--cutoffs', '2',
            p('sample.lab')])
        self.assertEqual(result.output.strip().replace(" ", ""),
            ntcireval_formatting(r("test_compute_cutoff")))

    def test_compute_label_j(self):
        runner = CliRunner()
        result = runner.invoke(cli, ['compute', 
            '-r', p('sample.rel'),
            '-g', '1:2:3',
            p('sample-j.lab')])
        self.assertEqual(result.output.strip().replace(" ", ""),
            ntcireval_formatting(r("test_compute_label_j")))
