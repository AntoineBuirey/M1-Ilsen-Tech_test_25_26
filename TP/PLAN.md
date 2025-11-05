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


### PointSetManager commucation module

Will be responsible to communicate with the PointSetManager service to retrieve point sets.
This is just an interface between the service and the program.

- [ ] test the PointSetManager communication module:
    - [ ] success case:
     mock the PointSetManager service to return a valid point set, check that the module correctly retrieves and parses it

    - [ ] failure case:
     mock the PointSetManager service to return an error (e.g. 404 Not Found), check that the module correctly handles the error and raises the appropriate exception from the module. 
     The message from the api should be transferred through the exception.
     Should raise:
     - `ValueError` if getting a 400 Bad Request
     - `KeyError` if getting a 404 Not Found
     - `RuntimeError` for 503 Database Unavailable


### Api

> Note: for all this tests, the algorithm is mocked to avoid getting errors from it when not testing it, as well as PointSetManager communication module.

- [ ] test the `triangulation` endpoint:

    - [ ] success case:
     send a valid request with a set of points, check the response contains the correct triangulation and status code 200
    
    - [ ] invalid input case:
     send a request with invalid data (like a empty, malformed or inexistant `PointSetID`), and check the response contains the appropriate error message
     - invalid `PointSetID` format, or empty `PointSetID`:
        - code 400 Bad Request
        - body in json containing a internal error code and an error message
    - inexistant `PointSetID`:
        - code 404 Not Found
        - body in json containing a internal error code and an error message

    - [ ] algorithm failure case:
     mock the algorithm to raise an exception, send a valid request and check the response contains the appropriate error message
        In that case, the response should be:
        - code 500 Internal Server Error
        - body in json containing a internal error code and an error message THAT DOES NOT REVEAL INTERNAL DETAILS OF THE SERVER (like stack traces, exception messages, etc.)

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
    > The system profile should be noted (CPU, RAM, OS, python version, etc.) to ensure reproducibility of the results.