# -*- coding:utf-8 -*-
import sys, os
import unittest
import nose
from click.testing import CliRunner
from pyNTCIREVAL.main import cli

def p(path):
    return os.path.join(os.path.dirname(__file__), 'dat', path)

def r(name):
    return open(p("res_%s.txt" % name)).read()

class MainTestCase(unittest.TestCase):
    def setUp(self):
        self.maxDiff = 10000
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
            self._formatting(r("test_compute")))

    def test_compute_grade(self):
        runner = CliRunner()
        result = runner.invoke(cli, ['compute', 
            '-r', p('sample.rel'),
            '-g', '1:4:9',
            p('sample.lab')])
        self.assertEqual(result.output.strip().replace(" ", ""),
            self._formatting(r("test_compute_grade")))

    def test_compute_cutoff(self):
        runner = CliRunner()
        result = runner.invoke(cli, ['compute', 
            '-r', p('sample.rel'),
            '-g', '1:2:3',
            '--cutoffs', '2',
            p('sample.lab')])
        self.assertEqual(result.output.strip().replace(" ", ""),
            self._formatting(r("test_compute_cutoff")))

    def test_compute_label_j(self):
        runner = CliRunner()
        result = runner.invoke(cli, ['compute', 
            '-r', p('sample.rel'),
            '-g', '1:2:3',
            p('sample-j.lab')])
        self.assertEqual(result.output.strip().replace(" ", ""),
            self._formatting(r("test_compute_label_j")))

    OLD_NEWS = [
        ("O-measure", "OMeasure"),
        ("P-measure", "PMeasure"),
        ("P-plus", "PPlusMeasure"),
        ("Q-measure", "QMeasure"),
        (",P", "P"),
        (",BR", "BR"),
        ("Q@", "QMeasure@"),
        ("\nP@", "\nPrecision@"),
    ]
    def _formatting(self, output):
        output = output.strip().replace(" ", "")
        for old, new in self.OLD_NEWS:
            output = output.replace(old, new)
        return output
