API
===

   from uk_postcode import decode
   decode("DN55 1PT")


CLI
===

   uk_postcode "DN55 1PT"


Rationale
=========

I considered regexp and logic branching approaches too complex in implementation and support.

Proposed solution idea derived from Petri nets. This allows to declare logic in graph (in fact, in a series of graphs) and have relatively small amount of Python code. Finding errors is fast if you understand what names of nodes mean.

I am generating uk_postcode package to minimize dependencies, used resource and time spent on useful work. It does not use even regular expressions and should work relatively fast.


Development Cycle
=================

add test cases to tests/
run ./setup.py test
edit postal.dot, decode_template.py or handlers.py (all in ./code_generator/
run ./setup.py gen
start over with ./setup.py test
when happy:
change version in setup.py
run ./setup.py sdist


Graph
=====

For those who knows what Petri net is: the graph here is not a real Petri net. I do not calculate links/markers. It is more like a marker moving from initial state through transitions and structure states until it finishs.

But it is similar in separation of nodes on states/transitions and having verices connected only nodes of different kinds. Also, we have context (dictionary object).

The net state is change syncronously with input chars. States divide in 3 kinds:
 - Structure states indicate the structure reached (S_). Become active when preceding transition becomes active.
 - Receptor states, represent predicates (logical conditions) based on type receptor class and it's arguments. (X_, C_, R_, AE_, ARI). Link from a receptor to a transition is always labelled with "+" or "-", thus allowing or forbidding transition to become active. All positives and no negatives connections must be on for transition to become active.
 - Accumulator states (A_). Add current input char to corresponding part of context dictionary.
