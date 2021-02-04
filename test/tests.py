import unittest
import main

class parseArgsTests(unittest.TestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test1(self):
        res = main.parseArgs('-t')
        args, text = res
        assert 't' in args and args['t'] == True and text == '', res

    def test2(self):
        res = main.parseArgs('-t ')
        args, text = res
        assert 't' in args and args['t'] == True and text == '', res

    def test3(self):
        res = main.parseArgs('-t -r -s')
        args, text = res
        assert (
            't' in args and args['t'] == True and
            'r' in args and args['r'] == True and
            's' in args and args['s'] == True and
            text == ''
            ), res

    def test4(self):
        res = main.parseArgs('-t asd')
        args, text = res
        assert 't' in args and args['t'] == True and text == 'asd', res

    def test5(self):
        res = main.parseArgs('-t=a -r=asd')
        args, text = res
        assert (
            't' in args and args['t'] == 'a' and
            'r' in args and args['r'] == 'asd' and
            text == ''
            ), res

    def test6(self):
        res = main.parseArgs('-t=asd text')
        args, text = res
        assert 't' in args and args['t'] == 'asd' and text == 'text', res




if __name__ == '__main__':
    unittest.main()
