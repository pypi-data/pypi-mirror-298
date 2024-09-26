import pytest


class TestSanitizeFunctionArgs():

    def function(a, b=1, c=2):
        print(locals())
        return

    def function_with_kwargs(a, b=1, c=(1, 2), d={"d": 1}, *my_list, **my_dict):
        print(locals())
        return


if __name__ == "__main__":
    pytest.main([__file__])
