## pytest
- Use of pytest is we can run from the last failed test and also we can skip the tests
- (Auto Discovery of Tests) `pytest` has the ability to pick up the test functions automatically if the files are saves with the prefix or suffix as a test_file.py or file_test.py format.
- Rich Assertion introspection 'Provides a deeper code tracing if anything goes wrong'.
- Supports Parameterized fixture-based testing.

## why pytest over other testing frameworks like unittest or noise?
- pytest has a simplified syntax
- Rich assertion introspection
- compatibility
- Extensibility `(if we have a Django application then we have a Django plugin we just have to install it and write the testcases)`

## How to run a pytest and how it works?
- By just entering the command as `pytest` in the terminal. 
- pytest framework automatically starts the execution of tests by finding the filenames prefixed with `test_* or *_test`

## Components of pytest
- assert ``one single statement is enough to compare either normal values or dictionaries or even lists or tuples or arrays``
- To check the console debugging statements we have to run the following command
   `pytest -s`. If we run without `-s` then the debugging statements won't be visible.

## What is Unit testing?

- Unit tests test individual units (modules, functions, classes) in isolation from the rest of the program.
- Since these unit tests validate only the individual units, only desired unit/class should be initialized in the test classes. 
- To ignore external service or external technical dependencies such as datasource, we can use mocks to imitate their behaviors. 
- Unit tests should take too short since they do not depend on any external source or services.
- A unit test is a smaller test, one that checks that a single component operates in the right way.
- unit test helps you to isolate what is broken in your application and fix it faster.

## What is Integration testing?
- mdd
