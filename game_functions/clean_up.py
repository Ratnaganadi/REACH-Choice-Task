import os
import glob
import pprint as pp

# current_dir = os.path.dirname(os.path.realpath('__file__'))
# homepath=str(current_dir)


current_dir = os.path.dirname(os.path.realpath('__file__'))
print 'current_dir',current_dir
dirname=list(current_dir.split('/'))
length = len(current_dir)-len(dirname[len(dirname)-1])
homepath = current_dir[:length]
print 'homepath',homepath

def delete_files(file_path,condition):
    os.chdir(file_path)
    current_files = glob.glob('*.xls')
    print 'processing {}...'.format(file_path)
    if condition:
        for cond in condition:
            inputfile = glob.glob(cond)
            if inputfile:
                for f in inputfile: 
                    print 'removing',cond, f
                    os.remove(f)
                current_files = glob.glob('*.xls')
            if not inputfile: print 'found no match for', cond
        print 'files remaining:',len(current_files)
    else: print 'no condition given, do nothing.'
    return current_files

complete_datapath = homepath + 'data/complete_data/'
datapath = homepath + 'data/'


conditions = ['*conflicted copy*.xls','*conflicted copy*.log','*test*.xls','*test*.log']
complete_data = delete_files(complete_datapath,conditions)
other_data = delete_files(datapath,conditions)
