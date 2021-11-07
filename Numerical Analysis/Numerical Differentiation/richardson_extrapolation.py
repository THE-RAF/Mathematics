from copy import deepcopy


class Differentiation:
    @staticmethod
    def differentiation_formula(x, h, func):
        return (func(x + h) - func(x)) / h

    @staticmethod
    def richardson_formula(k, i, fi_list):
        return ((2 ** k) * fi_list[i+1] - fi_list[i]) / (2 ** k - 1)

    @staticmethod
    def differentiate(x, func, h=1, error_order=9):
        diff_formula = lambda h: Differentiation.differentiation_formula(x, h, func)
        richardson_formula = Differentiation.richardson_formula

        fi_list = [diff_formula(h / (2**i)) for i in range(error_order)]
        for k in range(error_order-1, 0, -1):
            fi_list_copy = deepcopy(fi_list)
            fi_list = [richardson_formula(k, i, fi_list_copy) for i in range(k)]

        return fi_list[0]


if __name__ == '__main__':
    def f(x):
        return x**x

    print(Differentiation.differentiate(2, f, h=10, error_order=14))
