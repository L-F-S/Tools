# USAGE:
# Rscript Free_Energy_plot.r rmsd_nc_dataframe.csv
# 1. Takes as input a tab separated file of 2 columns of coupled RMSD and (normalized) Native Contact values.
# 2. Calculates the free energy of each data point as the negative logarithm of the relative frequency of each data point.
# 3. Plots a 2D heatmap of free energy as a function of RMSD vs Native Contacts.

library(plyr)
library(reshape2)
library(ggplot2)
suppressMessages(library(data.table))

# 1. Import Data

args <- commandArgs(trailingOnly = T)
filename <- args[1]
plotname <- strsplit(filename, "/")[[1]][length(strsplit(filename, "/")[[1]])]
plotname <- substr(plotname, 1, nchar(plotname)-4)
outdir <- strsplit(filename, "/")[[1]][1:length(strsplit(filename, "/")[[1]])-1]
outdir <- paste0(outdir, collapse = "", "/")

data <- as.data.frame(fread(filename, header = T, showProgress = F))


# 2. Reshape data

d <- data
d$RMSD <- round(d$RMSD, digits = 3)
d$NC <- round(d$NC, digits = 3)
x <- count(d, vars = c("RMSD", "NC"))
tot <- sum(x$freq)
x$freq <- -log(x$freq/tot)
colnames(x) <- c("RMSD", "NC", "free_energy")
x$free_energy <- x$free_energy-min(x$free_energy)


#plot free energy as points

jet.colors <- colorRampPalette(c("#00007F", "blue", "#007FFF", "cyan", "#7FFF7F", "yellow", "#FF7F00", "red", "#7F0000"))

p <- (ggplot(data = x, aes(x = RMSD, y = NC, color=free_energy))
  + geom_point(aes(x = RMSD, y = NC, color = free_energy, shape = 15),size = 2)
#  + geom_tile()
  + scale_color_gradientn(colours=rev(jet.colors(7)))
  + scale_shape_identity()
  + labs(color = "Free Energy")
  + scale_x_continuous(limits = c(0, 4), breaks = seq(0,4,1))
  + theme_classic()
)

ggsave(p, filename = paste0(plotname, ".pdf"), path = outdir, device = "pdf", width = 13.60, height = 7.60)