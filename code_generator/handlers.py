import logging


logger = logging.getLogger(__name__)


class X(object):
    def __init__(self, value):
        if value == 'SPACE':
            self.value = ' '
        else:
            self.value = value

    def __call__(self, _context, char):
        return char == self.value


class AE(object):
    def __init__(self, accumulator_name, value):
        self.accumulator_name = accumulator_name
        self.value = value

    def __call__(self, context, _char):
        return context.get(self.accumulator_name) == self.value


class C(object):
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
    def __init__(self, char_range):
        self.values = list(char_range)

    def __call__(self, _context, char):
        return char in self.values


class ARI(object):
    def __init__(self, accumulator_name, index, char_range):
        self.accumulator_name = accumulator_name
        self.index = index
        self.char_range = char_range

    def __call__(self, context, _char):
        value = context.get(self.accumulator_name)
        return (value is not None and len(value) > self.index
                and value[self.index] in self.char_range)


class A(object):
    def __init__(self, accumulator_name):
        self.accumulator_name = accumulator_name

    def __call__(self, context, char):
        if self.accumulator_name not in context:
            context[self.accumulator_name] = ''
        context[self.accumulator_name] += char
        logger.debug('called')
        return context


HANDLERS = dict((klass.__name__, klass) for klass in (X, AE, C, R, ARI, A))


def get_handler(node_id):
    tokens = node_id.split('_')
    handler = HANDLERS[tokens[0]](*tokens[1:])
    return handler
