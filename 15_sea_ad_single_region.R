setwd("C:/Users/jeyak/OneDrive/Documents/VDAC1_AD_Project")
library(data.table)
library(ggplot2)

REGION <- "V1C"
rc <- tolower(REGION)

vdac1 <- fread(paste0("data/sea_ad/sea_ad_", rc, "_vdac1_raw.csv"))
cm <- fread("data/sea_ad/sea_ad_cell_metadata.csv",
            select = c("cell_label", "donor_label", "umi_count"))
c2c <- fread("data/sea_ad/sea_ad_cell_to_cluster.csv")
c2c <- unique(c2c[, .(cell_label, cluster_alias = as.character(cluster_alias))])
cta <- fread("data/sea_ad/sea_ad_cluster_to_annotation.csv")
cta_sub <- unique(cta[cluster_annotation_term_set_name == "Subclass",
                      .(cluster_alias = as.character(cluster_alias),
                        cell_type = cluster_annotation_term_name)])
dis <- fread("data/sea_ad/sea_ad_disease_metadata.csv")
setnames(dis, "Overall AD neuropathological Change", "ad_stage")
bm <- c("Braak 0"=0,"Braak I"=1,"Braak II"=2,"Braak III"=3,
        "Braak IV"=4,"Braak V"=5,"Braak VI"=6)
dis[, braak_num := bm[Braak]]
dis_small <- unique(dis[, .(donor_label, ad_stage, braak_num)])

df <- vdac1[cm, on = "cell_label", nomatch = 0]
df <- df[c2c, on = "cell_label", nomatch = 0]
df <- df[cta_sub, on = "cluster_alias", nomatch = 0]
df <- df[dis_small, on = "donor_label", nomatch = 0]
df$group <- fifelse(df$ad_stage %in% c("Intermediate","High"), "AD",
             fifelse(df$ad_stage == "Not AD", "Control", NA_character_))

pb <- df[, .(vdac1_sum = sum(vdac1_raw), umi_sum = sum(umi_count),
             n_cells = .N, group = group[1], braak_num = braak_num[1]),
         by = .(donor_label, cell_type)]
pb$cpm <- pb$vdac1_sum / pb$umi_sum * 1e6
pb$log2_vdac1 <- log2(pb$cpm + 1)
pb <- pb[n_cells >= 20]
pb$region <- REGION
fwrite(pb, paste0("results/sea_ad_", rc, "_pseudobulk.csv"))

cat(REGION, "donors:", length(unique(pb$donor_label)), "\n")
print(table(unique(pb[, .(donor_label, group)])$group))

res <- pb[!is.na(group), {
  ad <- log2_vdac1[group == "AD"]; ctl <- log2_vdac1[group == "Control"]
  if (length(ad) < 4 | length(ctl) < 4) {
    .(n_AD = length(ad), n_Control = length(ctl),
      log2FC = NA_real_, SE = NA_real_, p = NA_real_)
  } else {
    tt <- t.test(ad, ctl)
    .(n_AD = length(ad), n_Control = length(ctl),
      log2FC = mean(ad) - mean(ctl),
      SE = sqrt(var(ad)/length(ad) + var(ctl)/length(ctl)),
      p = tt$p.value)
  }
}, by = cell_type]
res$p_adj <- p.adjust(res$p, method = "BH")
setorder(res, log2FC)
fwrite(res, paste0("results/sea_ad_", rc, "_vdac1_by_celltype.csv"))
print(res)

braak_res <- pb[!is.na(braak_num), {
  if (.N >= 8) {
    ct <- cor.test(log2_vdac1, braak_num, method = "spearman", exact = FALSE)
    .(n_donors = .N, rho = unname(ct$estimate), p = ct$p.value)
  } else .(n_donors = .N, rho = NA_real_, p = NA_real_)
}, by = cell_type]
braak_res$p_adj <- p.adjust(braak_res$p, method = "BH")
setorder(braak_res, rho)
fwrite(braak_res, paste0("results/sea_ad_", rc, "_vdac1_vs_braak.csv"))
print(braak_res)

p <- ggplot(res[!is.na(log2FC)],
            aes(x = log2FC, y = reorder(cell_type, log2FC))) +
  geom_vline(xintercept = 0, linetype = "dashed", color = "grey60") +
  geom_errorbarh(aes(xmin = log2FC - 1.96*SE, xmax = log2FC + 1.96*SE),
                 height = 0.2, linewidth = 0.5) +
  geom_point(aes(color = p_adj < 0.05), size = 3) +
  scale_color_manual(values = c("grey50", "firebrick3")) +
  labs(title = paste0("VDAC1 by cell type in SEA-AD ", REGION),
       x = "log2 fold change", y = "", color = "") +
  theme_minimal(base_size = 13) + theme(legend.position = "bottom")
ggsave(paste0("results/sea_ad_", rc, "_vdac1_by_celltype.png"), p,
       width = 9, height = 7, dpi = 300)

cat("\nSaved ", REGION, " results.\n", sep = "")
