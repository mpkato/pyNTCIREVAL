# -*- coding:utf-8 -*-
import unittest
import nose
from click.testing import CliRunner
from pyNTCIREVAL.scripts.main import cli

class ScriptsTestCase(unittest.TestCase):
    def setUp(self):
        pass

    def test_say(self):
        runner = CliRunner()
        result = runner.invoke(cli, ['say'])
        self.assertEqual(result.output, 'Hello World\n')
