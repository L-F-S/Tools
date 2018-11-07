# just moves the folders with the polymd output to the simulaitons folder

cd ../input_files_pdb2kaw
for i in 1pgb 1poh 1psf 1shf_a 1ten 1tit 1ubq 1urn 1wit 2abd 2ci2 2pdd 2vik 256b; do
	cd $i.pdb
	echo moving $i 
	mv run* ../../simulations/$i.pdb
	cd ../
done
