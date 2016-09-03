#!/usr/bin/env python
# -*- coding:utf-8 -*-

#----------------------------------------------------------------------
# Francisco Carrillo Pérez
#----------------------------------------------------------------------

#-------------------------------------------------------------------
#
#  This script is used to change the size of all the images 
#
#-------------------------------------------------------------------

from sys import argv
import subprocess

for i in range(1,180):
	subprocess.call(['convert',"muestra"+str(i)+".png", "-resize","217x185","muestra"+str(i)+".png"])