# Copyright (c) Monotrix 2021-
# Has no dependencies except for binutils for DEB extraction

import os
import json
import sys
import time

if __name__ == "__main__":
    def help():
        print("Usage: python3 ./dpkg-scanpackages.py ./debs --create-archive=YES")
    if len(sys.argv) == 1:
        help()
        exit()
    archive = "no"
    if len(sys.argv) == 3:
        if (sys.argv[2]) == "--create-archive=YES":
            archive = "yes"
        elif (sys.argv[2]) != "--create-archive=YES":
            print("Unknown argument.")
            help()
            exit()
    dir = sys.argv[1] + "/"
    files = os.listdir(dir)
    def add(file):
        os.system('mkdir ./tmp; ar x ' + dir + file + '; mv ./control.tar.gz ./tmp; rm -rf data.tar.gz data.tar.lzma debian-binary; cd ./tmp; tar xvf ./control.tar.gz')
        sums = {
            "sha256": os.popen("shasum -a 256 " + dir + file + " | cut -d \" \" -f 1").read(),
            "sha1": os.popen("shasum -a 1 " + dir + file + " | cut -d \" \" -f 1").read(),
            "md5": os.popen("md5 " + dir + file + " | cut -d \" \" -f 4").read(),
            "size": os.stat(dir + file).st_size
        }
        sha256 = "SHA256: " + str(sums["sha256"])
        sha1 = "SHA1: " + str(sums["sha1"])
        md5 = "MD5sum: " + str(sums["md5"])
        filesize = "Size: " + str(sums["size"])
        filename = "Filename: " + dir + file
        control = open("./tmp/control", "r").read()
        output = control + filename + "\n" + md5 + sha1 + sha256 + filesize + "\n" + "\n"
        print(sha256, md5, sha1, filesize)
        f = open("./Packages", "a")
        f.write(output)
        f.close()
        os.system('rm -rf ./tmp')
    start_time = time.time()
    for file in files:
        add(file)
    if (archive) == "yes":
        os.system("echo \"[DSP] BUILDING BZ2\"; bzip2 -5fkv ./Packages > ./Packages.bz2; echo \"[DSP] BUILDING XZ\"; xz -5fkev Packages > Packages.xz; echo \"[DSP] BUILDING LZMA\"; xz -5fkev --format=lzma Packages > Packages.lzma")
    print("Finished in %s seconds." % (time.time() - start_time))

