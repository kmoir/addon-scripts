pvt_key = "user:nnn...."
secret = "my_secret"

f = open("addonlist.txt","r")
l = []
for line in f:
    l.append(line[0:len(line)-1])
f.close()

for entry in l:
    print "jpm sign --api-key ", pvt_key, " --api-secret ", secret,  " --xpi ", entry
# I exported the commands to a script and ran them one by one since many of
# them were problematic
