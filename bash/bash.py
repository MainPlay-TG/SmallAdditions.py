from subprocess import Popen
from sys import argv,stdin,exit
exit(Popen(["busybox","bash"]+argv[1:],stdin=stdin).wait())