def func1(a):
    return(a[0] + a[1])

def func2(x):
    return x, x**2

print(func1(func2(3)))
