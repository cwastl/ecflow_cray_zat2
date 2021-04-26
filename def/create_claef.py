#!/usr/bin/env python3
#
#CREATE C-LAEF SUITE DEFINITION FILE
#
#OUTPUT: claef.def and *.job0 - task files
#
#CREATED: 2019-01-14
#
#AUTHOR: C. Wastl
###########################################################

#load modules
import os
from ecflow import *
import datetime

# get current date
now = datetime.datetime.now()

# ecFlow home and include paths
home = os.path.join(os.getenv("HOME"),"ecf");
incl = os.path.join(os.getenv("HOME"),"ecf/include");

# to submit jobs remotely
schedule = "/usr/local/apps/schedule/1.4/bin/schedule";

################################
### top level suite settings ###
################################

#suite name
suite_name = "claef"

#ensemble members
#members = [0,1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16]
members = [0,1,2,3]

# forecasting range
fcst = 48

# forecasting range control member
fcstctl = 48

# coupling frequency
couplf = 3

# use 15min output for precipitation
step15 = False

# assimilation switches
assimi = True   #assimilation yes/no
assimm = 0      #number of members without 3DVar
assimc = 6      #assimilation cycle in hours
eda = True      #ensemble data assimilation
seda = True     #surface eda

# use EnJK method of Endy yes/no
enjk = True

# use stochastic physics model error representation yes/no
stophy = True

# block transfer to speed up
blocks = 6             #block size

#transfer Files to ZAMG
trans = False

#archive Files to MARS
arch = False

# SBU account, cluster and user name, logport
account = "ata01";
schost  = "cca";
sthost  = "sc1";
user    = "zat2";
logport = 38776;

# main runs time schedule
timing = {
  'comp' : '23:30',
  'clean' : '05:00',
  'o00_1' : '0155',
  'o00_2' : '0205',
  'o06_1' : '0755',
  'o06_2' : '0805',
  'o12_1' : '1355',
  'o12_2' : '1405',
  'o18_1' : '1955',
  'o18_2' : '2005',
  'c00_1' : '02:30',
  'c00_2' : '10:15',
  'c06_1' : '08:30',
  'c06_2' : '11:15',
  'c12_1' : '14:30',
  'c12_2' : '17:15',
  'c18_1' : '20:30',
  'c18_2' : '23:15',
}

# debug mode (1 - yes, 0 - no)
debug = 0;

anzmem = len(members)

# date to start the suite
start_date = int(now.strftime('%Y%m%d'))
#start_date = 20190415
end_date = 20221231

###########################################
#####define Families and Tasks#############
###########################################

def family_operator():

   return Family("operator", 

      [
         Task("switch_schost",
             Edit(
                ECF_JOBOUT="%ECF_HOME%/ecf_out/ecf.out",
                ECF_JOB_CMD="{} {} ecgb %ECF_JOB% %ECF_JOBOUT%".format(schedule, user),
                NAME="switch_sc",
             ),
             Label("info", ""),
             Defstatus("suspended"),
          )
      ],

      [
         Task("switch_sthost",
             Edit(
                ECF_JOBOUT="%ECF_HOME%/ecf_out/ecf.out",
                ECF_JOB_CMD="{} {} ecgb %ECF_JOB% %ECF_JOBOUT%".format(schedule, user),
                NAME="switch_st",
             ),
             Label("info", ""),
             Defstatus("suspended"),
          )
       ],
    )

def family_dummy(startc1,startc2):

    # Family dummy
    return Family("dummy",

       # Family ez_trigger
       [
         Family("ez_trigger",

            # Task dummy1
            [
               Task("dummy1",
                  Edit(
                     NP=1,
                     CLASS='ts',
                     NAME="dummy1",
                  ),
                  Label("run", ""),
                  Label("info", ""),
                  Defstatus("suspended"),
               )
            ]
         )
       ],

       # Family check_obs
       [
         Family("check_obs",

            # Task dummy2
            [
               Task("dummy2",
                  Complete("../../obs == complete"),
                  Edit(
                     NP=1,
                     CLASS='ts',
                     NAME="dummy2",
                  ),
                  Label("run", ""),
                  Label("error", ""),
                  Time(startc1),
               )
            ]
         )
       ],

       # Family check_main
       [
         Family("check_main",

            # Task dummy2
            [
               Task("dummy2",
                  Complete("../../main == complete"),
                  Edit(
                     NP=1,
                     CLASS='ts',
                     NAME="dummy2",
                  ),
                  Label("run", ""),
                  Label("error", ""),
                  Time(startc2),
               )
            ]
         )
       ]
    )

def family_cleaning():

   return Task("cleaning",
             Trigger("dummy/ez_trigger/dummy1 == complete"),
             Edit(
                NP=1,
                CLASS='ts',
                NAME="cleaning",
                ANZMEMB=anzmem,
             ),
             Label("run", ""),
             Label("info", ""),

          )

def family_mirror():

   return Task("mirror",
             Trigger("main == complete"),
             Edit(
                NP=1,
                CLASS='ts',
                NAME="mirror",
                ANZMEMB=anzmem,
             ),
             Label("run", ""),
             Label("info", ""),

          )

def family_obs(starto1,starto2) :

    # Family OBS
    return Family("obs",

       Edit(ASSIM=assimi),

       # Task assim/getobs
       [
          Task("getobs",
             Trigger(":ASSIM == 1 and /claef:TIME > {} and /claef:TIME < {}".format(starto1,starto2)),
             Complete(":ASSIM == 0"),
             Meter("obsprog", -1, 3, 3),
             Edit(
                NP=1,
                CLASS='ts',
                NAME="getobs",
             ),
             Label("run", ""),
             Label("info", ""),
          )
       ],

       # Task assim/pregps
       [
          Task("pregps",
             Trigger(":ASSIM == 1 and getobs == complete"),
             Complete(":ASSIM == 1 and getobs:obsprog == 0 or :ASSIM == 0"),
             Edit(
                NP=1,
                CLASS='ts',
                NAME="pregps",
             ),
             Label("run", ""),
             Label("info", ""),
             Label("error", "")
          )
       ],

       # Task assim/bator
       [
          Task("bator",
             Trigger(":ASSIM == 1 and getobs == complete"),
             Complete(":ASSIM == 1 and getobs:obsprog == 0 or :ASSIM == 0"),
             Edit(
                NP=1,
                CLASS='ts',
                NAME="bator",
             ),
             Label("run", ""),
             Label("info", ""),
             Label("error", "")
          )
       ],

       # Task assim/bator3D
       [
          Task("bator3D",
             Trigger(":ASSIM == 1 and pregps == complete"),
             Complete(":ASSIM == 1 and getobs:obsprog == 0 or :ASSIM == 0"),
             Edit(
                NP=1,
                CLASS='ts',
                NAME="bator3D",
             ),
             Label("run", ""),
             Label("info", ""),
          )
       ],
    )

def family_main():

   # Family MAIN
   return Family("main",

      Edit(
         ASSIM=assimi,
         LEADT=fcst,
         SEDA=seda,
         ARCHIV=arch,
         TRANSF=trans),

      # Family MEMBER
      [
         Family("MEM_{:02d}".format(mem),

            # Task 927atm
            [
               Task("927",
                  Trigger("../../dummy/ez_trigger/dummy1 == complete"),
                  Event("d"),
                  Edit(
                     MEMBER="{:02d}".format(mem),
                     NP=16,
                     CLASS='tf',
                     NAME="927_{:02d}".format(mem),
                  ),
                  Label("run", ""),
                  Label("info", ""),
               )
            ],

            # Task 927/surf
            [
               Task("927surf",
                  Trigger("../../dummy/ez_trigger/dummy1 == complete"),
#                  Trigger("pgd == complete"),
                  Edit(
                     MEMBER="{:02d}".format(mem),
                     NP=1,
                     CLASS='tf',
                     NAME="927surf{:02d}".format(mem),
                  ),
                  Label("run", ""),
                  Label("info", ""),
                  Label("error", ""),
               )
            ],

            # Task assim/sstex
            [
               Task("sstex",
                  Trigger(":ASSIM == 1 and ../MEM_{:02d}/927:d".format(mem)),
                  Complete(":ASSIM == 1 and ../../obs/getobs:obsprog == 0 or :ASSIM == 0"),
                  Edit(
                     MEMBER="{:02d}".format(mem),
                     NP=1,
                     CLASS='ts',
                     NAME="sstex{:02d}".format(mem),
                  ),
                  Label("run", ""),
                  Label("info", ""),
               )
            ],

            # Task assim/addsurf
            [
               Task("addsurf",
                  Trigger(":ASSIM == 1 and sstex == complete"),
                  Complete(":ASSIM == 1 and ../../obs/getobs:obsprog == 0 or :ASSIM == 0"),
                  Edit(
                     MEMBER="{:02d}".format(mem),
                     NP=1,
                     CLASS='ts',
                     NAME="addsurf{:02d}".format(mem),
                  ),
                  Label("run", ""),
                  Label("info", ""),
               )
            ],

            # Task assim/screening 3D
            [
               Task("screen",
                  Trigger(":ASSIM == 1 and addsurf == complete and ../../obs/bator3D == complete"),
                  Complete(":ASSIM == 1 and ../../obs/getobs:obsprog == 0 or :ASSIM == 0"),
                  Edit(
                     MEMBER="{:02d}".format(mem),
                     NP=36,
                     CLASS='tp',
                     EDA=eda,
                     NAME="screen{:02d}".format(mem),
                  ),
                  Label("run", ""),
                  Label("info", ""),
                  Label("error", "")
               )
            ],

            # Task assim/screening surface
            [
               Task("screensurf",
                  Trigger(":ASSIM == 1 and addsurf == complete and ../../obs/bator == complete"),
                  Complete(":ASSIM == 1 and ../../obs/getobs:obsprog == 0 or :ASSIM == 0"),
                  Edit(
                     MEMBER="{:02d}".format(mem),
                     NP=1,
                     CLASS='tp',
                     NAME="screensurf{:02d}".format(mem),
                  ),
                  Label("run", ""),
                  Label("info", ""),
                  Label("error", "")
               )
            ],

            # Task assim/canari
            [
               Task("canari",
                  Trigger(":ASSIM == 1 and screensurf == complete"),
                  Complete(":ASSIM == 1 and ../../obs/getobs:obsprog == 0 or :ASSIM == 0"),
                  Edit(
                     MEMBER="{:02d}".format(mem),
                     NP=1,
                     CLASS='ts',
                     SEDA=seda,
                     NAME="canari{:02d}".format(mem),
                  ),
                  Label("run", ""),
                  Label("info", ""),
               )
            ],

            # Task assim/minimization
            [
               Task("minim",
                  Trigger(":ASSIM == 1 and screen == complete"),
                  Complete(":ASSIM == 1 and ../../obs/getobs:obsprog == 0 or :ASSIM == 0"),
                  Edit(
                     MEMBER="{:02d}".format(mem),
                     NP=36,
                     CLASS='tp',
                     ASSIMM=assimm,
                     ENSJK=enjk,
                     NAME="minim{:02d}".format(mem),
                  ),
                  Label("run", ""),
                  Label("info", ""),
               )
            ],

            # Task 001
            [
               Task("001",
                  Trigger("927 == complete and minim == complete and canari == complete"),
                  Event("e"),
                  Edit(
                     MEMBER="{:02d}".format(mem),
                     NP=360,
                     CLASS='tp',
                     STOCH=stophy,
                     STEPS15=step15,
                     NAME="001_{:02d}".format(mem),
                  ),
                  Label("run", ""),
                  Label("info", ""),
                  Label("error", "")
               )
            ],

            # Task PROGRID
            [
               Task("progrid",
                  Trigger("../MEM_{:02d}/001:e".format(mem)),
                  Complete(":LEAD < :LEADT"),
                  Event("f"),
                  Edit(
                     MEMBER="{:02d}".format(mem),
                     NP=1,
                     CLASS='tf',
                     STEPS15=step15,
                     NAME="progrid{:02d}".format(mem),
                  ),
                  Label("run", ""),
                  Label("info", ""),
                  Label("error", "")
               )
            ],

            # Task ADDGRIB
            [
               Task("addgrib",
                  Trigger("../MEM_{:02d}/progrid:f".format(mem)),
                  Complete(":LEAD < :LEADT"),
                  Event("g"),
                  Edit(
                     MEMBER="{:02d}".format(mem),
                     NP=1,
                     CLASS='tf',
                     STEPS15=step15,
                     NAME="addgrib{:02d}".format(mem),
                     BLOCKS=blocks,
                  ),
                  Label("run", ""),
                  Label("info", ""),
                  Label("error", ""),
               )
            ],

            # Task verif
            [
               Task("verif",
                  Time("10:00"),
                  Complete(":LEAD < :LEADT or :MEMBER == 01 or :MEMBER == 02 or :MEMBER == 03"),
                  Edit(
                     MEMBER="{:02d}".format(mem),
                     NP=1,
                     CLASS='ns',
                     NAME="verif{:02d}".format(mem),
                  ),
                  Label("run", ""),
                  Label("info", ""),
               )
            ],

            # Task Transfer 
            [
               Task("transfer",
                  Trigger(":TRANSF == 1 and ../MEM_{:02d}/addgrib:g".format(mem)),
                  Complete(":LEAD < :LEADT or :TRANSF == 0"),
                  Edit(
                     MEMBER="{:02d}".format(mem),
                     NP=1,
                     CLASS='ts',
                     STEPS15=step15,
                     NAME="transfer{:02d}".format(mem),
                     BLOCKS=blocks,
                  ),
                  Label("run", ""),
                  Label("info", ""),
                  Label("error", ""),
               )
            ],

            # Task MARS Archiv 
            [
               Task("archmars",
                  Trigger(":ARCHIV == 1 and transfer == complete"),
                  Complete(":LEAD < :LEADT or :ARCHIV == 0"),
                  Edit(
                     MEMBER="{:02d}".format(mem),
                     NP=1,
                     CLASS='ts',
                     NAME="archmars{:02d}".format(mem),
                     ANZMEMB=anzmem,
                  ),
                  Label("run", ""),
                  Label("info", ""),
               )
            ],

           ) for mem in members
         ]
       )

###########################
### create C-LAEF suite ###
###########################

print("\n=> creating suite definition\n");

defs = Defs().add(

          # Suite C-LAEF
          Suite(suite_name).add(

             Edit(
                # ecflow configuration
                ECF_MICRO='%',         # ecf micro-character
                ECF_EXTN='.ecf',        # ecf files extension
                ECF_HOME=home,         # ecf root path
                ECF_INCLUDE=incl,      # ecf include path
                ECF_TRIES=1,           # number of reruns if task aborts

                # suite configuration variables
                STHOST=sthost,
                SCHOST=schost,
                USER=user,
                ACCOUNT=account,
                CNF_DEBUG=debug,

                # suite variables
                KOPPLUNG=couplf,
                ASSIMC=assimc,
 
                # Running jobs remotely on HPCF
                ECF_OUT ='/%STHOST%/tcwork/' + user + '/sb/CLAEF', # jobs output dir on remote host
                ECF_LOGHOST='%SCHOST%-log',                     # remote log host
                ECF_LOGPORT=logport,                  # remote log port

                # Submit job (remotely)
                ECF_JOB_CMD="{} {} %SCHOST% %ECF_JOB% %ECF_JOBOUT%".format(schedule, user),
             ),

             Family("admin",

                # Task clean logfile
                Task("cleanlog",Date("28.*.*"),Time(timing['clean']),
                   Edit(
                      ECF_JOBOUT="%ECF_HOME%/ecf_out/ecf.out",
                      ECF_JOB_CMD="{} {} ecgb %ECF_JOB% %ECF_JOBOUT%".format(schedule, user),
                      NAME="cleanlog"),
                   Label("info", ""),
                ),

                # Task complete if something went wrong on the previous day
                Task("complete", Cron(timing['comp']),
                   Edit( NAME="complete", CLASS="ts", NP=1, SUITENAME=suite_name ),
                   Label("run", ""),
                   Label("info", ""),
                ),

                # Family operator if something goes wrong
                family_operator(),

             ),

             Family("runs",

                RepeatDate("DATUM",start_date,end_date),

                # Task dummy
                Task("dummy",
                  Edit(
                     NP=1,
                     CLASS='ns',
                     NAME="dummy",
                  ),
                  Label("run", ""),
                  Label("info", ""),
                  Defstatus("suspended"),
                ),

                # Main Runs per day (00, 06, 12, 18)
                Family("RUN_00",
                   Edit( LAUF='00', VORHI=6, LEAD=fcst, LEADCTL=fcstctl ),

                   # add suite Families and Tasks
                   family_dummy(timing['c00_1'],timing['c00_2']),
                   family_cleaning(),
                   family_obs(timing['o00_1'],timing['o00_2']),
                   family_main(),
#                   family_mirror(),
                ),

                Family("RUN_06",
                   Edit( LAUF='06',VORHI=6, LEAD=assimc, LEADCTL=assimc ),

                   # add suite Families and Tasks
                   family_dummy(timing['c06_1'],timing['c06_2']),
                   family_cleaning(),
                   family_obs(timing['o06_1'],timing['o06_2']),
                   family_main(),
#                   family_mirror(),
                ),

                Family("RUN_12",
                   Edit( LAUF='12',VORHI=6, LEAD=assimc, LEADCTL=assimc ),
   
                   # add suite Families and Tasks
                   family_dummy(timing['c12_1'],timing['c12_2']),
                   family_cleaning(),
                   family_obs(timing['o12_1'],timing['o12_2']),
                   family_main(),
#                   family_mirror(),
                ),

                Family("RUN_18",
                   Edit( LAUF='18',VORHI=6, LEAD=assimc, LEADCTL=assimc ),
 
                   # add suite Families and Tasks
                   family_dummy(timing['c18_1'],timing['c18_2']),
                   family_cleaning(),
                   family_obs(timing['o18_1'],timing['o18_2']),
                   family_main(),
#                   family_mirror(),
               ),
            )
         )
       )

###################################
### check and save C-LAEF suite ###
###################################

print("=> checking job creation: .ecf -> .job0");
print(defs.check_job_creation());
print("=> saving definition to file " + suite_name + ".def\n");
defs.save_as_defs(suite_name + ".def");
exit(0);

