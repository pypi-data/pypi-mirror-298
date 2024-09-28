from sample_rspymodule._lowlevel import hello, sum_as_string


def pymodule_f(arg: str):
    print("Python module called with arg:", arg)
    result = hello()
    print("End of Python module: ", result)


def miss_pymodule_f(arg: str):
    print("Python module called with arg:", arg)
    hello()
    print("End of Python module: None")


def call_sum_as_stringpy():
    print("Python module called with arg: call_sum_as_stringpy")
    sum_as_string(1,2)
    print("End of Python module: None")
