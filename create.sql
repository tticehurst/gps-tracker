-- gpstracker.readings definition

CREATE TABLE `readings` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `reading_time` timestamp(6) NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `lon` decimal(13,10) NOT NULL,
  `lat` decimal(13,10) NOT NULL,
  `geoloc` varchar(255) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;