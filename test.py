import sys
import time


class Test(object):
    def __init__(self):
        True

    def test(self, arr, default=True, test1=False):
        print default
        print test1
        print arr
        if(test1):
            print "yiipppeee"
        print "testing"

    def main(self):
        arg = "test"
        args = "test1=True,default=False"
        arr = ["hello"]
        eval("self."+arg+"("+str(arr)+","+args+")") 

       
if __name__ == "__main__":
    testclass = Test()
    testclass.main()
    #getattr(testclass, "test")("default=False","test1=True")

