# 09_isoforms.R — VDAC1 vs VDAC2 vs VDAC3 comparison
source('00_setup.R')

iso <- read.csv('results/isoform_all_effects.csv', stringsAsFactors = FALSE)
for (v in c('VDAC1', 'VDAC2', 'VDAC3')) {
  sub <- iso[iso$isoform == v, ]
  res <- rma(yi = log2FC, sei = SE, data = sub, method = 'REML')
  cat('\n===', v, '===\n'); print(summary(res))
}
