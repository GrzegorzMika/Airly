CREATE TABLE IF NOT EXISTS data
(
    installation_id   integer   not null,
    from_date_time    timestamp not null,
    till_date_time    timestamp not null,
    measurement_name  text      not null,
    measurement_value float     not null,
    CONSTRAINT data_pk PRIMARY KEY (installation_id, from_date_time, measurement_name)
);