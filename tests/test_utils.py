class FunctorTest():
    @staticmethod
    def test(test, functor, input, expected):
        test.assertEqual(expected, functor(input))