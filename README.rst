Usage
=====

Python API::

    from uk_postcode import decode
    decode("DN55 1PT")


Example CLI::

    uk_postcode "DN55 1PT"


Rationale
=========

UK postal code system is rather complex: https://en.wikipedia.org/wiki/Postcodes_in_the_United_Kingdom#Postcode_unit

I think that regexp and/or logic branching would be too complex to implement and support.

Proposed solution declares logic in graph (in fact, in a series of graphs) and has relatively small amount of Python code. Finding errors is fast if you understand what names of nodes mean. Code to distribute is generated.

Resulting code does not even import regular expressions, requires nothing but standard library and is quite fast. It is easy to add rules, fix errors and reason about.


Development Cycle
=================

* add test cases to tests/
* LOGGING_LEVEL=DEBUG run ./setup.py test
* (edit postal.dot, decode_template.py or handlers.py (all in ./code_generator/
* run ./setup.py gen
* start over with ./setup.py test

When happy
* change version in setup.py
* ready to install/distribute now


Graph
=====

For those who knows what Petri net is: the graph here is not a real Petri net. I do not calculate links/markers. It is more like a marker moving from initial state through transitions and structure states until it finishs.

But it is similar in separation of nodes on states/transitions and having verices connected only nodes of different kinds. Also, we have context (dictionary object).

The net state is change syncronously with input chars. States divide in 3 kinds.

Structure states (S)
    Indicate the structure reached.
    Become active when preceding transition becomes active.

Receptor states (X, C, R, AE, ARI)
    Represent predicates (logical conditions) based on type receptor class and it's arguments. For example, X_SPACE is active if current char is space; ARI_AREA_0_AZ is active if first character of accumulator named "AREA" has A or Z as a first element.

    Link from a receptor to a transition is always labelled with "+" or "-", thus allowing or forbidding transition to become active. All positives and no negatives connections must be on for transition to become active.

Accumulator states (A)
    Add current input char to corresponding part of context dictionary.

File postal.dot contains graphs grouping states and transitions closely related to each other.
