####### to be used only once:
## generate a .kaw file from the original, but with readchain = 0

from sys import argv
filename = argv1[1]
original = open(filename)
newfile = ""
firstiline = True
for line in original.readlines():
	if firstline == True:
		newfile += "#read_chain     0"
		firstline = False
	else:
		newfile += line

original.close()
newfilename = filename.rstrip(".kaw")+"_0.kaw"
new_file = open(newfilename, "w")
new_file.write(newfilename)
new_file.close()