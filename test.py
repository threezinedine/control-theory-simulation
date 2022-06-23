def test(a, b, *args, **kwargs):
    print(kwargs)
    print(args)
    print(kwargs['count'])
    return a + b


test(3, 4, 5, 6, 7, time=3, count="Hello")

