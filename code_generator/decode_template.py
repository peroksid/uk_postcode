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
        logger.debug('char: "%s"', char)
        logger.debug('states: %s', state)
        logger.debug('context %s', context)
        transitions = TRANSITIONS[state]
        logger.debug('transitions %s', transitions)
        for t in transitions:
            logger.debug('transition %s', t)
            positives = POSITIVES.get(t, [])
            logger.debug('positives %s', positives)
            positive_results = [x(context, char) for x in positives]
            if all(positive_results):
                negatives = NEGATIVES.get(t, [])
                logger.debug('negatives %s', negatives)
                negative_results = [x(context, char) for x in negatives]
                if not any(negative_results):
                    state = STATES.get(t)
                    logger.debug('new state %s', state)
                    logger.debug('accumulators %s', ACCUMULATORS.get(t, []))
                    for a in ACCUMULATORS.get(t, []):
                        a(context, char)
                    break
                else:
                    logger.debug('negatives rejected %s', negative_results)
            else:
                logger.debug('positives rejected %s', positive_results)
        else:
            raise RuntimeError("all transitions are inactive")
    return context
