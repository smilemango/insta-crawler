--for insta_user-relations.sqlite3
BEGIN TRANSACTION;
CREATE TABLE "users" (
	`id`	INTEGER NOT NULL UNIQUE,
	`username`	TEXT UNIQUE,
	`full_name`	TEXT,
	PRIMARY KEY(`id`)
);
CREATE TABLE `relations` (
	`user_id`	INTEGER NOT NULL,
	`follow_id`	INTEGER NOT NULL,
	PRIMARY KEY(`user_id`,`follow_id`)
);
CREATE INDEX `users_idx_username` ON `users` (`username` ASC);
COMMIT;
