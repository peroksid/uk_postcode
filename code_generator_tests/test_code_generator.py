import logging
import unittest


from code_generator.validators import VALIDATORS
from code_generator.handlers import HANDLERS



class HanldersTestCase(unittest.TestCase):
    def test_main(self):
        self.assertEqual(len(VALIDATORS), len(HANDLERS))

        for k in VALIDATORS:
            logging.debug(k)
            self.assertEqual(len(VALIDATORS[k]),
                             HANDLERS[k].__init__.im_func.func_code.co_argcount - 1)
