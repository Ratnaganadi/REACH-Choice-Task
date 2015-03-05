from subprocess import check_output
from dir_function import get_homepath

dir_hierarchy = 1
homepath = get_homepath(dir_hierarchy,go_home='')

commit_hash = check_output(["git","rev-parse","HEAD"])

commit_hash = commit_hash.strip()

version_file = open("taskversion.py", "w")

version_file.write("'" + commit_hash + "'")

version_file.close()