import glob
import os
import subprocess
from urllib.parse import urljoin
# os.system("rm ./*.png")

files = glob.glob("./*.svg")
path = os.getcwd()  
files = os.listdir(path)  
count = len(files) 
n = count
for name in files:
    baseurl = "https://github.com"
    n = name
    name.replace(".svg", '') #ファイル名を取り除く
    url = urljoin(baseurl, name)
    command = '/usr/bin/curl {url} | awk \'/<svg.+class=\"js-calendar-graph-svg\"/,/svg>/\' | sed -e \'s/<svg/<svg xmlns=\"http:\/\/www.w3.org\/2000\/svg\"/\''
    command = command + " >" + "./" + n
    command = command.format(url=url)
    print(command)
    grass_image = os.system(command)
    grass_image_name = "./" + name
    grass_convert_fname = "--output=" + "./" + name + ".png"
    subprocess.run(["rsvg-convert", "--format=png",  grass_image_name, grass_convert_fname])