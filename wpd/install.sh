#! /bin/bash

if [ $1 = "install" ]
then
   cp ./wp.service /etc/systemd/system/wp.service
   chmod 777 /etc/systemd/system/wp.service

   systemctl daemon-reload
   systemctl start wp.service
   systemctl enable wp.service
   systemctl status wp.service
   echo "service installed"
   echo "Reboot now? Y/N"
   read input
   if [ $input = "y" ]
   then
      reboot
      echo "Rebooting..."
   else
      echo "Install complete"
   fi
elif [ $1 = "start" ]
then
   systemctl start wp.service
   echo "start attempt completed"
elif [ $1 = "stop" ]
then
   systemctl stop wp.service
   echo "stop attempt completed"
elif [ $1 = "status" ]
then
   systemctl status wp.service
fi