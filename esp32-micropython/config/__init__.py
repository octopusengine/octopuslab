"""
octopusLAB - config class
from config import Config
conf = Config("your_file") > config/your_file.json
conf.setup()
"""

from util.octopus import printTitle
import ujson


class Config():
    def __init__(self, name="test"):
        self.file = "config/" + name + ".json"

        try:
            with open(self.file, 'r') as f:
                d = f.read()
                f.close()
                self.config = ujson.loads(d)
        except OSError:
            # FileNotFound
            self.config = {}


    def setup(self):
        while True:
            print()
            print('=' * 50)
            print('        S E T U P - ' + self.file)
            print('=' * 50)
            # show options with current values
            c = 0
            for i in self.config:
                c += 1
                # print("[%2d] - %8s [%s] - %s" % (c, i['attr'], io_conf.get(i['attr'], 0), i['descr']))
                # print("[%2d] - %8s - %s" % (c, i[0], i[1]))
                print(c, i)
            print("[x]  - Exit from json setup")

            print('=' * 50)
            sele = input("select: ")

            if sele == "x":
                # done with editing
                break

            try:
                sele = int(sele)
            except ValueError:
                print("Invalid input, try again.")

            # change selected item if integer
            if sele > 0 and sele <= len(self.config):
                # print attribute name and description
                print()
                # print current value
                try:
                    #new_val = int(input("New Value [%s]: " % io_conf.get(io_menu_layout[sele - 1]['attr'], 0)))
                    new_val = int(input("New Value: "))
                except ValueError:
                    # if invalid input, 0 is inserted
                    new_val = 0
                # update config object
                print(new_val)
                # dump updated setting into json
                ## print("Writing new config to file %s" % io_conf_file)
                ## with open(io_conf_file, 'w') as f:
                ##    ujson.dump(io_conf, f)
            else:
                print("Invalid input, try again.")
