# Tests to do:

## Behavior tests

### Algorithm

> Note: I will not test any function with arguments of bad types, because Python 3.13 (version used) has type hints and static analysis tools can be used to check types before runtime. Bad programmers should be punished by bad reviews, not by writing redundant tests.


- [ ] test the main algorithm:

    - [ ] success case:
     given input a set of points (a `PointSet` Object), check the output is correct (a `Triangles` Object)

    - [ ] invalid input case:
     given invalid input (e.g. empty `PointSet`), check that the algorithm raises the appropriate exception

    - [ ] edge case:
     given input with minimal number of points (e.g. 3 points), check the output is correct

- [ ] test helper functions used in the algorithm:
    - [ ] success case:
     for each helper function, provide valid input and check the output is as expected

    - [ ] invalid input case:
     for each helper function, provide invalid input and check that the appropriate exception is raised

### Api

> Note: for all this tests, the algorithm is mocked to avoid getting errors from it when not testing it.

- [ ] test the `triangulation` endpoint:

    - [ ] success case:
     send a valid request with a set of points, check the response contains the correct triangulation
    
    - [ ] invalid input case:
     send a request with invalid data (like a empty, malformed or inexistant `PointSetID`), and check the response contains the appropriate error message

    - [ ] algorithm failure case:
     mock the algorithm to raise an exception, send a valid request and check the response contains the appropriate error message

## Performance tests

> Note: only the main algorithm is tested here, not the api, because the api the performance can be affected by many external factors (network latency, server load, etc.) that are not related to the algorithm itself.

- [ ] test the performance of the algorithm with datasets of increasing size:
    - minimal dataset (3 points)
    - vey-small dataset (e.g. 100 points)
    - small dataset (e.g. 1,000 points)
    - medium dataset (e.g. 10,000 points)
    - large dataset (e.g. 100,000 points)
    - very-large dataset (e.g. 1,000,000 points)

- [ ] For each dataset, measure:
    - the execution time
    - memory usage of the algorithm