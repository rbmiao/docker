#!/usr/bin/python
import os
import json
import commands
import sys
import time

if __name__ == "__main__":
    mem = "8192"
    cpuset = '0-5'
    timestr = time.strftime("%Y%m%d%H%M%S", time.localtime()) 
    rmlimit = 20

    if len(sys.argv) <= 1:
        print "How to use:"
        print "\t [Command] image version project"
        print "\t e.g: [Command]  docker-registry.xxxxx.com:5000/xxxxxx/nginx-php   v1  test.xxxxxx.com"
        sys.exit(0)


    image = sys.argv[1]
    version = sys.argv[2]
    project = sys.argv[3]
    
    runcomm = "docker run -it -d -v /etc/localtime:/etc/localtime:ro --name "+project+"_"+version+"_"+timestr + "  -m "+mem+"m --cpuset-cpus "+cpuset+ "  " + image+":"+version
    print runcomm
    status,did = commands.getstatusoutput( runcomm )
    if status != 0 :
        print "docker run error!",did
        sys.exit(1)

    file_list = "/home/code/"+project+".list"
    f=open(file_list,'a')
    f.write( did )
    f.write("\n")

    dockerlist = open(file_list,'rU').readlines()
    #print dockerlist
    dockercount = len( dockerlist )
    print "project total count is:", dockercount

    rmcount = dockercount - rmlimit
    if rmcount > 0 :
        i = 0
        while i < rmcount:
            rmdocker = dockerlist[i][0:24]
            rmcomm = "docker rm -f "+rmdocker
            print rmcomm
            commands.getstatusoutput( rmcomm )
            del( dockerlist[i] )
            i += 1
    
    fl=open(file_list, 'w')
    for dockerid in dockerlist:
        fl.write(dockerid)
    fl.close()

    #3, get port
    inspcomm = "docker inspect "+did[0:24]
    status,inspres = commands.getstatusoutput( inspcomm )
    outres = json.loads( inspres )
    ip = outres[0]["NetworkSettings"]["IPAddress"]
    #sshport = outres[0]["NetworkSettings"]["Ports"]["22/tcp"][0]["HostPort"]
    
    print "--------------done-----------------"
    print "------docker id is:",did
    print "\n\n"
    print "ssh command is:  ssh work@"+ip
    print "\n\n"