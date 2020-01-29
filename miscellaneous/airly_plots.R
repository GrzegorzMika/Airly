library(tidyverse)
files <- str_c("Pulpit/Projects/Airly/", list.files("Pulpit/Projects/Airly/")[str_detect(list.files("Pulpit/Projects/Airly/"), "csv")])

Airly <- map_df(files, read_csv)
Airly %>%
  filter(installation_id %in% c(3105, 2339)) %>%
  select(installation_id, air_quality_index_value, start_date) %>%
  mutate(installation_id = as.character(installation_id)) %>%
  ggplot(aes(x = start_date, y = air_quality_index_value, col = installation_id)) + geom_line(size = 1)
