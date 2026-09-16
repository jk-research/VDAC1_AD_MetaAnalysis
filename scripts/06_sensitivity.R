# 06_sensitivity.R — LOO, Baujat, funnel, Egger's, influence
source('00_setup.R')

effects <- read.csv('results/all_effects_combined.csv', stringsAsFactors = FALSE)
res <- rma(yi = log2FC, sei = SE, data = effects, method = 'REML')

# Leave-one-out
leave1 <- leave1out(res)
print(leave1)

# Egger's test
egger <- regtest(res, model = 'lm')
sink('results/eggers_test.txt'); print(egger); sink()

# Funnel plot
pdf('results/funnel_plot.pdf', width = 8, height = 6)
funnel(res, main = 'Funnel Plot: VDAC1 in AD vs Control')
dev.off()
