#!/bin/bash

RUN_NAME=$1

LOREM_IPSUM_5="Lorem ipsum dolor sit amet,"
LOREM_IPSUM_100="""
  Lorem ipsum dolor sit amet, consetetur sadipscing elitr,
  sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat,
  sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum.
  Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet.
  Lorem ipsum dolor sit amet, consetetur sadipscing elitr,
  sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua.
  At vero eos et accusam et justo duo dolores et ea rebum.
  Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet.
"""
LOREM_IPSUM_200="""
  Lorem ipsum dolor sit amet, consetetur sadipscing elitr,
  sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat,
  sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum.
  Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet.
  Lorem ipsum dolor sit amet, consetetur sadipscing elitr,
  sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat, sed diam voluptua.
  At vero eos et accusam et justo duo dolores et ea rebum.
  Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet.  Lorem ipsum dolor sit amet, consetetur sadipscing elitr,
  sed diam nonumy eirmod tempor invidunt ut labore et dolore magna aliquyam erat,
  sed diam voluptua. At vero eos et accusam et justo duo dolores et ea rebum.
  Stet clita kasd gubergren, no sea takimata sanctus est Lorem ipsum dolor sit amet.
"""

# Lorem ipsum 5
echo "Lorem ipsum (5) loop counter 5"
python3 task_1.py $RUN_NAME "$LOREM_IPSUM_5" 5
echo "Lorem ipsum (5) loop counter 100"
python3 task_1.py $RUN_NAME "$LOREM_IPSUM_5" 100
echo "Lorem ipsum (5) loop counter 1000"
python3 task_1.py $RUN_NAME "$LOREM_IPSUM_5" 1000

# Lorem ipsum 100
echo "Lorem ipsum (100) loop counter 5"
python3 task_1.py $RUN_NAME "$LOREM_IPSUM_100" 5
echo "Lorem ipsum (100) loop counter 100"
python3 task_1.py $RUN_NAME "$LOREM_IPSUM_100" 100
echo "Lorem ipsum (100) loop counter 1000"
python3 task_1.py $RUN_NAME "$LOREM_IPSUM_100" 1000

# Lorem ipsum 1000
echo "Lorem ipsum (200) loop counter 5"
python3 task_1.py $RUN_NAME "$LOREM_IPSUM_200" 5
echo "Lorem ipsum (200) loop counter 100"
python3 task_1.py $RUN_NAME "$LOREM_IPSUM_200" 100
echo "Lorem ipsum (200) loop counter 1000"
 python3 task_1.py $RUN_NAME "$LOREM_IPSUM_200" 1000