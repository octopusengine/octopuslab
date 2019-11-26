"""
octopusLAB - config class
last update: 3.11.2019

from config import Config
keys = ["tempMax","tempMin"]
conf = Config("your_file", keys) > config/your_file.json
conf.setup()

ampy -p /COM6 put ./config/__init__.py config/__init__.py
"""

from util.octopus import printTitle
import ujson


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

    def set(setlf, key, value):
        self.config[key] = value

    def save(self):
        # dump updated setting into json
        print("Writing new config item to file %s" % self.file)
        with open(self.file, 'w') as f:
            ujson.dump(self.config, f)

    def setup(self):
        while True:
            print()
            print('=' * 50)
            print('        S E T U P - ' + self.file)
            print('=' * 50)
            # show options with current values
            c = 0
            for i in self.keys:
                c += 1
                # print("[%2d] - %8s [%s] - %s" % (c, i['attr'], io_conf.get(i['attr'], 0), i['descr']))
                try:
                    print("[%2d] - %16s - %s" % (c, i, self.config[i]))
                except:
                    this_key_in_json = False
            print("[ x] - Exit from json setup")

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
                    # new_val = int(input("New Value: "))
                    new_val = input("New Value: ")
                    try:
                        new_val = int(new_val)
                    except:
                        new_val_it_int = False
                except ValueError:
                    # if invalid input, 0 is inserted
                    new_val = 0

                # update config object
                print(self.keys[sele-1] + "->" + str(new_val))
                self.config[self.keys[sele-1]] = new_val
                self.save()
            else:
                print("Invalid input, try again.")


    def print(self):
        print()
        print('=' * 39)
        for ix in self.conf_data:
            try:
                # print(ix, cc[ix]) # dict{}
                print(" %25s - %s " % (ix[0], self.config[ix[1]] ))
            except:
                Err_print_config = True
        print('=' * 39)
