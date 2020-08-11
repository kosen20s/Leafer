import glob
import os
import subprocess
from urllib.parse import urljoin
os.system("rm ./*.png")

files = glob.glob("./*.svg")
path = os.getcwd()  
files = os.listdir(path)  
count = len(files) 
n = count
for name in files:
    if name == ("ref.py"):
        continue
    if name == ("*.png"):
        continue
    baseurl = "https://github.com"
    n = name
    name = name.replace(".svg", '') #ファイル名を取り除く
    url = urljoin(baseurl, name)
    command = '/usr/bin/curl {url} | awk \'/<svg.+class=\"js-calendar-graph-svg\"/,/svg>/\' | sed -e \'s/<svg/<svg xmlns=\"http:\/\/www.w3.org\/2000\/svg\"/\''
    command = command + " >" + "./" + n
    command = command.format(url=url)
    print(command)
    grass_image = os.system(command)
    grass_image_name = "./" + n
    grass_convert_fname = "--output=" + "./" + name + ".png"
    print(grass_convert_fname)
    print(grass_image_name)
    subprocess.run(["rsvg-convert", "--format=png",  grass_convert_fname, grass_image_name])
    # os.system("rm ./*.png.png")