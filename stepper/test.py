import stepper_lib
import sys

def add(a, b):
    stepper_lib.push_env('add', {'a': a, 'b': b, })
    __step_ret = (a + b)
    stepper_lib.pop_env('add', __step_ret)
    return __step_ret

def fact(n):
    stepper_lib.push_env('fact', {'n': n, })
    __step_ret = ((n * fact((n - 1))) if (n > 1) else n)
    stepper_lib.pop_env('fact', __step_ret)
    return __step_ret
a = int(sys.argv[1])
b = int(sys.argv[2])
c = int(sys.argv[3])
print add(a, b)
print fact(c)
stepper_lib.print_state()
