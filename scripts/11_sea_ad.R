# 11_sea_ad.R — SEA-AD MTG cell-type-specific VDAC1 analysis
source('00_setup.R')

pb <- fread('data/sea_ad/sea_ad_mtg_vdac1_pseudobulk.csv')
pb <- pb[pb$n_cells >= 10 & !is.na(pb$diagnosis), ]
pb$diagnosis <- ifelse(grepl('AD', pb$diagnosis, ignore.case = TRUE), 'AD', 'Control')
pb$log2_vdac1 <- log2(pb$vdac1_sum / pb$n_cells + 1)

results <- do.call(rbind, lapply(unique(pb$cell_type), function(ct) {
  sub <- pb[pb$cell_type == ct, ]
  ad <- sub$log2_vdac1[sub$diagnosis == 'AD']
  ctl <- sub$log2_vdac1[sub$diagnosis == 'Control']
  if (length(ad) < 3 | length(ctl) < 3) return(NULL)
  tt <- t.test(ad, ctl)
  data.frame(cell_type = ct, n_AD = length(ad), n_Control = length(ctl),
             log2FC = mean(ad) - mean(ctl),
             SE = sqrt(var(ad)/length(ad) + var(ctl)/length(ctl)),
             p_value = tt$p.value)
}))
results$p_adj <- p.adjust(results$p_value, method = 'BH')
write.csv(results, 'results/sea_ad_vdac1_by_celltype.csv', row.names = FALSE)
print(results)
