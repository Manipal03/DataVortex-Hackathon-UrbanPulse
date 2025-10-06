-- UrbanPulse AI schema
create table if not exists public.detections (
	id uuid primary key default gen_random_uuid(),
	timestamp timestamptz default now(),
	vehicle_type text,
	confidence double precision,
	bbox jsonb,
	lat double precision,
	lon double precision
);

create table if not exists public.traffic_signals (
	id text primary key,
	status text,
	last_updated timestamptz default now()
);

create table if not exists public.routes (
	id uuid primary key default gen_random_uuid(),
	name text,
	coordinates jsonb
);

create table if not exists public.users (
	id uuid primary key,
	email text unique,
	role text
);
