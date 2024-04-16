import unittest

def throwError(num):
    if (num == 1):
        raise Exeption("Why would you do that")

def fun(num):
    return num / 3

class TestClass(unittest.TestCase):
    #tells the computer that this is just test case
    def test_one(self):
        #checks if two things are equal
        self.assertEquals(fun(1), 1/3)

    def test_two(self):
        #checks if true
        self.assertTrue()
        #checks if false
        self.assertFalse()


    def testRaise(self):
        #
        self.assertRaises(throwError(1))



if __name__ == '__main__':
    unittest.main()