import os

filestemp = os.listdir('./')

files = []
for f in filestemp:
    if f.find('root.log')>=0:
    #if f.find('root.sh')>=0:
        #files.append(f)
        os.remove(f)

print(len(filestemp))
print(len(files))

