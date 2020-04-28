"""
octopusLAB - config class
last update: 8.12.2019

config (all) and config_data (for selected keys)
set / get / 

from config import Config
keys = ["tempMax","tempMin"]
conf = Config("your_file", keys) > config/your_file.json
conf.setup()

conf.create_from_query("a=1&b=2")
conf.set("c",3)
conf.save()

ampy -p /COM6 put ./config/__init__.py config/__init__.py
"""

class Conf:
    TW = 50

from util.octopus import printTitle
import ujson
from ucollections import OrderedDict

# convert query "a=1&b=2" to dict {'a': '1', 'b': '2'}
# test: q = ("a=1&b=2&x3=3&y5=5&z7=7")
def query2dict(q):
    d = dict([v.split("=", 1) for v in q.split("&") if "=" in v])
    # d = OrderedDict(d)
    return d


class Config():
    def __init__(self, name="test", keys = ["version","default_null_test"], conf_data = [["config version", "version"], ["NULL Test", "default_null_test"]]):
        self.file = "config/" + name + ".json"
        self.keys = keys
        self.conf_data = conf_data

        try:
            with open(self.file, 'r') as f:
                d = f.read()
                f.close()
                self.config = ujson.loads(d)
        except OSError:
            # FileNotFound
            self.config = {}

    def get(self, key):
        return self.config.get(key)


    def set(self, key, value):
        self.config[key] = value


    def save(self, ordered = False):
        # dump updated setting into json
        print("Writing new config item to file %s" % self.file)
        with open(self.file, 'w') as f:
            if ordered:
                ujson.dump(self.config, f)
            else:
                ujson.dump(OrderedDict(self.config), f)


    def create_from_query(self,q):
        self.config = query2dict(q)
        print(self.config)


    def setup(self):
        while True:
            print()
            print('=' * Conf.TW)
            print('        S E T U P - ' + self.file)
            print('=' * Conf.TW)
            # show options with current values
            c = 0
            for i in self.keys:
                c += 1
                print("[%2d] - %16s - %s" % (c, i, self.config[i] if i in self.config else ""))

            print("[ x] - Exit from json setup")

            print('=' * Conf.TW)
            sele = input("select: ")

            if sele == "x":
                # done with editing
                break

            try:
                sele = int(sele)
            except ValueError:
                print("Invalid input, try again.")

            # change selected item if integer
            if sele > 0 and sele <= len(self.keys):
                # print attribute name and description
                print()
                # print current value
                try:
                    # new_val = int(input("New Value: "))
                    new_val = input("New Value: ")
                    try:
                        new_val = int(new_val)
                    except:
                        pass
                except ValueError:
                    # if invalid input, 0 is inserted
                    new_val = 0

                # update config object
                print(self.keys[sele-1] + "->" + str(new_val))
                self.config[self.keys[sele-1]] = new_val
                self.save()
            else:
                print("Invalid input, try again.")


    def print(self): # list_for_keys
        print()
        print('=' * Conf.TW)
        for ix in self.conf_data:
            try:
                print(" %25s - %s " % (ix[0], self.config[ix[1]] ))
            except:
                Err_print_config = True
        print('=' * Conf.TW)


    def print_all(self):
        print()
        print('-' * Conf.TW)
        for ix in self.config:
            try:
                # print(ix, cc[ix]) # dict{}
                print(" %25s - %s " % (ix, self.config[ix]))
            except:
                Err_print_config = True
        print('-' * Conf.TW)


    def __str__(self):
        printTitle(self.file)
        print(self.config)
        print("Keys: ")
        print(self.keys)
        self.print_all()
        print(".create_from_query(q) | .save()")
        print(".get(k) | .set(k,v) | .setup()")
        print(".list_all() | .list_for_keys()")
