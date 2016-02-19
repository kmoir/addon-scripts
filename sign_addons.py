from jose import jws
from jose.constants import ALGORITHMS
import random
import time
#import requests
#from requests_jwt import JWTAuth
import rdflib
import zipfile
import os
import fnmatch


#sign addons with JWT
#needs to be fixed
#better script is https://github.com/jasonthomas/sign-addon/blob/master/sign.py

def generate_token(pvt_key, secret, valid_for=3600, algorithm=ALGORITHMS.HS256):
    #generate JWT token
    jti = str(random.random())
    iat = int(time.time())
    valid_for = iat + 60
    payload = {"iss": pvt_key,
               "iat": iat,
               "jti": jti,
               "exp": valid_for,
               }
    return jws.sign(payload, secret, algorithm=algorithm)


def find_files(start, regexp):
    l = []
    for relpath, dirs, files in os.walk(start):
        for f in files:
            if fnmatch.fnmatch(f, regexp):
                full_path = os.path.join(start, relpath, f)
                l.append(full_path)
    return(l)


def addons_dict(my_dir, regexp):
    #create a dictionary of the xpi files that need to be signed in a dir
    #create list of files in dir that end in .xpi
    addons_list = find_files(my_dir, regexp)

    manifest = "install.rdf"
    outpath = "/Users/kmoir/tmp3"
    a_dict = {}
    for a in addons_list:
        fh = open(a, 'rb')
        try:
           z = zipfile.ZipFile(fh)
           for name in z.namelist():
              if name == manifest:
                  z.extract(name, outpath)
                  #parse manifest
                  g = rdflib.Graph()
                  addons_path = os.path.join(outpath, name)
                  g.parse(addons_path)
                  for subj, pred, obj in g:
                      if pred.endswith("#id"):
                          a_dict[a] = str(obj)
                          continue
                  fh.close()
                  #cleanup files
                  os.remove(addons_path)
        except zipfile.BadZipfile as e:
           print "File ", a , "is a invalid file"

    return a_dict

#main
my_dir = "/Users/kmoir/hg/mozilla-central/toolkit/mozapps/extensions/test/xpcshell"
regexp = "*.xpi"
addons_to_sign = addons_dict(my_dir, regexp)
print addons_to_sign
pvt_key = ""

secret = ""
#token = generate_token(pvt_key, secret)
#print token
#need to parse id from install.rdf
#url = "https://addons.mozilla.org/api/v3/addons/system5@tests.mozilla.org/versions/1.0"
#print url

#auth = JWTAuth(token)
#headers = {"Authorization: JWT": str(token)}
#print headers
#files = {'upload': open('system5_1.xpi', 'rb')}
#payload = {'upload': 'system5_1.xpi'}
#s = requests.Session()
##s.auth = auth
#s.headers.update(headers)
#r = s.put(url, data=payload)
#print r.status_code
