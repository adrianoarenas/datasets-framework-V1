create table if not exists staging.london_pollution (
    "timestamp" timestamp,
    location varchar(50),
    country varchar(50),
    temp_c double precision,
    humidity double precision,
    co double precision,
    no2 double precision,
    o3 double precision,
    so2 double precision,
    pm2_5 double precision,
    pm10 double precision,
    us_epa_index int,
    gb_defra_index int,
    constraint london_pollution_pkey primary key (timestamp, location, country) 
);

create table if not exists pollution.uk (
    id serial primary key,
    "date" date,
    "hour" int,
    city_id int,
    country_id int,
    temp_c double precision,
    humidity double precision,
    co double precision,
    no2 double precision,
    o3 double precision,
    so2 double precision,
    pm2_5 double precision,
    pm10 double precision,
    UNIQUE (date, hour, city_id, country_id)
);

create table if not exists public.cities (
    id  serial primary key,
    name varchar(50)
);

create table if not exists public.countries (
    id  serial primary key,
    name varchar(50)
);

insert into public.cities (name) values
('London'),
('Manchester'),
('Glasgow'),
('Barcelona'),
('Guayaquil');

insert into public.countries (name) values
('United Kingdom'),
('Spain'),
('Ecuador');

create schema if not exists temp;