CREATE TABLE IF NOT EXISTS `login` (

	`aadhaar_no` bigint(12) unsigned NOT NULL UNIQUE,
	`name` varchar(32) NOT NULL,
	`mobile_no` bigint(10) unsigned NOT NULL UNIQUE,
	`email` varchar(64) NOT NULL,
	`passwd` varchar(512) NOT NULL,
	`authority_level` ENUM('0', '1', '2', '3') NOT NULL,
	`notification_id` int unsigned NOT NULL DEFAULT 0,
	`city` varchar(64) NOT NULL,
	PRIMARY KEY (`aadhaar_no`)
);


CREATE TABLE IF NOT EXISTS `dam` (
	`dam_id` int unsigned NOT NULL AUTO_INCREMENT,
	`dam_name` varchar(64) NOT NULL UNIQUE,
	`nearest_city` varchar(32) NOT NULL,
	`state` varchar(32) NOT NULL,
	`year_of_completion` int NOT NULL,
	`river` varchar(32),
	`height` DOUBLE(20, 6) NOT NULL, -- m
	`length` DOUBLE(20, 6) NOT NULL, -- m
	`volume_content` DOUBLE(20, 6), -- 10^3 m^3
	`gross_storage_capacity` DOUBLE(20, 6) NOT NULL, -- km^3
	`reservoir_area` DOUBLE(20, 6), -- km^2
	`effective_storage_capacity` DOUBLE(20, 6), -- km^3
	`designed_spillway` DOUBLE(20, 6), -- m^3 / sec
	PRIMARY KEY (`dam_id`)
);


CREATE TABLE IF NOT EXISTS `dam_data` (
	`dam_data_id` int unsigned NOT NULL AUTO_INCREMENT,
	`seepage` ENUM('0', '1') NOT NULL,
	`cracks` ENUM('0', '1') NOT NULL,
	`erosion` ENUM('0', '1') NOT NULL,
	`gates_condition` ENUM('0', '1', '2') NOT NULL,
	`sluice_gates_condition` ENUM('0', '1', '2') NOT NULL,
	`max_flood_handled` int unsigned, -- m^3 / sec
	`energy_dissipator_condition` ENUM('0', '1', '2') NOT NULL,
	`instrument_condition` ENUM('0', '1', '2') NOT NULL,
	`latitude` DOUBLE(10, 6) NOT NULL,
	`longitude` DOUBLE(10, 6) NOT NULL,
	`time_stamp` TIMESTAMP,
	`descrip` varchar(512),
	`image1` blob,
	`image2` blob,
	`aadhaar_no` bigint(12) unsigned,
	`dam_id` int unsigned,
	`severity` ENUM('0', '1', '2'),
	FOREIGN KEY (`aadhaar_no`) REFERENCES `login`(`aadhaar_no`),
	FOREIGN KEY (`dam_id`) REFERENCES `dam`(`dam_id`),
	PRIMARY KEY(`dam_data_id`)
);
