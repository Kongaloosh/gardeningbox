CREATE TABLE garden(
  time timestamp primary key,
  humidity      double precision not null,
  temperature     double precision not null,
  soil_moisture   double precision not null,
  img_loc     text
);
