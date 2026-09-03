-- --------------------------------------------------------
-- Host:                         127.0.0.1
-- Server version:               10.4.32-MariaDB - mariadb.org binary distribution
-- Server OS:                    Win64
-- HeidiSQL Version:             12.17.0.7270
-- --------------------------------------------------------

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET NAMES utf8 */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;


-- Dumping structure for table alembic_version
DROP TABLE IF EXISTS `alembic_version`;
CREATE TABLE IF NOT EXISTS `alembic_version` (
  `version_num` varchar(32) NOT NULL,
  PRIMARY KEY (`version_num`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Dumping data for table alembic_version: ~0 rows (approximately)
DELETE FROM `alembic_version`;

-- Dumping structure for table messages_chats
DROP TABLE IF EXISTS `messages_chats`;
CREATE TABLE IF NOT EXISTS `messages_chats` (
  `message_id` int(11) NOT NULL AUTO_INCREMENT,
  `sender_id` int(11) DEFAULT NULL,
  `sender_type` enum('artist','patron') DEFAULT NULL,
  `receiver_id` int(11) DEFAULT NULL,
  `receiver_type` enum('artist','patron') DEFAULT NULL,
  `message_text` mediumtext DEFAULT NULL,
  `message_date` datetime DEFAULT NULL,
  `is_read` tinyint(4) DEFAULT NULL,
  PRIMARY KEY (`message_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Dumping data for table messages_chats: ~0 rows (approximately)
DELETE FROM `messages_chats`;

-- Dumping structure for table order_purchase_details
DROP TABLE IF EXISTS `order_purchase_details`;
CREATE TABLE IF NOT EXISTS `order_purchase_details` (
  `purchase_id` int(11) NOT NULL AUTO_INCREMENT,
  `purchase_amt` decimal(10,2) DEFAULT NULL,
  `order_status` enum('pending','completed','cancelled') DEFAULT NULL,
  `order_id` int(11) DEFAULT NULL,
  `art_item_id` int(11) DEFAULT NULL,
  `stock_quantity` int(11) DEFAULT NULL,
  PRIMARY KEY (`purchase_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Dumping data for table order_purchase_details: ~0 rows (approximately)
DELETE FROM `order_purchase_details`;

-- Dumping structure for table orders_purchase
DROP TABLE IF EXISTS `orders_purchase`;
CREATE TABLE IF NOT EXISTS `orders_purchase` (
  `purchase_id` int(11) NOT NULL AUTO_INCREMENT,
  `purchase_amt` decimal(10,2) DEFAULT NULL,
  `order_status` enum('pending','processing','shipped','delivered','completed','cancelled') DEFAULT 'pending',
  `order_id` varchar(50) NOT NULL,
  `art_item_id` int(11) DEFAULT NULL,
  `stock_quantity` int(11) DEFAULT NULL,
  `artist_id` int(11) DEFAULT NULL,
  `patron_id` int(11) DEFAULT NULL,
  `delivery_address` varchar(500) DEFAULT NULL,
  `order_date` datetime DEFAULT NULL,
  PRIMARY KEY (`purchase_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Dumping data for table orders_purchase: ~0 rows (approximately)
DELETE FROM `orders_purchase`;

-- Dumping structure for table orders_purchases
DROP TABLE IF EXISTS `orders_purchases`;
CREATE TABLE IF NOT EXISTS `orders_purchases` (
  `order_id` int(11) NOT NULL AUTO_INCREMENT,
  `patron_ord_id` int(11) DEFAULT NULL,
  `artist_ord_id` int(11) DEFAULT NULL,
  `order_date` datetime DEFAULT NULL,
  `total_amount` int(11) DEFAULT NULL,
  `order_status` enum('pending','delivered') DEFAULT NULL,
  `delivery_address` varchar(505) DEFAULT NULL,
  PRIMARY KEY (`order_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Dumping data for table orders_purchases: ~0 rows (approximately)
DELETE FROM `orders_purchases`;

-- Dumping structure for table payments
DROP TABLE IF EXISTS `payments`;
CREATE TABLE IF NOT EXISTS `payments` (
  `payment_id` int(11) NOT NULL AUTO_INCREMENT,
  `patron_payment_id` int(11) DEFAULT NULL,
  `order_art_id` int(11) DEFAULT NULL,
  `date_payed` timestamp NULL DEFAULT NULL,
  `artist_payment_id` int(11) DEFAULT NULL,
  `payment_reference` varchar(95) DEFAULT NULL,
  `amount_payed` int(15) DEFAULT NULL,
  `payment_status` enum('pending','paid') DEFAULT NULL,
  PRIMARY KEY (`payment_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Dumping data for table payments: ~0 rows (approximately)
DELETE FROM `payments`;

-- Dumping structure for table ratings_reviews
DROP TABLE IF EXISTS `ratings_reviews`;
CREATE TABLE IF NOT EXISTS `ratings_reviews` (
  `ratings_id` int(11) NOT NULL AUTO_INCREMENT,
  `rating_score` tinyint(4) DEFAULT NULL,
  `rated_artist_id` int(11) DEFAULT NULL,
  `rated_art_id` int(11) DEFAULT NULL,
  `rated_by_id` int(11) DEFAULT NULL,
  `rating_date` datetime DEFAULT NULL,
  `comment` text DEFAULT NULL,
  PRIMARY KEY (`ratings_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Dumping data for table ratings_reviews: ~0 rows (approximately)
DELETE FROM `ratings_reviews`;

-- Dumping structure for table state
DROP TABLE IF EXISTS `state`;
CREATE TABLE IF NOT EXISTS `state` (
  `state_id` int(11) NOT NULL AUTO_INCREMENT,
  `state_name` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`state_id`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Dumping data for table state: ~8 rows (approximately)
DELETE FROM `state`;
INSERT INTO `state` (`state_id`, `state_name`) VALUES
	(1, 'Lagos'),
	(2, 'Abuja'),
	(3, 'Kano'),
	(4, 'Oyo'),
	(5, 'Rivers'),
	(6, 'Kaduna'),
	(7, 'Enugu'),
	(8, 'Anambra');

-- Dumping structure for table tb_admin
DROP TABLE IF EXISTS `tb_admin`;
CREATE TABLE IF NOT EXISTS `tb_admin` (
  `admin_id` int(11) NOT NULL AUTO_INCREMENT,
  `admin_fullname` varchar(150) DEFAULT NULL,
  `admin_email` varchar(200) DEFAULT NULL,
  `admin_password` varchar(255) NOT NULL,
  `admin_lastlogged` timestamp NULL DEFAULT NULL,
  `is_active` tinyint(1) DEFAULT 1,
  PRIMARY KEY (`admin_id`)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Dumping data for table tb_admin: ~1 rows (approximately)
DELETE FROM `tb_admin`;
INSERT INTO `tb_admin` (`admin_id`, `admin_fullname`, `admin_email`, `admin_password`, `admin_lastlogged`, `is_active`) VALUES
	(1, 'Admin User', 'admin@talentbridge.com', 'scrypt:32768:8:1$nTp0zWJlgoqnLs8E$b8febc6c40db3590209e0a5ce50d259bd1ddeb8c80541467e16b3fc897ba2e914b2856832bf89e1c6e40ee7dcce5c701b938895300ed91bcd6458df56ef7ba7b', NULL, 1);

-- Dumping structure for table tb_art_type
DROP TABLE IF EXISTS `tb_art_type`;
CREATE TABLE IF NOT EXISTS `tb_art_type` (
  `art_type_id` int(11) NOT NULL AUTO_INCREMENT,
  `art_type_name` varchar(70) DEFAULT NULL,
  PRIMARY KEY (`art_type_id`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Dumping data for table tb_art_type: ~8 rows (approximately)
DELETE FROM `tb_art_type`;
INSERT INTO `tb_art_type` (`art_type_id`, `art_type_name`) VALUES
	(1, 'Painting'),
	(2, 'Sculpture'),
	(3, 'Bead Making'),
	(4, 'Woodwork'),
	(5, 'Metalwork'),
	(6, 'Digital Art'),
	(7, 'Photography'),
	(8, 'Inventions');

-- Dumping structure for table tb_artists
DROP TABLE IF EXISTS `tb_artists`;
CREATE TABLE IF NOT EXISTS `tb_artists` (
  `artist_id` int(11) NOT NULL AUTO_INCREMENT,
  `artist_fname` varchar(100) DEFAULT NULL,
  `artist_lname` varchar(100) DEFAULT NULL,
  `artist_phone` varchar(200) DEFAULT NULL,
  `artist_mail` varchar(100) DEFAULT NULL,
  `artist_password` varchar(255) DEFAULT NULL,
  `artist_bio` varchar(1000) DEFAULT NULL,
  `artist_art` varchar(200) DEFAULT NULL,
  `artist_reg_date` datetime DEFAULT NULL,
  `artist_state_id` int(11) DEFAULT NULL,
  `is_active` tinyint(1) DEFAULT 1,
  PRIMARY KEY (`artist_id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Dumping data for table tb_artists: ~5 rows (approximately)
DELETE FROM `tb_artists`;
INSERT INTO `tb_artists` (`artist_id`, `artist_fname`, `artist_lname`, `artist_phone`, `artist_mail`, `artist_password`, `artist_bio`, `artist_art`, `artist_reg_date`, `artist_state_id`, `is_active`) VALUES
	(1, 'Raven', 'Diahl', NULL, 'rdiahl@gmail.com', 'ef797c8118f02dfb649607dd5d3f8c7623048c9c063d532cc95c5ed7a898a64f', NULL, NULL, '2026-07-20 14:59:21', NULL, 1),
	(2, 'Maxim', 'Feries', NULL, 'max@gmail.com', '4e20613ec3a63732f98630b9429e1600d47a08f059496d39ffd353f0c3038f39', NULL, NULL, '2026-07-20 18:03:13', NULL, 1),
	(3, 'Greg', 'Baltimore', NULL, 'ggb@gmail.com', '0c88cc86a73aa7c4058ff7c0e31d6f105c0ca3575d5a68e060e95d9c84a607a9', NULL, NULL, '2026-07-20 18:26:29', NULL, 1),
	(4, 'John', 'Redol', NULL, 'jdol@gmail.com', '67b55d55dddfbbeb5d8e1ae4dac71dea37b3e67e1639e56b8046c2fa6543e1c6', NULL, NULL, '2026-07-22 10:04:40', NULL, 1),
	(5, 'Evern', 'Dall', NULL, 'ed@gmail.com', '9c528dbcc589566cafc4f0044b10a01e524007f035186ee11a5d1a3e6737cb7d', NULL, NULL, '2026-07-22 11:41:15', NULL, 1);

-- Dumping structure for table tb_arts
DROP TABLE IF EXISTS `tb_arts`;
CREATE TABLE IF NOT EXISTS `tb_arts` (
  `art_id` int(11) NOT NULL AUTO_INCREMENT,
  `art_title` varchar(100) DEFAULT NULL,
  `art_desc` varchar(5000) DEFAULT NULL,
  `art_price` decimal(10,2) DEFAULT NULL,
  `art_image` varchar(300) DEFAULT NULL,
  `art_type_id` int(11) DEFAULT NULL,
  `artwork_status` enum('available','sold') DEFAULT NULL,
  `artist_art_id` int(11) DEFAULT NULL,
  `art_date` datetime DEFAULT NULL,
  `stock_qty` int(11) DEFAULT NULL,
  PRIMARY KEY (`art_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Dumping data for table tb_arts: ~0 rows (approximately)
DELETE FROM `tb_arts`;

-- Dumping structure for table tb_patrons
DROP TABLE IF EXISTS `tb_patrons`;
CREATE TABLE IF NOT EXISTS `tb_patrons` (
  `patron_id` int(11) NOT NULL AUTO_INCREMENT,
  `patron_fname` varchar(100) DEFAULT NULL,
  `patron_lname` varchar(100) DEFAULT NULL,
  `patron_mail` varchar(100) DEFAULT NULL,
  `patron_password` varchar(255) DEFAULT NULL,
  `patron_type` enum('buyer','scout','business') DEFAULT NULL,
  `patron_regdate` datetime DEFAULT NULL,
  `patron_state_id` int(11) DEFAULT NULL,
  `is_active` tinyint(1) DEFAULT 1,
  PRIMARY KEY (`patron_id`)
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Dumping data for table tb_patrons: ~2 rows (approximately)
DELETE FROM `tb_patrons`;
INSERT INTO `tb_patrons` (`patron_id`, `patron_fname`, `patron_lname`, `patron_mail`, `patron_password`, `patron_type`, `patron_regdate`, `patron_state_id`, `is_active`) VALUES
	(1, 'Jolm', 'Dessers', 'jdess@gmail.com', '4071572612d01c01f89b61bd04c889ab355b6071d02d6c42969551cff5187211', 'buyer', '2026-07-22 11:53:15', NULL, 1),
	(2, 'Telco', 'Calonti', 'telco@gmail.com', 'c129db8be8904b40ac21c9cf5d9f5c0e24ef455d1d7a7bbfd7049fc6dc9d2429', 'buyer', '2026-07-23 20:46:41', NULL, 1);

-- Dumping structure for table user_search_track
DROP TABLE IF EXISTS `user_search_track`;
CREATE TABLE IF NOT EXISTS `user_search_track` (
  `user_search_id` int(11) NOT NULL AUTO_INCREMENT,
  `artist_id` int(11) DEFAULT NULL,
  `patron_id` int(11) DEFAULT NULL,
  `search_term` varchar(255) DEFAULT NULL,
  `search_date` datetime DEFAULT NULL,
  PRIMARY KEY (`user_search_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- Dumping data for table user_search_track: ~0 rows (approximately)
DELETE FROM `user_search_track`;

/*!40103 SET TIME_ZONE=IFNULL(@OLD_TIME_ZONE, 'system') */;
/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IFNULL(@OLD_FOREIGN_KEY_CHECKS, 1) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40111 SET SQL_NOTES=IFNULL(@OLD_SQL_NOTES, 1) */;
