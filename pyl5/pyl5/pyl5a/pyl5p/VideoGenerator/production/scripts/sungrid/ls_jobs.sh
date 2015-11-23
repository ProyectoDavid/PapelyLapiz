# This script lists jobs running on the sun grid
qstat -u $USER | grep $USER | grep -v qw | grep -v INTERA | wc -l
qstat -u $USER | grep $USER | grep -v INTERA | wc -l
