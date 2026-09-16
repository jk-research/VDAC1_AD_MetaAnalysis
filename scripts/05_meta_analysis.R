# 05_meta_analysis.R — random-effects meta-analysis
source('00_setup.R')

effects <- read.csv('results/all_effects_combined.csv', stringsAsFactors = FALSE)
res <- rma(yi = log2FC, sei = SE, data = effects, method = 'REML')
print(summary(res))

write.csv(
  data.frame(k = res$k, estimate = res$b, SE = res$se,
             pval = res$pval, ci_lb = res$ci.lb, ci_ub = res$ci.ub,
             I2 = res$I2, tau2 = res$tau2),
  'results/overall_meta_summary.csv', row.names = FALSE
)

# Subgroup by platform
effects$platform <- ifelse(effects$dataset_id == 'GSE125583', 'RNA-seq', 'microarray')
res_platform <- rma(yi = log2FC, sei = SE, mods = ~ platform,
                    data = effects, method = 'REML')
print(summary(res_platform))
