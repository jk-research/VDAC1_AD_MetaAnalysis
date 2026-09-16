# 01_geo_download.R — download GEO series matrices
source('00_setup.R')

geo_ids <- c('GSE5281','GSE109887','GSE132903','GSE29378',
             'GSE36980','GSE48350','GSE15222','GSE125583')

download_geo_metadata <- function(gse_id, destdir = 'data/metadata') {
  dir.create(destdir, showWarnings = FALSE, recursive = TRUE)
  prefix <- substr(gse_id, 1, nchar(gse_id) - 3)
  subdir <- paste0(prefix, 'nnn')
  url <- paste0('https://ftp.ncbi.nlm.nih.gov/geo/series/', subdir, '/',
                gse_id, '/matrix/', gse_id, '_series_matrix.txt.gz')
  destfile <- file.path(destdir, paste0(gse_id, '_series_matrix.txt.gz'))
  if (!file.exists(destfile)) download.file(url, destfile, mode = 'wb')
  destfile
}

for (gse in geo_ids) {
  message('Processing ', gse)
  tryCatch(download_geo_metadata(gse), error = function(e) message(e$message))
}
