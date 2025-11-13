# Objects definitions

## PointSet
A PointSet is an object that contains a set of points in 2D space.
Each point is represented by its x and y coordinates (float).

### Minimum methods

- `add_point(x: float, y: float)`: adds a point to the set
- `remove_point(index: int)`: removes the point at the given index
- `__iter__()`: returns an iterator over the points in the set
- `__len__()`: returns the number of points in the set
- `get_point(index: int)`: returns the point at the given index
- `set_point(index: int, value: Tuple[float, float])`: sets the point at the given index
- `__eq__(other: PointSet)`: checks if two PointSet objects are equal (all points are the same and in the same order)
- `to_bytes()`: serializes the PointSet to bytes for transmission
- *`from_bytes(data: bytes)`*: deserializes bytes to a PointSet object

### Constructor
- `__init__(points: Optional[List[Tuple[float, float]]] = None)`: initializes the PointSet with an optional list of points


## Triangles
A Triangles object is an object that contains a set of triangles in 2D space.
Each triangle is represented by the indices of its three vertices in the original PointSet.
The PointSet used to create the Triangles object must be stored within the Triangles object for reference.
For this reason, the Triangles object will inherit from the PointSet object.

### Minimum methods
- `add_triangle(i1: int, i2: int, i3: int) -> int`: adds a triangle to the set,
    raise `IndexError` if any index is out of bounds of the underlying PointSet
    raise `ValueError` if the three indices are not unique
    raise `ValueError` if a triangle with the same indices already exists (regardless of the order of the indices)
    return the index of the newly added triangle
- `remove_triangle(index: int)`: removes the triangle at the given index,
    raise `IndexError` if the index is out of bounds
    return nothing
- `__iter__()`: returns an iterator over the triangles in the set
- `__len__() -> int`: returns the number of triangles in the set
- `get_triangle(index: int) -> Triangle`: returns the triangle at the given index,
    raise `IndexError` if the index is out of bounds
    raise `ValueError` if the triangle at the given index is invalid (e.g. indices out of bounds of the PointSet)
- `set_triangle(index: int, value: Tuple[int, int, int])`: sets the triangle at the given index
- `__eq__(other: Triangles)`: checks if two Triangles objects are equal (all triangles are the same and in the same order, and the underlying PointSets are equal)
- `to_bytes()`: serializes the Triangles to bytes for transmission
- *`from_bytes(data: bytes)`*: deserializes bytes to a Triangles object

### Constructor
- `__init__(point_set: Optional[List[Tuple[float, float]]] = None, triangles: Optional[List[Tuple[int, int, int]]] = None)`: initializes the Triangles with an optional PointSet and an optional list of triangles

## PointSetManager (PSM)
The PointSetManager is a module responsible for communicating with the PointSetManager service to retrieve point sets.
It's not a class, but a module with functions to interact with the service.
It's a wrapper around the service API.

### methods
> Note: only the get_point_set method is required, as we don't need to register new point sets from the triangulator.

- *`get_point_set(point_set_id: str) -> PointSet`*: retrieves the PointSet with the given ID from the PointSetManager service.
    - raises `ValueError` if the request is invalid (400 Bad Request)
    - raises `KeyError` if the PointSetID does not exist (404 Not Found)
    - raises `RuntimeError` if the service is unavailable (503 Database Unavailable)



# Tests to do

## Behavior tests


### PointSet and Triangles objects
- [x] test PointSet to_bytes and from_bytes methods:
    - [x] success case:
     create a PointSet object, serialize it to bytes, then deserialize it back to a PointSet object, and check that the original and deserialized objects are equal

    - [x] invalid input case:
     provide invalid bytes data to from_bytes method and check that the appropriate exception is raised. eg.
        - data that does not represent a valid PointSet object
        - data with invalid point coordinates (e.g. non-float values)
        - data where the number of points is inconsistent with the data length

- [x] test Triangles to_bytes and from_bytes methods:
    - [x] success case:
     create a Triangles object, serialize it to bytes, then deserialize it back to a Triangles object, and check that the original and deserialized objects are equal
    - [x] invalid input case:
     provide invalid bytes data to from_bytes method and check that the appropriate exception is raised. eg.
        - data that does not represent a valid Triangles object
        - data that represents a Triangles object with invalid triangle indices (e.g. indices out of bounds of the PointSet)
        - data with inconsistent number of triangles
        - data where the PointSet part is invalid


### Algorithm

> Note: I will not test any function with arguments of bad types, because Python 3.13 (version used) has type hints and static analysis tools can be used to check types before runtime. Bad programmers should be punished by bad reviews, not by writing redundant tests.


- [x] test the main algorithm:

    - [x] success case:
     given input a set of points (a `PointSet` Object), check the output is correct (a `Triangles` Object)

    - [x] invalid input case:
     given invalid input (e.g. empty `PointSet`), check that the algorithm raises the appropriate exception

    - [x] edge case:
     given input with minimal number of points (e.g. 3 points), check the output is correct

- [ ] test helper functions used in the algorithm:
    > will be done once the helper functions are implemented
    - [ ] success case:
     for each helper function, provide valid input and check the output is as expected

    - [ ] invalid input case:
     for each helper function, provide invalid input and check that the appropriate exception is raised


### PointSetManager commucation module

Will be responsible to communicate with the PointSetManager service to retrieve point sets.
This is just an interface between the service and the program.

- [x] test the PointSetManager communication module:
    - [x] success case:
     mock the PointSetManager service to return a valid point set, check that the module correctly retrieves it

    - [x] failure case:
     mock the PointSetManager service to return an error (e.g. 404 Not Found), check that the module correctly handles the error and raises the appropriate exception from the module. 
     The message from the api should be transferred through the exception.
     Should raise:
     - `ValueError` if getting a 400 Bad Request
     - `KeyError` if getting a 404 Not Found
     - `RuntimeError` for 503 Database Unavailable


### Api

> Note: for all this tests, the algorithm is mocked to avoid getting errors from it when not testing it, as well as PointSetManager communication module.

- [x] test the `triangulation` endpoint:

    - [x] success case:
     send a valid request with a set of points, check the response contains the correct triangulation and status code 200
    
    - [x] invalid input case:
     send a request with invalid data (like a empty, malformed or inexistant `PointSetID`), and check the response contains the appropriate error message
     - invalid `PointSetID` format, or empty `PointSetID`:
        - code 400 Bad Request
        - body in json containing a internal error code and an error message
    - inexistant `PointSetID`:
        - code 404 Not Found
        - body in json containing a internal error code and an error message

    - [x] algorithm failure case:
     mock the algorithm to raise an exception, send a valid request and check the response contains the appropriate error message
        In that case, the response should be:
        - code 500 Internal Server Error
        - body in json containing a internal error code and an error message THAT DOES NOT REVEAL INTERNAL DETAILS OF THE SERVER (like stack traces, exception messages, etc.)

    - [x] PointSetManager cannot be reached case:
     mock the PointSetManager communication module to raise a `RuntimeError`, send a valid request and check the response contains the appropriate error message
        In that case, the response should be:
        - code 503 Service Unavailable
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