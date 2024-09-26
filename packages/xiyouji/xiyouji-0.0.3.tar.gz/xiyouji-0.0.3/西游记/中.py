
import sys

from cmd import Cmd

class 猜数字(Cmd):
    intro = "我想了个 100 之内的数，猜猜是几？"
    想的 = 81
    prompt = '请猜吧: '

    def default(self, 行):
        数 = int(行)
        if 数 > self.想的:
            print("太多了!")
        elif 数 < self.想的:
            print("太少了!")
        else:
            print("取到经了!")
            self.do_quit(行)

    def do_quit(self, arg):
        sys.exit()

def 中(args=None):
    游记 = 猜数字()
    游记.cmdloop()

中(sys.argv)