#!/bin/bash
echo "Enter volume ID"
read varname


# Input volume Id will be read and find out the AZ of that volume.
# Use `  or $(command) to run the command and save it in a variable.
avail_zone=`aws ec2 describe-volumes --volume-ids $varname --query 'Volumes[*].[AvailabilityZone]' --output text`

#Ceate an instance  in the same AZ based on the above AZ of the volume.

instance=`aws ec2 run-instances --image-id ami-569ed93c --count 1 --instance-type t1.micro --key-name ec2-backup --placement AvailabilityZone=$avail_zone`

#Sleep until the instance is created.
sleep 20s


#We are using awk command to print the 12th line content (Instance Id) and piping it to sed.
#You can use sed to chop off the beginning double quote, keep what's in between them, and chop off the remaining quote + everything there after.

disp=`echo $instance |  awk '{print $12}' | sed 's/^"\(.*\)".*/\1/'`


echo Instance created: $disp

#attach the volume to the created instance.
aws ec2 attach-volume --volume-id $varname --instance-id $disp --device /dev/sdf

#Display the public DNS name.

pubDNS=`aws ec2 describe-instances --instance-ids $disp --query 'Reservations[*].Instances[*].[PublicDnsName]' --output text`

#echo $pubDNS

#Here we are passing commands to be executed on ec2-instance after ssh. We have got an error to run disklabel. So, we have also given the path of disklabel(which disklabel)
ssh -T -o StrictHostkeyChecking=no root@$pubDNS  'echo $(uname -a); echo $(whoami); echo $(/sbin/disklabel xbd2)' 

#Terminating the Instance.
aws ec2 terminate-instances --instance-ids $disp

