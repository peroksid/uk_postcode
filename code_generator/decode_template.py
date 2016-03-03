import logging

from .handlers import get_handler


logger = logging.getLogger(__name__)


START_STATE = {}
TRANSITIONS = {}
STATES = {}
ACCUMULATORS = {}
POSITIVES = {}
NEGATIVES = {}

for collection in (ACCUMULATORS, POSITIVES, NEGATIVES):
    for t_id, node in collection.items():
        collection[t_id] = [get_handler(x) for x in node]


def decode(code):
    state = START_STATE
    context = {}
    for index, char in enumerate(code):
        logger.debug(char)
        logger.debug(state)
        logger.debug(context)
        for t in TRANSITIONS[state]:
            if all(x(context, char) for x in POSITIVES.get(t, [])):
                if not any(x(context, char) for x in NEGATIVES.get(t, [])):
                    state = STATES.get(t)
                    logger.debug('new state %s', state)
                    logger.debug('accumulators %s', ACCUMULATORS.get(t, []))
                    for a in ACCUMULATORS.get(t, []):
                        context = a(context, char)
                    break
        else:
            raise RuntimeError("all transitions are inactive")
    return context
