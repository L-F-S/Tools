cd ../input_files_pdb2kaw
for folder in $(ls); do
	echo entering folder $folder
	cd $folder
	kawfile=$(ls *kaw)
	python ../../distcheck.py $kawfile
	cd ../
done
