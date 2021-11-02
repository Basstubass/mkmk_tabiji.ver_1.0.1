-- SQLite
/*
BEGIN TRANSACTION;


CREATE TABLE IF NOT EXISTS "TRIPS" (
	"trips_id"	INTEGER NOT NULL UNIQUE,
	"trip_title"	TEXT NOT NULL,
	"route_url"	TEXT NOT NULL,
	"start_time" TIME NOT NULL,
	"user_id"	INTEGER NOT NULL,
	FOREIGN KEY("user_id") REFERENCES "USERS"("user_id"),
	PRIMARY KEY("trips_id")
);
CREATE TABLE IF NOT EXISTS "USERS" (
	"user_id"	INTEGER NOT NULL UNIQUE,
	"user_name"	TEXT NOT NULL,
	"password"	TEXT NOT NULL,
	PRIMARY KEY("user_id")
);
CREATE TABLE IF NOT EXISTS "FAVORITE_SITES" (
	"favorite_sites_id"	INTEGER NOT NULL UNIQUE,
	"trip_id"	INTEGER NOT NULL,
	"site_url"	TEXT NOT NULL,
	"site_name"	TEXT NOT NULL,
	"address"	TEXT NOT NULL,
	"hours"	TEXT NOT NULL,
	"phone_number"	INTEGER NOT NULL,
	"rating"	FLOAT NOT NULL,
	"review"	TEXT NOT NULL,
	"type"	TEXT NOT NULL,
	"picture_url"	TEXT NOT NULL,
	PRIMARY KEY("favorite_sites_id")
);
COMMIT;
*/