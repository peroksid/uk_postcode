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

Proposed solution idea derived from Petri nets. This allows to declare logic in graph (in fact, in a series of graphs) and have relatively small amount of Python code.

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


