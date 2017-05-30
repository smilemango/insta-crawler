--for insta_users.sqlite3
BEGIN TRANSACTION;
CREATE TABLE "users" (
	`id`	INTEGER NOT NULL UNIQUE,
	`username`	TEXT NOT NULL UNIQUE,
	PRIMARY KEY(`id`)
);
COMMIT;
