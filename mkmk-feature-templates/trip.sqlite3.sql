/*
BEGIN TRANSACTION;
CREATE TABLE IF NOT EXISTS "trips" (
	"trips_id"	INTEGER NOT NULL UNIQUE,
	"trip_title" TEXT NOT NULL,
	"route_url"	TEXT,
	"start_time" DATETIME,
	"start_place" TEXT,
	"goal_place" TEXT,
	"means" TEXT,
	"user_id"	INTEGER NOT NULL,
	FOREIGN KEY("user_id") REFERENCES "users"("id"),
	PRIMARY KEY("trips_id")
	UNIQUE("trip_title", "user_id")
);
CREATE TABLE IF NOT EXISTS "users" (
	"user_id"	INTEGER NOT NULL UNIQUE,
	"user_name"	TEXT NOT NULL,
	"password"	TEXT NOT NULL,
	PRIMARY KEY("user_id")
);
CREATE TABLE IF NOT EXISTS "favorite_sites" (
	"favorite_sites_id"	INTEGER NOT NULL UNIQUE,
	"trips_id"	INTEGER NOT NULL,
	"site_url"	TEXT,
	"site_name"	TEXT NOT NULL,
	"address"	TEXT,
	"hours"	TEXT,
	"phone_number"	INTEGER,
	"rating"	FLOAT,
	"review"	TEXT,
	"type"	TEXT,
	"picture_url"	TEXT,
	FOREIGN KEY("trips_id") REFERENCES "trips"("trips_id") ON DELETE CASCADE,
	PRIMARY KEY("favorite_sites_id")
);
COMMIT; 
*/