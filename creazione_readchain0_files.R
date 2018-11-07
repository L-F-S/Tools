wd <- "/home/lorenzo/tirocinio/input_files_pdb2kaw/"
folder <- list.files(wd)[grep("pdb", list.files(wd))]
f <- substr(folder, start = 1, nchar(folder)-4)
for(i in f){
  comm2 <- paste0("awk '{if (NR==1) {print \"#read_chain     0\"} else {print $0} }' ", wd, i, ".pdb/", i, ".kaw > ", wd, i, ".pdb/", i, "_0.kaw")
  system(comm2)
  }