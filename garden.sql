CREATE TABLE garden(
  time DATETIME primary key,
  humidity DOUBLE PRECISION not null,
  temperature DOUBLE PRECISION not null,
  soil_moisture DOUBLE PRECISION not null,
  img_loc text
);
