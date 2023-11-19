CREATE TABLE IF NOT EXISTS data
(
    InstallationId integer not null,
    FromDateTime timestamp not null,
    TillDateTime timestamp not null,
    Name         text      not null,
    Value        float     not null
);