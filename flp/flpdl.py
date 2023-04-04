# -*- coding: utf-8 -*-

"""flpdl - A utility for downloading Feynman's lectures.

requests for downloading the files by sending a GET request.
shutil for writing the files to the hard disk, thus freeing up memory.
argparse for making CLI more accessible.
sys for exiting the app in case of an error.
"""

import requests
import shutil
import argparse
import os

parser = argparse.ArgumentParser()
parser.add_argument("-e", "--ext",
                    help="Choose a file extension for the lectures.",
                    choices=["ogg", "mp4"], default="ogg")
parser.add_argument("-o", "--output-directory",
                    help="Specify a working directory.\
                    Creates flpdl directory in current working directory.")
args = parser.parse_args()

if args.output_directory:
    try:
        os.mkdir(f'{args.output_directory}')
        os.chdir(f'{args.output_directory}')
    except FileExistsError:
        os.chdir(f'{args.output_directory}')

else:
    try:
        os.mkdir(os.path.join(os.curdir, "flp"))
        os.chdir(os.path.join(os.curdir, "flp"))
    except FileExistsError:
        os.chdir(os.path.join(os.curdir, "flp"))


def episodes():
    """Download episodes.

    Helps to download episodes in desired format.
    """
    useragent = "Mozilla/5.0"
    baseurl = "https://www.feynmanlectures.caltech.edu/audio/"
    downloadurl = baseurl + f'{args.ext}' + "/FLP_"
    refererurl = baseurl + "flptapes.html"
    key = {"Referer": refererurl, "User-agent": useragent}
    for urlno in range(1, 4):
        if urlno == 1:
            filecode = ["34A", "41A", "S53A", "RevA", "RevB", "RevC"]
            for fc in filecode:
                url_2 = downloadurl+fc+"_01."+f'{args.ext}'
                filename = url_2.split('/')[-1]
                try:
                    r = requests.get(url_2, headers=key,
                                     timeout=30, stream=True)
                    print("Downloading", filename)
                    with r as filereq:
                        with open(filename, 'wb') as filedl:
                            shutil.copyfileobj(filereq.raw, filedl)
                except r.raise_for_status:
                    return r.status

        elif urlno == 2:
            for i in range(1, 52):
                url_1 = downloadurl+str(i)+"_01."+f'{args.ext}'
                filename = url_1.split('/')[-1]
                try:
                    r = requests.get(url_1, headers=key,
                                     timeout=30, stream=True)
                    with r as filereq:
                        with open(filename, 'wb') as filedl:
                            shutil.copyfileobj(filereq.raw, filedl)

                except r.raise_for_status:
                    pass

        elif urlno == 3:
            for i in (epno for epno in range(1, 65) if epno != 55):
                url_3 = downloadurl+"S"+str(i)+"_01."+f'{args.ext}'
                filename = url_3.split('/')[-1]
                try:
                    r = requests.get(url_3, headers=key,
                                     timeout=30, stream=True)
                    with r as filereq:
                        with open(filename, 'wb') as filedl:
                            shutil.copyfileobj(filereq.raw, filedl)
                except r.raise_for_status:
                    pass


if __name__ == '__main__':
    episodes()
