-->To execute unix commands in Python we have package called "os".
--> By importing os we can use statements like "system" to execute commands.
Ex: os.system("ls -s")
--> We have package called "subprocess" which replaces "os".
Ex: subprocess.call("ls", shell=True)
  -->By using subprocess, we can communicate with shell from our python script. It basically executes the commands on shell and will get output from our python script.
  --> In the above example, it is calling "ls" commmand. "shell = True" means it is doing everything in the shell.
--> To store the output in a variable using subprocess.
Ex: output = subprocess.check_output("ls", shell=True)
  (this gives output as bytes)
--> We have subprocess.getoutput(cmd) to give output as string.
--> we have json.loads() to parse the string type to dictionary in python.
