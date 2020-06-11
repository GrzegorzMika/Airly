library("data.table")

setDTthreads(threads = parallel::detectCores()) # allow data.table to use all available (including logical) cores

t0 <- Sys.time()
path <- "/home/grzegorz/Pulpit/Projects/Airly/data/" # path to folder with raw data

preprocess <- function(df) { # sometimes the columns from columns air_quality_index_colour are shifted by one, so deal with it
  if (length(colnames(df)) == 21) {
    tmp <- copy(df)
    tmp <- tmp[!is.na(tmp[, V21])]
    cn <- colnames(tmp)
    tmp <- tmp[, cn[9:20] := tmp[, 10:21]]
    tmp <- tmp[, V21 := NULL]

    tmp_1 <- copy(df)
    tmp_1 <- tmp_1[is.na(tmp_1[, V21])]
    tmp_1 <- tmp_1[, V21 := NULL]

    return(rbindlist(list(tmp, tmp_1)))
  }
  else {
    return(df)
  }
}

files <- paste0(path, list.files(path, pattern = ".csv"))

df <- lapply(files, fread, sep = ",")

df <- lapply(df, preprocess)

for (i in 1:length(files)) {
  fwrite(df[[i]], file = files[i])
}

df <- rbindlist(df)

fwrite(df, paste0(path, "airly_data_full.csv"))

Sys.time() - t0
