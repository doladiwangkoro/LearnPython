from subprocess import call
from subprocess import Popen, PIPE
from JavadSimpleOPF import main_node

#bot1 = Popen(["gnome-terminal", "-e", "python3", "-i", "play1.py"], stdout=PIPE, stderr=PIPE, stdin=PIPE)
#bot2 = Popen(["gnome-terminal", "-e", "python3", "-i", "play2.py"], stdout=PIPE, stderr=PIPE, stdin=PIPE)

call(['gnome-terminal', '-e', "python3 play1.py"])
call(['gnome-terminal', '-e', "python3 play2.py"])
