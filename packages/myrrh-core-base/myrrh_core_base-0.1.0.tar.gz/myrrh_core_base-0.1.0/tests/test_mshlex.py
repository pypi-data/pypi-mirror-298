import unittest

from myrrh.core.utils import mshlex


class TestShcmd(unittest.TestCase):

    def test_basic(self):

        _, cmd = mshlex.shcmd("ls {opt:PATH}", options={"PATH": "/path"})
        self.assertEqual(cmd, "ls /path")
        _, cmd = mshlex.shcmd("ls {opt:PATH}", options={"ANOTHER": "/path"})
        _, self.assertEqual(cmd, "ls")
        _, cmd = mshlex.shcmd("ls {opt:PATH: -l {PATH}}", options={"PATH": "/path"})
        _, self.assertEqual(cmd, "ls  -l /path")
        _, cmd = mshlex.shcmd("ls {opt:PATH: -l {PATH}}", options={"ANOTHER": "/path"})
        _, self.assertEqual(cmd, "ls")


if __name__ == "__main__":
    unittest.main(verbosity=2)
