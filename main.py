import os
from image_match.goldberg import ImageSignature
import shutil
import time
from progress.bar import IncrementalBar
import sys


class GetDuplicateFoto:
    def __init__(self, inpath, topath):
        self.inpath = inpath
        self.topath = topath

    def start(self):
        find_files = []
        gis = ImageSignature()
        for root, dirs, files in os.walk(self.inpath):
            find_files += [os.path.join(root, name) for name in files]
        bar = IncrementalBar('Countdown', max=len(find_files)*2)
        with open(self.topath + "\\log.txt", "w") as file:
            for x in find_files:
                for y in find_files:
                    if x == y:
                        bar.next()
                        time.sleep(1)
                        continue
                    try:
                        a = gis.generate_signature(x)
                        b = gis.generate_signature(y)
                    except:
                        bar.next()
                        time.sleep(1)
                        continue

                    if gis.normalized_distance(a, b) <= 0.22095170140933634:
                        pname = y.replace(self.inpath, "")
                        shutil.move(y, self.topath + pname)
                        file.write(x + ';' + y + '\r\n')
                bar.next()
                time.sleep(1)
        bar.finish()


# ac = GetDuplicateFoto("D:\\foto3", "D:\\foto4")
# ac.start()

if __name__ == "__main__":
    if len(sys.argv) < 3:
        print("Переданы некорректные параметры!")
        sys.exit()

    ac = GetDuplicateFoto(sys.argv[1], sys.argv[2])
    ac.start()
