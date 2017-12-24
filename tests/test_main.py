# -*- coding:utf-8 -*-
import sys, os
from click.testing import CliRunner
from pyNTCIREVAL.main import cli
from tests.helper import ntcireval_formatting

class TestMain(object):

    def _p(self, path):
        return os.path.join(os.path.dirname(__file__), 'dat', path)

    def _r(self, name):
        return open(self._p("res_%s.txt" % name)).read()

    def test_label(self):
        runner = CliRunner()
        result = runner.invoke(cli, ['label',
            '-r', self._p('sample.rel'),
            self._p('sample.res')])
        assert result.output.strip() ==\
            '''
dummy11 L0
dummy01 L3
dummy12
dummy04 L2
            '''.strip()

    def test_compute(self):
        runner = CliRunner()
        result = runner.invoke(cli, ['compute', 
            '-r', self._p('sample.rel'),
            '-g', '1:2:3',
            self._p('sample.lab')])
        assert result.output.strip().replace(" ", "") ==\
            ntcireval_formatting(self._r("test_compute"))

    def test_compute_grade(self):
        runner = CliRunner()
        result = runner.invoke(cli, ['compute', 
            '-r', self._p('sample.rel'),
            '-g', '1:4:9',
            self._p('sample.lab')])
        assert result.output.strip().replace(" ", "") ==\
            ntcireval_formatting(self._r("test_compute_grade"))

    def test_compute_cutoff(self):
        runner = CliRunner()
        result = runner.invoke(cli, ['compute', 
            '-r', self._p('sample.rel'),
            '-g', '1:2:3',
            '--cutoffs', '2',
            self._p('sample.lab')])
        assert result.output.strip().replace(" ", "") ==\
            ntcireval_formatting(self._r("test_compute_cutoff"))

    def test_compute_label_j(self):
        runner = CliRunner()
        result = runner.invoke(cli, ['compute', 
            '-r', self._p('sample.rel'),
            '-g', '1:2:3',
            self._p('sample-j.lab')])
        assert result.output.strip().replace(" ", "") ==\
            ntcireval_formatting(self._r("test_compute_label_j"))
