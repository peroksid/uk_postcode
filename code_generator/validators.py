import logging
import re

from .constants import ACCUMULATOR_NAMES


__all__ = ('VALIDATORS',)

logger = logging.getLogger(__name__)


VALIDATORS = {
    'X': [re.compile('^SPACE|[A-Z0-9]$').match],
    'AE': [lambda x: x in ACCUMULATOR_NAMES,
           re.compile('^[A-Z0-9]+$').match],
    'C': [lambda x: x in ('ALPHA', 'DIGIT', 'SPACE')],
    'R': [lambda x: len(x) > 0],
    'ARI': [lambda x: x in ACCUMULATOR_NAMES,
            lambda x: x.isdigit(),
            lambda x: len(x) > 0],
    'A': [lambda x: x in ACCUMULATOR_NAMES]
}
