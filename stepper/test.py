import stepper_lib
import sys

def add(a, b):
    stepper_lib.push_call('add', {'a': a, 'b': b, })
    __step_ret = (a + b)
    stepper_lib.pop_call('add', __step_ret)
    return __step_ret
stepper_lib.store_env('add')

def fact(n):
    stepper_lib.push_call('fact', {'n': n, })
    __step_ret = ((n * fact((n - 1))) if (n > 1) else n)
    stepper_lib.pop_call('fact', __step_ret)
    return __step_ret
stepper_lib.store_env('fact')

def add2(a):
    stepper_lib.push_call('add2', {'a': a, })

    def finish_add(b):
        stepper_lib.push_call('finish_add', {'b': b, })
        __step_ret = (a + b)
        stepper_lib.pop_call('finish_add', __step_ret)
        return __step_ret
    stepper_lib.store_env('finish_add')
    __step_ret = finish_add
    stepper_lib.pop_call('add2', __step_ret)
    return __step_ret
stepper_lib.store_env('add2')

def mymax(a, b):
    stepper_lib.push_call('mymax', {'a': a, 'b': b, })
    if (a > b):
        __step_ret = a
        stepper_lib.pop_call('mymax', __step_ret)
        return __step_ret
    else:
        __step_ret = b
        stepper_lib.pop_call('mymax', __step_ret)
        return __step_ret
stepper_lib.store_env('mymax')
a = int(sys.argv[1])
b = int(sys.argv[2])
c = int(sys.argv[3])
print add(a, b)
print fact(c)
print add2(a)(b)
print mymax(a, b)
stepper_lib.print_call_history()
