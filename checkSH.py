import os

if __name__ == "__main__":
  while True:
    print(os.popen("sh checkSH.sh CSCI+151").read())
    print()
