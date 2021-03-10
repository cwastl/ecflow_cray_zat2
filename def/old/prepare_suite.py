#!/usr/bin/env python3

import os

suite = "claef"
runs = ["00","06","12","18"]
famil = ["lbc","obs","main"]
members = ["00", "01","02","03","04","05","06","07","08","09","10","11","12","13","14","15","16"]
tasks_operator = ["switch_sthost","switch_schost"]
tasks_comp = ["complete"]
tasks_ez_trigger = ["dummy1"]
tasks_check_lbc = ["dummy2"]
tasks_check_obs = ["dummy2"]
tasks_check_main = ["dummy2"]
tasks_clean = ["cleaning"]
tasks_mirror = ["mirror"]
tasks_lbc = ["getlbc","divlbc","901","getlbc_gl","gl"]
tasks_obs = ["getobs","bator","bator3D"]
tasks_main = ["927","pgd","927surf","sstex","addsurf","screen", "screensurf","canari","minim","001","progrid","addgrib","transfer","archmars"]

hpath="/home/ms/at/zat2/ecf/"

if not os.path.exists(hpath + suite):
    os.mkdir(hpath + suite)

os.chdir(hpath + suite)

if not os.path.exists("operator"):
         os.mkdir("operator")  

for t in tasks_operator:

    if not os.path.lexists("operator/" + t + ".ecf"):
        os.symlink(hpath + "scripts/" + t + ".ecf", "operator/" + t + ".ecf")

for t in tasks_comp:

    if not os.path.lexists(t + ".ecf"):
        os.symlink(hpath + "scripts/" + t + ".ecf", t + ".ecf")

for r in runs:

     if not os.path.exists("RUN_" + r):
         os.mkdir("RUN_" + r)  

     if not os.path.exists("RUN_" + r + "/dummy"):
         os.mkdir("RUN_" + r + "/dummy")  

     for s in tasks_dummy:

         if not os.path.lexists("RUN_" + r + "/dummy/" + s + ".ecf"):
             os.symlink(hpath + "scripts/" + s + ".ecf", "RUN_" + r + "/dummy/" + s + ".ecf")

     for t in tasks_clean:

         if not os.path.lexists("RUN_" + r + "/" + t + ".ecf"):
             os.symlink(hpath + "scripts/" + t + ".ecf", "RUN_" + r + "/" + t + ".ecf")

     for f in famil:

          if not os.path.exists("RUN_" + r + "/" + f):
              os.mkdir("RUN_" + r + "/" + f)

          if f == "lbc":

             if not os.path.exists("RUN_" + r + "/" + f):
                os.mkdir("RUN_" + r + "/" + f)                     

             for t in tasks_lbc:

                if t == "getlbc":
                  
                   if not os.path.lexists("RUN_" + r + "/" + f + "/" + t + ".ecf"):
                        os.symlink(hpath + "scripts/" + t + ".ecf", "RUN_" + r + "/" + f + "/" + t + ".ecf")

                else:

                  for m in members:

                     if not os.path.exists("RUN_" + r + "/" + f + "/MEM_" + m):
                        os.mkdir("RUN_" + r + "/" + f + "/MEM_" + m)                     

                     if not os.path.lexists("RUN_" + r + "/" + f + "/MEM_" + m + "/" + t + ".ecf"):
                        os.symlink(hpath + "scripts/" + t + ".ecf", "RUN_" + r + "/" + f + "/MEM_" + m + "/" + t + ".ecf")

          if f == "obs":

             for t in tasks_obs:

                 if not os.path.lexists("RUN_" + r + "/" + f + "/" + t + ".ecf"):
                     os.symlink(hpath + "scripts/" + t + ".ecf", "RUN_" + r + "/" + f + "/" + t + ".ecf")

          if f == "main":

             for m in members:

                 if not os.path.exists("RUN_" + r + "/" + f + "/MEM_" + m):
                     os.mkdir("RUN_" + r + "/" + f + "/MEM_" + m)

                 for t in tasks_main:
 
                     if not os.path.lexists("RUN_" + r + "/" + f + "/MEM_" + m + "/" + t + ".ecf"):
                        os.symlink(hpath + "scripts/" + t + ".ecf", "RUN_" + r + "/" + f + "/MEM_" + m + "/" + t + ".ecf")

     for t in tasks_mirror:

         if not os.path.lexists("RUN_" + r + "/" + t + ".ecf"):
             os.symlink(hpath + "scripts/" + t + ".ecf", "RUN_" + r + "/" + t + ".ecf")
   




