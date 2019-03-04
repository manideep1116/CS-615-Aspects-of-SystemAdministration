import subprocess
import time
import json

#Asking for input (to enter volume Id)
vol_Id = input("Enter Volume-ID ")

#Look for az of given volume.
#Here we are writing two functions: so that it will be easier to find errors.
# 1) az_comm() is to store the command.
def az_comm(x):
    return 'aws ec2 describe-volumes --volume-ids ' + x + ' --query "Volumes[*].[AvailabilityZone]" --output text'

'''
2) find_az() is to excute the command through subprocess.
We can also use subprocess.check_output() but the subprocess gives the output in bytes. We need to give the output of this command as input in next subprocess command which requires input as string. So , to get the output from subprocess as string, we are using subprocess.getoutput().
'''
def find_az(y):
    '''Find availability zone'''
    avail_zone = subprocess.getoutput(az_comm(y))
    return avail_zone

#Callig the function with input as volume id and storing it in a variable 'az'.
az = find_az(vol_Id)

#Now again two functions to create instance.
# 1) ins_comm is to store the command.
def ins_comm(i):
    return 'aws ec2 run-instances --image-id ami-569ed93c --count 1 --instance-type t1.micro --key-name ec2-backup --placement AvailabilityZone=' + i

# 2) this command is to execute the command through subprocess. 
def create_ins(ins):
    instance = subprocess.getoutput(ins_comm(ins))
    return instance
#calling the function and storing it in variable 'inst'. It store the information that displays after the instance is created as 'string'.
inst = create_ins(az)

'''
#Now we need the instanceId. So, the output string can be parsed(changing the data structure to store data) to JSON to extract the id easily using json.loads() function. But in python we dont have json. So, we get output in the form of dictionary. In that dictinary we may have list in the values and in that lists we may have dictionaries.So here: 
--> output of inst is string format.
>> type(inst)
<class 'str'>
--> let parsedint = json.loads(inst)
>>type(parsedinst)
<class 'dict'>
 >>parsedinst.keys()
 dict_keys(['Groups', 'Instances', 'OwnerId', 'ReservationId'])
-->now will take the key 'Instances
>>type(parsedinst['Instances'])
<class 'list'>
-->Types of all the keys:
    >> type(parsedinst['Groups'])
    <class 'list'>
    >> type(parsedinst['Instances'])
    <class 'list'>
    >> type(parsedinst['OwnerId'])
    <class 'str'>
    >> type(parsedinst['ReservationId'])
    <class 'str'>
--> Now in Instances list we have one item, which is dictionary.
>> type(parsedinst['Instances'][0])
<class 'dict'>
--> Now will retrieve our required instanceId which is the value of the key 'InstanceID'
> parsedinst['Instances'][0]['InstanceId']
'i-030f31cf7a1b76344'

'''
inst_Id = json.loads(inst)['Instances'][0]['InstanceId']
# will wait till the instance is created.
time.sleep(20)

#now we will write two other functions for attaching the volume to the created instance.
# 1)To store the command.
def attach_comm(a,b):
    return 'aws ec2 attach-volume --volume-id ' +  a +' --instance-id ' + b + ' --device /dev/sdf'

# 2)To execute the command through subprocess.
def attach_vol(c,d):
    attach = subprocess.getoutput(attach_comm(c,d))
    return attach
  
attach_vol(vol_Id, inst_Id)
#time.sleep(60)
 # Now will find the public dns name using our json.loads() function.
 # We can also find this using our aws command: `aws ec2 describe-instances --in    stance-ids 12345 --query 'Reservations[*    ].Instances[*].[PublicDnsName]' --output text`
# Instances-dict[key]
# [0] index number for the list which is the value of Instances
# Publicdnsname is the key name in the dictionary present in the list.
#pubDNS= json.loads(inst)['Instances'][0]['PublicDnsName']
#writing functions to find public dns name
def pub(a):
    return "aws ec2 describe-instances --instance-ids " +a+" --query 'Reservations[*].Instances[*].[PublicDnsName]' --output text"

#2)second function to execute the command through subprocess.
def pub_dns(d):
    pub_d = subprocess.getoutput(pub(d))
    return pub_d

pubDNS= pub_dns(inst_Id)




# Now we are writting two functions to ssh into the instance.
# 1) To store the comman to ssh includind commands to be executed after ssh.
def ssh_comm(dns):
    return "ssh -T -o StrictHostkeyChecking=no root@"+dns+ " ' echo $(uname -a); echo $(whoami); echo $(/sbin/disklabel xbd2)'"

# 2) To execute the command through subprocess.

def ssh(d):
    ssh_into = subprocess.getoutput(ssh_comm(d))
    return ssh_into

# We are printing the output of commands excuted after ssh.
print(ssh(pubDNS))

#Now we write a function to terminate instance.
def terminate(i):
    return subprocess.getoutput('aws ec2 terminate-instances --instance-ids ' + i)

terminate(inst_Id)

