def deploy(url):
    import sys
    import os
    import lib.shutil as shutil
    import upip_utarfile as utarfile
    import urequests

    res = urequests.get(url)

    if not res.status_code == 200:
        return

    def exists(path):
        try:
            os.stat(path)
            return True
        except:
            return False

    t = utarfile.TarFile(fileobj = res.raw)

    for f in t:
        print("Extracting {}: {}".format(f.type, f.name))
        if f.type == utarfile.DIRTYPE:
            if f.name[-1:] == '/':
                name = f.name[:-1]
            else:
                name = f.name

            if not exists(name):
                os.mkdir(name)
        else:
            extracted = t.extractfile(f)

            with open(f.name, "wb") as fobj:
                shutil.copyfileobj(extracted, fobj)

def shutil():
    print("System download > (initial octopus modules)")
    import upip
    print("Installing shutil")
    upip.install("micropython-shutil")
    print("Running deploy")


shutil()
deplUrl="https://octopusengine.org/download/micropython/stable.tar"
deploy(deplUrl)
