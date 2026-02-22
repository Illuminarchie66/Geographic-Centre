import numpy as np
C = map.centre3(P, Q, S).cartesian

def recursive(C):
    x = map.centreN([P, Q, S], C).cartesian
    print(x)
    recursive(x)

print(map.centre3(P, Q, S).cartesian)

recursive(map.centre3(P, Q, S).cartesian)
