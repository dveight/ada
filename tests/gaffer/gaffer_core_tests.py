import os
import tempfile
import unittest2 as unittest

import shutil

import Gaffer

from ada.core.utils import is_nuke, is_gaffer
import ada.core.gaffer.executable


class AdaCoreGafferTestCase(unittest.TestCase):

    def test_nuke_executable(self):
        self.assertTrue(ada.core.gaffer.executable.GAFFER_EXECUTABLE)
        self.assertTrue(os.path.exists(ada.core.gaffer.executable.GAFFER_EXECUTABLE))

    def test_is_nuke(self):
        self.assertFalse(is_nuke())

    def test_is_gaffer(self):
        self.assertTrue(is_gaffer())


class AdaGafferTestCase(unittest.TestCase):

    def setUp(self):
        self.root = Gaffer.ScriptNode()
        self.tempdir = None

    def test_bake_noop(self):
        with self.root.context():
            dot = Gaffer.Dot()
            self.root["dot"] = dot

    def tearDown(self):
        del self.root
        if self.tempdir and os.path.exists(self.tempdir):
            shutil.rmtree(self.tempdir)


if __name__ == "__main__":
    unittest.main()
