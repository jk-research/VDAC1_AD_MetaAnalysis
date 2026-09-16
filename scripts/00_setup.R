# ============================================================
# 00_setup.R — VDAC1_AD_Project
# Source this at the top of every other script
# ============================================================

PROJ <- 'C:/Users/jeyak/OneDrive/Documents/VDAC1_AD_Project'
setwd(PROJ)

suppressPackageStartupMessages({
  library(data.table); library(dplyr); library(stringr)
  library(ggplot2); library(metafor); library(limma)
})

dir.create('results', showWarnings = FALSE)
dir.create('results/proteomics', showWarnings = FALSE)
cat('Setup complete. Working dir:', getwd(), '\n')
