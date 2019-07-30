"""posting.py : Create/Edit Posts v0.1 (2019-07-28)
usage:  posting.py (newpostname) : make new post file for current time
    or: posting.py (existingpostfile) : Edit last modified date
posting.py will work whether it is in _post directory or blog's root directory
parameters::
'-q' or '--quiet' : work without print texts
'-h' or '--help' : print this texts
"""
import datetime
import sys
import os

longparam={"quiet":"q","help":"h"}
param=["q","h"]
quietmode=False

def enableparam(par):
#Enable reciving parameter
    if par=='q':
        quietmode=True
    elif par=='h':
        print(__doc__)
        sys.exit()


if len(sys.argv)==1:
    print(__doc__)
    sys.exit()
for arg in sys.argv[1:]:
    print(arg)
    if '--' in arg:
        #handling long parameter
        if arg[2:] in longparam.keys():
            enableparam(longparam[arg[2:]])
        else: name=arg
    elif '-' in arg:
        #handling parameter
        if arg[1:] in param:
            enableparam(param[arg[1:]])
        else: name=arg
    else:
        name=arg
        
if os.getcwd().split('/')[-1] == '_posts': fdir=""
else: 
    fdir="_posts/"
    if(not quietmode): print("getting into _posts/...")

for file in os.listdir(os.getcwd()+'/'+fdir):   #finding file by name
    if name in file:
        if(not quietmode) : print("found "+os.path.join(file))
        name=file


if os.path.exists(fdir+name):
    post=open(fdir+name,"r")
    post.seek(0)
    lines=post.readlines()
    post.close()
    headercnt=0
    post=open(fdir+name,"w")
    
    for line in lines:
        print(">"+line)
        if '---' in line:
            headercnt+=1
            if headercnt == 2:
                if(not quietmode):
                    print("There is not last_modified_at tag. Adding one.")
                    post.write("last_modified_at: "+datetime.datetime.now().isoformat()+'\n')
            post.write("---\n")
        
        elif "last_modified_at:" in line:
            if(not quietmode):
                print("found "+line[:-2]+" at "+str(post.tell()))
                post.write("last_modified_at: "+datetime.datetime.now().isoformat()+'\n')
                headercnt=3 #to disable detect ---
        else: post.write(line)
    post.close()    

    if(not quietmode): print("Modified "+name)
    
else:
    post=open(fdir+datetime.date.today().isoformat()+'-'+name+".md","w")
    post.write("---\n")
    post.write("title: "+name)
    post.write("\npublished: true")
    post.write("\ncategory: newpostcategory")
    post.write("\ntags: [newposttag]")
    post.write("\nlast_modified_at: "+datetime.datetime.now().isoformat())
    post.write("\nexcerpt_separator: '<!--more-->'")
    post.write("\n---\n")
    post.write("\n## Sample Title\n")
    post.write("\nThis is a sample text")
    post.write("\n<!--more-->\n")
    post.write("\nThis is a sample text after excerp\n")
    post.close()
    if(not quietmode): print("The post "+name+" is successfully made.")