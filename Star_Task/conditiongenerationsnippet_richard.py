import csv
import cPickle

xy_pos_dict = {}

conditions = [['size','xy_pos_key']]

for n in [1]:#list of the sizes you want to generate conditions for
    for i in range(1):#however many conditions for each size you want to generate
        #Here is where your xy_pos generation code goes, I assume you will have some list named xy_pos as the output
        
        xy_pos_key = str(n)+"_"+str(i)
        xy_pos_dict[xy_pos_key] = xy_pos
        
        conditions.append([n, xy_pos_key])

with open('xy_pos.obj','w') as filename:

    pickling = cPickle.Pickler(filename)

    pickling.dump(xy_pos_dict)

    filename.close()

with open('conditions.csv','w') as filename:

    csving = csv.writer(filename)
    
    csving.writerows(conditions)
    
    filename.close()

#This will save the dictionary and the conditions file
#To reopen the dictionary as an object later, use the code below:

unpickler = cPickle.Unpickler(open('xy_pos.obj','r'))

xy_pos_dict = unpickler.load()