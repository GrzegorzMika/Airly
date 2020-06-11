library(tidyverse)
path <- "/home/grzegorz/Pulpit/Projects/Airly/data/airly_data_full.csv"
# files <- str_c(path, list.files(path)[str_detect(list.files(path), "csv")])

# Airly <- map_df(files, read_csv)
Airly <- read_csv(path)
Airly %>%
  filter(installation_id %in% c(3105, 2339)) %>% 
  filter(air_quality_index_value < 500) %>% 
  select(installation_id, air_quality_index_value, start_date) %>%
  mutate(installation_id = as.character(installation_id)) %>%
  mutate(location = ifelse(installation_id == 3105, "Czeladź", "Kraków")) %>%
  ggplot(aes(x = start_date, y = air_quality_index_value, col = location)) +
  geom_line(size = 1)
  
