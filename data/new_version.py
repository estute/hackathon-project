class Foo(object):

    def bar(self, x, y=10):
        """
        comment
        """
        return x + y

    def baz(self):
        """
        comment
        """
        return 42


def funky():
    return "Hello world"



def main():

    f = Foo()
    funk()


if __name__ == "__main__":
    main()
