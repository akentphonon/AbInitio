#!/usr/bin/env python

# this script extracts the atomic displacements from
# the DISP file generated by Phon,
# and creates POSCAR files for corresponding displacements

from p4vasp.SystemPM import *
from p4vasp.Structure import Structure
#run=XMLSystemPM('vasprun.xml')
#struct=run.FINAL_STRUCTURE

struct = Structure("POSCAR")

dispfile=open("DISP",'r')
runfile=open("runhf", 'w')

runfile.write("#!/bin/bash \n")
runfile.write("VASP='vasp' \n\n")

disp=[]
pos=[]

pos.append(struct)
pos[len(pos)-1].write('pos'+repr(len(pos)-1))

for line in dispfile:
  str=eval(line)
  liststr=str.split()
  listnum=[]
  for item in liststr:
    listnum.append(eval(item))
  disp.append(listnum)
  atomindex=listnum[0]
  atomdisp=listnum[-3:]
  pos.append(struct)
  print "Length of positions file list:", len(pos) 
  pos[len(pos)-1].positions[atomindex-1]=pos[len(pos)-1].positions[atomindex-1]+Vector(atomdisp)
  print "Writing pos file ", len(pos)-1
  pos[len(pos)-1].write('pos'+repr(len(pos)-1), newformat=0)
  # !!! struct must be some kind of reference and copying it (appending) to pos[]
  #     only adds another reference to it... so we have to undo mods as we go !!!
  pos[len(pos)-1].positions[atomindex-1]=pos[len(pos)-1].positions[atomindex-1]-Vector(atomdisp)

  runfile.write("cp pos"+repr(len(pos)-1)+" POSCAR \n")
  runfile.write("$VASP >>out.vasp 2>>err.vasp & \n")
  runfile.write("wait \n")
  runfile.write("cp OUTCAR out_"+repr(len(pos)-1)+" \n\n")
  runfile.write("cp CHGCAR CHGCAR_"+repr(len(pos)-1)+" \n\n")
  runfile.write("cp vasprun.xml vasprun.xml_"+repr(len(pos)-1)+" \n\n")

dispfile.close()
runfile.close()
