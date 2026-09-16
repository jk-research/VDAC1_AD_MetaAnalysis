# 04_effect_sizes.R — limma (microarray) + DESeq2 (RNA-seq)
source('00_setup.R')

# Produces: results/limma_effects_all.csv
#           results/GSE125583_DESeq2_effect.csv
#           results/all_effects_combined.csv
cat('Run effect size computation from project history\n')
