# usage: ./op1_reload.sh ~/op1_backups/2020-04-16-14-11-52 /media/op1_parent_dir/
rsync -rvL --stats --checksum ${1}/* $2
