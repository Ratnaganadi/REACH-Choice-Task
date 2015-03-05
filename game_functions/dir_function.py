import os

def get_homepath(dir_hierarchy,go_home):
	current_dir = os.path.dirname(os.path.realpath('__file__'))
	dirname=list(current_dir.split('/'))
	length = len(current_dir)-len(dirname[len(dirname)-dir_hierarchy])
	homepath = current_dir[:length]
	if go_home or isinstance(go_home, basestring): os.chdir(homepath+go_home)
	print 'current_dir',current_dir
	print 'homepath',homepath
	return homepath
