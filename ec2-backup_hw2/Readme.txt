This assignment is part of project to build a ec2-backup tool. The ec2-backup(1) tool will eventually perform a backup of the given directory into Amazon Elastic Block Storage (EBS). This will be achieved by creating a volume of the appropriate size, attaching it to an EC2 instance and finally copying the files from the given directory onto this volume.

In this assignment, we will lay the ground work.

1) Input will be given a volume ID.
2) The AZ of this volume will be found.
3) An instance with the mentioned specifications is created in the same az as of volume.
4) Now, the instance will be attached to the given volume.
5) SSH into the instance along with the commands passed to display uname, whoami and disklabel xbd2( usual disk).
6) Then teminate the instance.
