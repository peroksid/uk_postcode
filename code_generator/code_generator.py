import json
import logging
import os
import os.path
import re
import shutil

from collections import defaultdict

from pydotplus import graph_from_dot_file

from .validators import VALIDATORS


logger = logging.getLogger(__name__)

source_dir = os.path.dirname(os.path.realpath(__file__))
destination_dir = os.path.join(os.path.dirname(source_dir), 'uk_postcode')


def source(filename):
    filepath = os.path.join(source_dir, filename)
    logger.debug('sourced %s for %s', filepath, filename)
    return filepath


def destination(filename):
    filepath = os.path.join(destination_dir, filename)
    logger.debug('destined %s for %s', filepath, filename)
    return filepath


def read_graphs():
    POSTAL_FILE = 'postal.dot'

    nodes = set()
    edges = []
    starting_states = set()
    ending_states = set()

    dotfile = source(POSTAL_FILE)
    logging.info('reading file %s', dotfile)
    for g in graph_from_dot_file(dotfile):
        logging.info('started graph %s', g.get_name())
        for e in g.get_edges():
            def error(message, *args):
                full_message = message % args + ': ' + e.to_string()
                logging.error(full_message)
                raise RuntimeError(full_message)

            l = [e.get_source(), e.get_destination()]

            label = e.get_label()
            if label is not None:
                if label not in ['"+"', '"-"']:
                    error('Unknown label %s', label)
                if not l[1].startswith('T_'):
                    error('positive/negative needs T_ as destination')
                l.append(label.replace('"', ''))
            else:
                if re.match('A_|S_|T_', l[0]) is None:
                    error('receptor must start signed edge')
                l.append(label)
            # validation start
            if l[0].startswith('A_'):
                error("A_ can't be source", e)
            elif l[0].startswith('T_'):
                if not (l[1].startswith('S_') or l[1].startswith('A_')):
                    error('bad destination for T')
            elif l[0].startswith('S_'):
                if not l[1].startswith('T_'):
                    error('source S_ requires destination T_')
            else:
                if not l[1].startswith('T_'):
                    error('receptors require destination T_')
            if l[1].startswith('A_'):
                if not l[0].startswith('T_'):
                    error(' A_ as destination requires  T_ as source')
            elif l[1].startswith('S_'):
                if not l[0].startswith('T_'):
                    error('source T_ requires destination S_')
            elif l[1].startswith('T_'):
                pass
            else:
                error("receptor can't be destination")
            # validation end
            # starting node search start
            if l[0].startswith('S_'):
                starting_states.add(l[0])
            if l[1].startswith('S_'):
                ending_states.add(l[1])
            # starting node search end
            # check known receptors start
            for x in l[0:2]:
                prefix, tail = x.split('_', 1)
                if prefix in VALIDATORS:
                    validators = VALIDATORS.get(prefix)
                    if validators is None:
                        error('validator not found for %s', x)
                    arguments = tail.split('_')
                    if len(arguments) != len(validators):
                        error('bad arity for prefix %s, arguments %s, node %s',
                              prefix, arguments, x)
                    if not all(v(a) for v, a in zip(validators, arguments)):
                        error('invalid arguments  for '
                              'prefix %s, arguments %s, node %s',
                              prefix, arguments, x)
                else:
                    if prefix not in ['S', 'T']:
                        error('unknown prefix %s', prefix)
            # check known receptors end
            edges.append(l)
            nodes.update(l[0:2])
    logger.debug(edges)
    logger.debug(nodes)
    states_difference = starting_states - ending_states
    if len(states_difference) != 1:
        error('1 starting state required %s', str(states_difference))
    else:
        START_STATE = list(states_difference)[0]
    return edges, nodes, START_STATE


def prepare_net(edges, nodes, start_state):
    def error(template, *args):
        message = template % args
        logging.error(message)
        raise RuntimeError(message)

    TRANSITIONS = defaultdict(list)
    STATES = {}
    POSITIVES = defaultdict(list)
    NEGATIVES = defaultdict(list)
    ACCUMULATORS = defaultdict(list)

    for e in edges:
        if e[0].startswith('S_'):
            TRANSITIONS[e[0]].append(e[1])
        if e[0].startswith('T_') and e[1].startswith('S_'):
            if e[0] in STATES:
                error('redefining transit->state: %s', str(e))
            STATES[e[0]] = e[1]

        if e[0].split('_', 1)[0] in VALIDATORS:
            logger.debug('e %s', e)
            if e[2] == "+":
                POSITIVES[e[1]].append(e[0])
            elif e[2] == "-":
                NEGATIVES[e[1]].append(e[0])
        if e[1].split('_', 1)[0] in VALIDATORS:
            ACCUMULATORS[e[0]].append(e[1])

    # raise RuntimeError
    finishing_states = set(STATES.values()) - set(TRANSITIONS.keys())
    if len(finishing_states) != 1:
        error('expect exactly 1 finishing_state')

    logger.debug(start_state)
    logger.debug(TRANSITIONS)
    logger.debug(STATES)
    logger.debug(POSITIVES)
    logger.debug(NEGATIVES)
    logger.debug(ACCUMULATORS)
    logger.debug(finishing_states)
    return start_state, TRANSITIONS, STATES, POSITIVES, NEGATIVES, ACCUMULATORS


def generate_code(START_STATE, TRANSITIONS, STATES,
                  POSITIVES, NEGATIVES, ACCUMULATORS):
    with open(source('decode_template.py')) as f:
        template = f.read()

    for varname in ('START_STATE', 'TRANSITIONS', 'STATES',
                    'POSITIVES', 'NEGATIVES', 'ACCUMULATORS'):
        template = template.replace(
            '%s = {}' % varname,
            '%s = %s' % (varname, json.dumps(locals()[varname],
                                             indent=4,
                                             separators=(',', ': '))))

    with open(destination('__init__.py'), 'w') as f:
        f.write(template)
    shutil.copy(source('handlers.py'), destination('handlers.py'))


def main():
    level = getattr(logging, os.getenv('LOGGING_LEVEL', 'ERROR'))
    logging.basicConfig(level=level)
    generate_code(*prepare_net(*read_graphs()))
