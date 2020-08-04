import os


print(os.popen("sh checkSH.sh CSCI+151 | gunzip -c").read())