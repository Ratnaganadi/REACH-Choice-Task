import os

def get_homepath(dir_hierarchy,go_home):

	current_dir = os.getcwd()
	dirname=list(current_dir.split('/'))
	length = len(current_dir)-len(dirname[len(dirname)-dir_hierarchy])
	homepath = current_dir[:length]

	if go_home or isinstance(go_home, basestring): 
		os.chdir(homepath+go_home)
	
	print 'current_dir',current_dir
	print 'homepath',homepath
	return homepath

# def error_check(vars):
# 	for var in vars:
# 		Error = True
# 		while Error:
# 			message = None
# 			if not var:
# 				message = 'Error: need {} information, none given.'.format(var)


# 			if dir_hierarchy and not isinstance(dir_hierarchy, int):
# 				message = 'Error: dir_hierarchy has to be int'
# 			if go_home!=False and not isinstance(go_home, basestring):
# 				message = 'Error: go_home has to be string or "False"'
# 			if message: 
# 				Error = True
# 				print message
# 			else: Error = False





