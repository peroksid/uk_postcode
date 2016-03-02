import logging
import re
from collections import defaultdict

from pydotplus import graph_from_dot_file


logger = logging.getLogger(__name__)

logging.basicConfig(level=logging.DEBUG)


POSTAL_FILE = 'postal.dot'


ACCUMULATOR_NAMES = ('AREA', 'OUTWARD', 'SECTOR', 'INWARD', 'UNIT', 'TOWN')


class X(object):
    validators = [re.compile('^SPACE|[A-Z0-9]$').match]

    def __init__(self, value):
        if value == 'SPACE':
            self.value = ' '
        else:
            self.value = value

    def __call__(self, _context, char):
        return char == self.value


class AE(object):
    validators = [lambda x: x in ACCUMULATOR_NAMES, re.compile('^[A-Z0-9]+$').match]

    def __init__(self, accumulator_name, value):
        self.accumulator_name = accumulator_name
        self.value = value

    def __call__(self, context, _char):
        return context.get(self.accumulator_name) == self.value


class C(object):
    validators = [lambda x: x in ('ALPHA', 'DIGIT', 'SPACE')]

    def __init__(self, value):
        self.klass = value

    def __call__(self, _context, char):
        if self.klass == 'ALPHA':
            return char.isalpha()
        elif self.klass == 'DIGIT':
            return char.isdigit()
        else:
            return char == ' '


class R(object):
    validators = [lambda x: len(x) > 0]

    def __init__(self, char_range):
        self.values = list(char_range)

    def __call__(self, _context, char):
        return char in self.values


class ARI(object):
    validators = [lambda x: x in ACCUMULATOR_NAMES, lambda x: x.isdigit(), lambda x: len(x) > 0]

    def __init__(self, accumulator_name, index, char_range):
        self.accumulator_name = accumulator_name
        self.index = index
        self.char_range = char_range

    def __call__(self, context, _char):
        value = context.get(self.accumulator_name)
        return (value is not None and len(value) > self.index 
                and value[self.index] in self.char_range)


class A(object):
    validators = [lambda x: x in ACCUMULATOR_NAMES]
    def __init__(self, accumulator_name):
        self.accumulator_name = accumulator_name

    def __call__(self, context, char):
        if self.accumulator_name not in context:
            context[self.accumulator_name] = ''
        context[self.accumulator_name] += char
        logger.debug('called')
        return context


HANDLERS = dict((klass.__name__, klass) for klass in (X, AE, C, R, ARI, A))


nodes = set()
edges = []
starting_states = set()
ending_states = set()

logging.info('reading file %s', POSTAL_FILE)
for g in graph_from_dot_file(POSTAL_FILE):
    logging.info('started graph %s', g.get_name())
    for e in g.get_edges():
        def error(message, *args):
            full_message = message % args + ': ' + e.to_string()
            logging.error(full_message)
            raise RuntimeError, full_message

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
            if prefix in HANDLERS:
                klass = HANDLERS[prefix]
                arguments = tail.split('_')
                if len(arguments) != len(klass.validators):
                    error('bad arity from  %s for %s', x, klass.__name__)
                else:
                    if not all(v(a) for v, a in zip(klass.validators, arguments)):
                        error('invalid arguments %s for %s', arguments, klass.__name__)
            else:
                if prefix not in ['S', 'T']:
                    error('unknown prefix %s', prefix)
        # check known receptors end
        edges.append(l)
        nodes.update(l[0:2])

logger.debug(edges)
logger.debug(nodes)


def error(template, *args):
    message = template % args
    logging.error(message)
    raise RuntimeError, message

states_difference = starting_states - ending_states
if len(states_difference) != 1:
    error('1 starting state required %s', str(states_difference))
else:
    START_STATE = list(states_difference)[0]

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

    parts = e[0].split('_')
    if parts[0] in HANDLERS:
        handler = HANDLERS[parts[0]](*parts[1:])
        logger.debug('e %s', e)
        if e[2] is not None:
            (POSITIVES if e[2] == '+' else NEGATIVES)[e[1]].append(handler)
    parts = e[1].split('_')
    if parts[0] in HANDLERS:
        handler = HANDLERS[parts[0]](*parts[1:])
        ACCUMULATORS[e[0]].append(handler)

# raise RuntimeError
finishing_states = set(STATES.values()) - set(TRANSITIONS.keys())
if len(finishing_states) != 1:
       error('expect exactly 1 finishing_state')

print START_STATE
print TRANSITIONS
print STATES
print POSITIVES
print NEGATIVES
print finishing_states

def decode(code):
    state = START_STATE
    context = {}
    for index, char in enumerate(code):
        logger.debug(char)
        logger.debug(state)
        logger.debug(context)
        for t in TRANSITIONS[state]:
            if all(x(context, char) for x in POSITIVES[t]):
                if not any(x(context, char) for x in NEGATIVES[t]):
                    state = STATES[t]
                    logger.debug('new state %s', state)
                    logger.debug('accumulators %s', ACCUMULATORS[t])
                    for a in ACCUMULATORS[t]:
                        context = a(context, char)
                    break
        else:
            raise RuntimeError, "all transitions are inactive"
    return context

logger.debug('ACCUMULATORS %s', ACCUMULATORS)

print decode('DN55 1PT')
                  
    
       

        
        
