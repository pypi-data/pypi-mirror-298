#!/usr/bin/env python3

import json
import shutil
import argparse
import configparser
import os
from pick import pick
from iterfzf import iterfzf
import time
import fnmatch
import tempfile
from subprocess import call
import datetime
from dateutil import parser
import random
import webbrowser
import pyperclip
from os.path import expanduser

# parms
parser = argparse.ArgumentParser(description='linker - Tag and open files from the CLI!')
parser.add_argument('-i','--importfile', nargs='+', metavar='filename', help='Add a new file.', required=False)
parser.add_argument('-l','--listfiles', help='List database contents.', metavar='filename|tag|ALL', required=False)
parser.add_argument('-t','--tag', nargs='+', metavar='tag', help='Optional tag filter when listing files (only valid with -l flag)', required=False)
parser.add_argument('-lt','--listtags', help='List all tags.', action='store_true', required=False)
parser.add_argument('--wrapper', help='Menu wrapper.', action='store_true', required=False)
parser.add_argument('-r','--restore', help='Restore corrupted linker database.', action='store_true', required=False)
parser.add_argument('-c', '--cli', nargs=2, metavar=('url', 'tags'), help='Manually enter bookmark: url, tags.', required=False)
parser.add_argument('--title', nargs='+', metavar='title', help='Title for the URL.', required=False)
args = parser.parse_args()

# configs
home = expanduser("~")
linker_base = ( home + '/linker')
linker_home = ( linker_base + '/bookmarks')
configfiledir = ( linker_base + '/conf')
configfile = ( linker_base + '/conf/linker.conf')

if not os.path.isfile(configfile):
  if not os.path.exists(configfiledir):
    os.makedirs(configfiledir)
  configfileobject = open(configfile, 'a+')
  configfileobject.write("[Main]\n")
  configfileobject.write('number_of_backups = 3\n')
  configfileobject.write('editor = vim\n')
  configfileobject.write('# When commented out, will use OS defaults:\n')
  configfileobject.write('#clipboard = copyqscript\n')
  configfileobject.write('#browser = /snap/bin/firefox\n')
  configfileobject.write("\n")
  configfileobject.write('[/home/workdevice/linker/bookmarks]\n')
  configfileobject.write('# Config section for different devices\n')
  configfileobject.write('clipboard = copyqscript\n')
  configfileobject.write('browser = /usr/bin/google-chrome\n')
  configfileobject.write("\n")
  configfileobject.close()

config = configparser.ConfigParser()
config.read(configfile)
bu_versions_to_keep = config.getint('Main', 'number_of_backups')
editorconf = config.get('Main', 'editor')
EDITOR = os.environ.get('EDITOR',editorconf)

jsondb=linker_home+"/linker.json"
jsondbss=linker_home+"/linkerss.json"

if not os.path.isfile(jsondb):
  if not os.path.exists(linker_home):
    os.makedirs(linker_home)
  jsondbobject = open(jsondb, 'a+')
  jsondbobject.write("{}")
  jsondbobject.close()

if not os.path.isfile(jsondbss):
  jsondbssobject = open(jsondbss, 'a+')
  jsondbssobject.write("{}")
  jsondbssobject.close()

# ansi color setup
class bcolors:
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    GRAY = '\033[0;37m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'

try:
  browser = config.get(linker_home, 'browser')
except:
  try:
    browser = config.get('Main', 'browser')
  except:
    browser = False

try:
  clipboard = config.get(linker_home, 'clipboard')
except:
  try:
    clipboard = config.get('Main', 'clipboard')
  except:
    clipboard = False


def dbfio(jsonfile,iotype,vtable={}):
  if iotype == "write":
    with open(jsonfile,"w") as outputfile:
      json.dump(vtable, outputfile)
  elif iotype == "read":
    with open(jsonfile,"r") as inputfile:
      try:
        vtable=json.load(inputfile)
      except ValueError:
        vtable={}
  return vtable


def abort(tocall="", extraArgs=""):
  if tocall == "":
    os.system("clear")
    print ("\n\n bye...\n")
    os._exit(0)
  else:
    tocall(extraArgs)

def define_bookmark_cli(url, title, tag_in):
  if url in videodb:
    print ("\nThat url appears to have already been imported.\n")
    return ["exists",url]
  videohash = {
    "url": url,
    "tags": tag_in,
    "title": title,
    "date": str(datetime.datetime.now())
  }
  return [videohash, url]

def define_bookmark():
  url = input("\nURL: ")
  if url in videodb:
    print ("\nThat url appears to have already been imported.\n")
    return ["exists",url]
  title = input("\nTitle: (default: %s)" % url)
  if title == "":
    title = url
  garbage = input("\npress [enter] to begin selecting tags:")
  try:
    tag_in = iterfzf(listalltags(), multi=True)
  except:
    tag_in = []
  if tag_in is None or tag_in == []:
    raw_in = input("\n\nno existing tag was selected. enter new tags (seperate by space): ").lower()
    if raw_in != "":
      tag_in = raw_in.split()
    else:
      tag_in = []
  videohash = {
    "url": url,
    "tags": tag_in,
    "title": title,
    "date": str(datetime.datetime.now())
  }
  return [videohash, url]

def add_a_bookmark_cli(url, title, raw_in):
  global videodb
  singlebookmark = define_bookmark_cli(url, title, raw_in)
  if singlebookmark[0] != "exists":
    videodb[singlebookmark[1]]=singlebookmark[0]
    save_and_reload()
    thetitle = reget_title(singlebookmark[1])
    selection = [singlebookmark[1], [thetitle]]
    menu(selection)
  else:
    selection = [singlebookmark[1],"exists"]
    garbage = input("Press <enter> to see it.")
    menu(selection)

def add_a_bookmark():
  global videodb
  singlebookmark = define_bookmark()
  if singlebookmark[0] != "exists":
    videodb[singlebookmark[1]]=singlebookmark[0]
    save_and_reload()
    thetitle = reget_title(singlebookmark[1])
    selection = [singlebookmark[1], [thetitle]]
    menu(selection)
  else:
    selection = [singlebookmark[1],"exists"]
    garbage = input("Press <enter> to see it.")
    menu(selection)

def reget_title(key):
  thetitle=videodb[key]["title"]
  tags=""
  for atag in videodb[key]["tags"]:
    tags=tags+"|"+atag
  tags=tags[1:]
  new_title=thetitle+" (Tags: "+tags+")"
  return new_title

def reget_titleb(key):
  thetitle=videodb[key]["title"]
  url=videodb[key]["url"]
  tags=""
  for atag in videodb[key]["tags"]:
    tags=tags+"|"+atag
  tags=tags[1:]
  new_title=thetitle+" (Tags: "+tags+")"
  return [thetitle, tags, url]

def list_all(searchstring='ALL',tagfilter='',getcount=False,getlistcount=False):
  results=[]
  response=[]
  if searchstring == 'ALL':
    for key, thehash in videodb.items():
      tags=""
      for atag in thehash["tags"]:
        tags=tags+"|"+atag
      tags=tags[1:]
      if tagfilter == [] or tagfilter is None:
        results.append([key, "%s (Tags: %s)" % (thehash['title'],tags),thehash['date']])
      else:
        tagmatch =  all(item in thehash["tags"] for item in tagfilter)
        if tagmatch:
          results.append([key, "%s (Tags: %s)" % (thehash['title'],tags),thehash['date']])
    kountresults=[]
    if getcount:
      for somerec in results:
        if somerec[1].split()[0].isdigit():
          kountresults.append(somerec[1].split()[0]) 
      kountresults.sort()
      try:
        nextcount = ( int(kountresults[-1]) + 1)
      except:
        nextcount="1"
      nextcount = ("%03d" % nextcount)
      return nextcount
  else:
    for key, thehash in videodb.items():
      if searchstring.lower() in thehash["title"].lower() or searchstring.lower() in thehash["tags"] or searchstring.lower() in thehash["url"]:
        tags=""
        for atag in thehash["tags"]:
          tags=tags+"|"+atag
        tags=tags[1:]
        if tagfilter == '':
          results.append([key, "%s (Tags: %s)" % (thehash['title'],tags),thehash['date']])
        else:
          tagmatch =  all(item in thehash["tags"] for item in tagfilter)
          if tagmatch:
            results.append([key, "%s (Tags: %s)" % (thehash['title'],tags),thehash['date']])
  userdisplay=[]
  results.sort(key=lambda x: x[1]) # sort by name
  for record in results:
    userdisplay.append(record[1])
  if userdisplay is None:
    userdisplay=""
  if len(userdisplay) == 1:
    if not getlistcount:
      response.append(results[0][1])
    else:
      return 1
  else:
    if getlistcount:
      return len(userdisplay)
    else:
      try:
        response = iterfzf(userdisplay, multi=True)
      except:
        response = []
  if response is None:
    response=""
  responsecount = len(response)
  if len(response) > 1:
    selectedresults=[]
    for somerec in response:
      for searchit in results:
        if somerec == searchit[1]:
          selectedresults.append(searchit[0])
    multitag(selectedresults)
    return [False,False,False]
  else:
    for searchit in results:
      try:
        if response[0] == searchit[1]:
          selectedkey = searchit[0]
      except:
        if args.listfiles or args.tag:
          abort()
        else:
          return [False,False,False]
    try:
      if len(userdisplay) == 1:
        return [selectedkey, response, False]
      else:
        return [selectedkey, response, True]
    except:
      if args.listfiles or args.tag:
        abort()
      else:
        return [False,False,False]

def listalltags():
  alltags=[]
  try:
    for key, thehash in videodb.items():
      for tag in thehash["tags"]:
        alltags.append(tag)
    uniqtags = list(set(alltags))
  except:
    uniqtags=[]
  return uniqtags

def multitag(fzfselected):
  os.system("clear")
  multimenu=["add tags","remove tags","delete","open","abort"]
  multioption, index = pick(multimenu, "batch mode:")
  if multioption == "abort":
    return False
  elif multioption == "add tags":
    tag_in_fzf = iterfzf(listalltags(), multi=False)
    newtag = True
    if tag_in_fzf is None:
      tag_in = input("\n\nno existing tag was selected. enter new tags (seperate by space): ").lower()
    else:
      tag_in = tag_in_fzf
    if tag_in == "":
      newtag = False
    if newtag:
      new_tags = tag_in.split()
      for key in fzfselected:
        for anewtag in new_tags:
          if anewtag not in videodb[key]["tags"]:
            videodb[key]["tags"].append(anewtag)
      save_and_reload()
      confirm = input("\ntags added. press [enter]")
  elif multioption == "remove tags":
    tagtochoose=[]
    for key in fzfselected: 
      for tag in videodb[key]["tags"]:
        tagtochoose.append(tag)
    tags_to_delete = iterfzf(list(set(tagtochoose)), multi=True)
    os.system("clear")
    print ("\n\nwill remove the following tags from the selected records:\n")
    for tag in tags_to_delete:
      print (tag)
    confirm = input("\nare you sure? (y|N): ")
    if confirm == "y":
      for key in fzfselected: 
        for deltag in tags_to_delete:
          try:
            videodb[key]["tags"].remove(deltag)
          except:
            pass
      save_and_reload()
      confirm = input("\ntags removed. press [enter]")
  elif multioption == "delete":
    print ("\n")
    for key in fzfselected:
      print (videodb[key]["title"])
    confirm = input("\n\ndelete selected records. are you sure? (y|N): ")
    if confirm == "y":
      for key in fzfselected:
        delfile(key, [False,False,False],False)
      confirm = input("\nrecords deleted. press [enter]")
    else:
      confirm = input("\n\ndelete aborted. press [enter]")
  elif multioption == "open":
    for key in fzfselected:
      runfile(key, True)
    abort()
  else:
    return False

def listtags():
  try:
    tag_in_fzf = iterfzf(listalltags(), multi=True)
  except:
    confirm = input("\nno tags exist yet. press [enter]")
    tag_in_fzf = []
  return tag_in_fzf

def tagmod(key, users_selection, studytag=False):
  if studytag:
    orig_tags = videodb[key]["tags"]
    newtags = []
    previousstudytag=1
    for origtag in orig_tags:
      if "studyrate_" not in origtag:
        newtags.append(origtag)
      else:
        previousstudytag=origtag[10:]
    if studytag.isdigit():
      formattedstudytag="studyrate_"+studytag
    else:
      if studytag == "bad":
        previousstudytag = int(previousstudytag)+1
        if previousstudytag > studytagmax:
          previousstudytag = studytagmax
      else:
        previousstudytag = int(previousstudytag)-1
        if previousstudytag < 1:
          previousstudytag = 1
      formattedstudytag="studyrate_"+str(previousstudytag)
    if studytag != "0":
      newtags.append(formattedstudytag)
    videodb[key]["tags"] = newtags
    save_and_reload()
  else:
    try:
      tag_in_fzf = iterfzf(listalltags(), multi=False)
    except:
      tag_in_fzf = None
    newtag = True
    if tag_in_fzf is None:
      tag_in = input("\n\nno existing tag was selected. enter new tags (seperate by space): ").lower()
      if tag_in == "":
        newtag = False
    else:
      tag_in = tag_in_fzf
    if newtag:
      try:
        new_tags = tag_in.split()
      except:
        new_tags = []
      for atag in new_tags:
        if atag not in videodb[key]["tags"]:
          videodb[key]["tags"].append(atag)
      save_and_reload()

def edittitle(key, users_selection):
  orig_title = videodb[key]["title"]
  with tempfile.NamedTemporaryFile(suffix=".tmp") as tf:
    tf.write(orig_title.encode('utf-8'))
    tf.flush()
    call([EDITOR, '+set backupcopy=yes', tf.name])
    tf.seek(0)
    videodb[key]["title"] = tf.read().rstrip().decode()
    save_and_reload()
    users_selection[1]=[reget_title(users_selection[0])]

def tagdel(key, users_selection):
  orig_tags = videodb[key]["tags"]
  orig_tags.append("abort")
  tag, index = pick(orig_tags, "Select tag to delete:")
  if tag != "abort":
    orig_tags.remove("abort")
    orig_tags.remove(tag)
    videodb[key]["tags"] = orig_tags
    save_and_reload()
    users_selection[1]=[reget_title(users_selection[0])]
  else:
    orig_tags.remove("abort")

def runfile(key, stayopen=False):
  if not browser:
    webbrowser.open(videodb[key]["url"])
  else:
    urlfmt="\"%s\"" % videodb[key]["url"]
    torun = "%s %s" % (browser, urlfmt)
    os.system(torun)
  if not stayopen:
    abort()

def copyurl(key, stayopen=False):
  if not clipboard:
    pyperclip.copy(videodb[key]["url"])
  else:
    urlfmt="\"%s\"" % videodb[key]["url"]
    torun = "%s %s" % (clipboard, urlfmt)
    os.system(torun)
  print ("\n\nURL copied to clipboard.\n")
  time.sleep(0.2)
  if not stayopen:
    abort()

def delfile(key, users_selection,confirmit=True):
  title = videodb[key]["title"]
  if confirmit:
    confirm = input("\ndelete: %s.  are you sure? (y|N): " % title)
    if confirm == "y":
      torun = "rm -f %s" % videodb[key]["url"]
      del videodb[key]
      os.system(torun)
      save_and_reload()
      return True
    else:
      return False
  else:
    torun = "rm -f %s" % videodb[key]["url"]
    del videodb[key]
    os.system(torun)
    save_and_reload()
    return True

def menu(users_selection):
  loop = True
  catit = False
  userin = ""
  while loop:
      pageno=1
      try:
        users_selection[1]=[reget_titleb(users_selection[0])]
      except:
        return
      os.system("clear")
      title = users_selection[1][0][0]
      thetags = users_selection[1][0][1]
      url = users_selection[1][0][2]
      key = users_selection[0]
      dateobject = datetime.datetime.strptime(videodb[key]["date"], "%Y-%m-%d %H:%M:%S.%f")
      datestring=dateobject.strftime("%d-%m-%y %H:%M")
      print (bcolors.OKGREEN+"\n%s\n" % title +bcolors.ENDC)
      print (bcolors.FAIL+"%s\n" % (datestring) +bcolors.ENDC)
      print (bcolors.GRAY+"(t)ags: %s\n" % (thetags) +bcolors.ENDC)
      print (bcolors.OKBLUE+"\n%s\n" % (url) +bcolors.ENDC)
      print
      linecount=0
      garbage = True
      studyanswer=[]
      if pageno > 1:
        pagestring="-p%s-" % pageno
      else:
        pagestring=""
      print (bcolors.GRAY+"\n(r)emove-tag  (s)imilar-tags  (e)dit-title  (d)elete  (c)lip  (b)ack [/]  [q]uit\t%s\n" % pagestring +bcolors.ENDC)
      appendprompt=False
      if not appendprompt:
        userin = input(": ").lower()
      if userin == "o" or userin == "":
        runfile(key)
      if userin == "c":
        copyurl(key, False)
      elif userin.isdigit():
        tagmod(key, users_selection, userin)
      elif userin == "t":
        tagmod(key, users_selection)
      elif userin == "r":
        tagdel(key, users_selection)
      elif userin == "d":
        if delfile(key, users_selection):
          loop = False
      elif userin == "e":
        edittitle(key, users_selection)
      elif userin == "n":
        editnotes(key, users_selection)
      elif userin == "a":
        editapplication(key, users_selection)
      elif userin == "s":
        similartags(key)
      elif userin == "q":
        loop = False
      elif userin == "b" or userin == "/":
        loop = False
  if userin == "q":
    abort()
  return userin

def save_and_reload():
  global videodb
  global bu_versions_to_keep
  uniqdt=time.strftime("%Y-%m-%d-%H-%M-%S")
  torun="cp %s %s.%s" % (jsondb, jsondb, uniqdt)
  videodb = dbfio(jsondb,"write", videodb)
  os.system(torun) # make a new backup
  nobufiles=len(fnmatch.filter(os.listdir(linker_home), 'linker.json.*'))
  while nobufiles > bu_versions_to_keep: # remove old backups
    backuplist=fnmatch.filter(os.listdir(linker_home), 'linker.json.*')
    backuplist.sort()
    oldestbu=backuplist[0]
    os.remove(linker_home+'/'+oldestbu)
    nobufiles=len(fnmatch.filter(os.listdir(linker_home), 'linker.json.*'))
  videodb = dbfio(jsondb,"read")

def restore():
  restore4user = input("\n\nRestore linker database from latest backup? Are you sure? (y|N): ")
  if restore4user == 'y':
    backuplist=fnmatch.filter(os.listdir(linker_home), 'linker.json.*')
    latestbackup=backuplist[-1]
    shutil.copy2(linker_home+'/'+latestbackup,jsondb)
    print ("\n\nDatabase restored.\n\n")

def search():
  os.system("clear")
  userin = input("\n search string: ").lower()
  confirm = input("\n filter by tags? (y|N): ")
  if confirm == "y":
    try:
      tagarray = iterfzf(listalltags(), multi=True)
    except:
      tagarray = []
    try:
      tag_in = tagarray[0] 
    except IndexError:
      tagarray=[]
  else:
    tagarray=[]
  selection = list_all(userin, tagarray)
  menu(selection)
  while selection[2]:
    selection = list_all(userin, tagarray)
    menu(selection)

def similartags(thekey):
  alltags=videodb[thekey]["tags"]
  tagarray = iterfzf(alltags, multi=True)
  try:
    if tagarray[0] != "":
      selection = list_all(searchstring, tagarray)
      menu(selection)
      while selection[2]:
        selection = list_all(searchstring, tagarray)
        menu(selection)
  except:
    pass

def saved_search(searchfunction): #add, delete, rename
  os.system("clear")
  savedsearches = dbfio(jsondbss,"read")
  userlist = list(savedsearches)
  userlist.append("abort")
  if searchfunction == "add":
    userin = input("\n\n search string: ").lower()
    confirm = input("\n include search by tags? (y|N): ")
    if confirm == "y":
      tagarray = iterfzf(listalltags(), multi=True)
      try:
        tag_in = tagarray[0] 
      except IndexError:
        tagarray=[]
    else:
      tagarray=[]

    ssname = input(" save search as: ").lower()
    if ssname != "":
      savedsearches[ssname]=[userin,tagarray]
      savedsearches = dbfio(jsondbss,"write", savedsearches)
  else:
    thesearch, thekey = pick(userlist, "\n select saved-search to %s:" % searchfunction)
    if thesearch != "abort":
      os.system("clear")
      if searchfunction == "delete":
        userresp = input("\n\n are you sure? (y/n): ").lower()
        if userresp == "y":
          del savedsearches[thesearch]
          savedsearches = dbfio(jsondbss,"write", savedsearches)
      else: #rename
        userresp = input("\n\n new name: ").lower()
        savedsearches[userresp] = savedsearches[thesearch]
        del savedsearches[thesearch]
        savedsearches = dbfio(jsondbss,"write", savedsearches)

def wrapper():
  menuoptions=[
                "tags",
                "all",
                "new",
                "search",
                "admin",
              ]
  savedsearches = dbfio(jsondbss,"read")
  sortedss=list(savedsearches)
  sortedss.sort()
  sswithcount=[]
  for somerec in sortedss:
    thecount = list_all(savedsearches[somerec][0], savedsearches[somerec][1], False, True)
    sswithcount.append([somerec+" ("+str(thecount)+")", somerec])
  sswithcountformatted=[]
  for somerec in sswithcount:
    sswithcountformatted.append(somerec[0])
  quit=["/"]
  try:
    spacer=["-" * len(max(sortedss, key=len))]
  except:
    spacer=False
  if spacer:
    menuselection = iterfzf(menuoptions+spacer+sswithcountformatted+spacer+quit, multi=False)
  else:
    menuselection = iterfzf(menuoptions+quit, multi=False)
  try:
    found=False
    for somerec in sswithcount:
      if menuselection == somerec[0]:
        userss=savedsearches[somerec[1]]
        found=True
        break
  except:
    found=False
  if found:
    return userss
  else:
    return menuselection

def wrapper_admin():
  os.system("clear")
  menuoptions=[
                "saved search - add",
                "saved search - delete",
                "saved search - rename",
                "/"
              ]
  menuselection = iterfzf(menuoptions, multi=False)
  if menuselection == "saved search - add":
    saved_search("add")
  elif menuselection == "saved search - delete":
    saved_search("delete")
  elif menuselection == "saved search - rename":
    saved_search("rename")
  else:
    return False

#
# MAIN CODE
#

videodb = dbfio(jsondb,"read") 
searchstring = "ALL"
tags = menuselect = ""
selection="begin"

if args.restore:
  restore()
  abort()

if args.cli:
  url, tags = args.cli
  tags = tags.split(',')
  title = ' '.join(args.title)
  add_a_bookmark_cli(url,title,tags)
  abort()

if not args.importfile and not args.listfiles and not args.tag and not args.listtags and not args.restore:
  while True:
    if menuselect == "q":
      input("debug2")
      abort()
    choice=wrapper()
    try:
      if choice == "all":
        try:
          selection = list_all("ALL", "")
        except:
          selection = []
        menuselect=menu(selection)
        while selection[2]:
          selection = list_all("ALL", "")
          menuselect=menu(selection)
      elif choice == "search":
        search()
      elif choice == "tags":
        tagarray = listtags()
        try:
          if tagarray[0] != "":
            selection = list_all(searchstring, tagarray)
            menuselect=menu(selection)
            while selection[2]:
              selection = list_all(searchstring, tagarray)
              menuselect=menu(selection)
        except:
          pass
      elif choice == "/":
        abort()
      elif choice == "admin":
        wrapper_admin()
      elif choice == "new":
        add_a_bookmark()
      else:
        try:
          usersearchstring=choice[0]
          usersearchtagsarray=choice[1]
          print ("%s" % usersearchstring )
          print ("%s" % usersearchtagsarray )
          selection = list_all(usersearchstring, usersearchtagsarray)
          menuselect=menu(selection)
          while selection[2]:
            selection = list_all(usersearchstring, usersearchtagsarray)
            menuselect=menu(selection)
        except:
          pass
    except IndexError:
      pass
else:
  while selection != "":
    if args.importfile:
      url = ' '.join(args.importfile)
      add_a_file(url)
      args.importfile = False
      args.listfiles = "ALL"
      tagarray = ''
    elif args.listfiles:
      searchstring = ''.join(args.listfiles)
      if args.tag:
        tags = ' '.join(args.tag)
        tagarray = tags.split()
      else:
        tagarray = ''
      selection = list_all(searchstring, tagarray)
      menuselect=menu(selection)
      while selection[2]:
        selection = list_all(searchstring, tagarray)
        menuselect=menu(selection)
    elif args.listtags:
      tagarray = listtags()
      try:
        if tagarray[0] != "":
          selection = list_all(searchstring, tagarray)
          menuselect=menu(selection)
          while selection[2]:
            selection = list_all(searchstring, tagarray)
            menuselect=menu(selection)
      except IndexError:
        abort()
    else:
      if args.tag:
        tags = ' '.join(args.tag)
        tagarray = tags.split()
        args.tag = ''
      else:
        tagarray = ''
      selection = list_all(searchstring, tagarray)
      menuselect=menu(selection)
      while selection[2]:
        selection = list_all(searchstring, tagarray)
        menuselect=menu(selection)
      selection = ''

videodb = dbfio(jsondb,"write", videodb) # save database
