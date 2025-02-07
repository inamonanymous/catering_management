-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Feb 07, 2025 at 05:25 PM
-- Server version: 10.4.32-MariaDB
-- PHP Version: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `catering_management`
--

-- --------------------------------------------------------

--
-- Table structure for table `alembic_version`
--

CREATE TABLE `alembic_version` (
  `version_num` varchar(32) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `alembic_version`
--

INSERT INTO `alembic_version` (`version_num`) VALUES
('bbaafe78cb07');

-- --------------------------------------------------------

--
-- Table structure for table `bookings`
--

CREATE TABLE `bookings` (
  `booking_id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `status` enum('to-pay','processing','completed') DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT current_timestamp(),
  `updated_at` timestamp NULL DEFAULT current_timestamp(),
  `total_price` decimal(10,2) NOT NULL,
  `event_id` int(11) DEFAULT NULL,
  `package_id` int(11) DEFAULT NULL,
  `payment_id` int(11) DEFAULT NULL,
  `paid_amount` decimal(10,2) NOT NULL DEFAULT 0.00
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `bookings`
--

INSERT INTO `bookings` (`booking_id`, `user_id`, `status`, `created_at`, `updated_at`, `total_price`, `event_id`, `package_id`, `payment_id`, `paid_amount`) VALUES
(20, 1, 'to-pay', '2025-02-07 16:04:23', '2025-02-07 16:04:23', 100000.00, 32, NULL, NULL, 0.00);

-- --------------------------------------------------------

--
-- Table structure for table `event_details`
--

CREATE TABLE `event_details` (
  `event_id` int(11) NOT NULL,
  `event_name` varchar(100) NOT NULL,
  `number_of_guests` int(11) NOT NULL,
  `event_date` datetime NOT NULL,
  `event_location` varchar(255) NOT NULL,
  `created_at` timestamp NULL DEFAULT current_timestamp(),
  `updated_at` timestamp NULL DEFAULT current_timestamp(),
  `food_time` time NOT NULL,
  `event_theme` varchar(40) NOT NULL,
  `event_color` varchar(40) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `event_details`
--

INSERT INTO `event_details` (`event_id`, `event_name`, `number_of_guests`, `event_date`, `event_location`, `created_at`, `updated_at`, `food_time`, `event_theme`, `event_color`) VALUES
(32, 'Stephen birthday', 1000, '2025-02-19 00:00:00', 'baguio', '2025-02-07 16:04:23', '2025-02-07 16:04:23', '00:07:00', 'a', 'a');

-- --------------------------------------------------------

--
-- Table structure for table `event_menu_choices`
--

CREATE TABLE `event_menu_choices` (
  `choice_id` int(11) NOT NULL,
  `menu_id` int(11) NOT NULL,
  `event_id` int(11) NOT NULL,
  `quantity` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `event_menu_choices`
--

INSERT INTO `event_menu_choices` (`choice_id`, `menu_id`, `event_id`, `quantity`) VALUES
(46, 1, 32, 1000);

-- --------------------------------------------------------

--
-- Table structure for table `menu`
--

CREATE TABLE `menu` (
  `menu_id` int(11) NOT NULL,
  `menu_name` varchar(50) NOT NULL,
  `description` text DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT current_timestamp(),
  `price` decimal(10,2) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `menu`
--

INSERT INTO `menu` (`menu_id`, `menu_name`, `description`, `created_at`, `price`) VALUES
(1, 'Standard Buffet', 'Includes main course, drinks, and dessert', '2025-02-07 08:11:37', 100.00),
(2, 'Vegetarian Menu', 'A selection of vegetarian dishes', '2025-02-07 08:11:37', 200.00),
(3, 'BBQ Grill', 'Grilled meats and sides', '2025-02-07 08:11:37', 300.00);

-- --------------------------------------------------------

--
-- Table structure for table `menu_items`
--

CREATE TABLE `menu_items` (
  `item_id` int(11) NOT NULL,
  `menu_id` int(11) NOT NULL,
  `category` enum('appetizer','main','drink','dessert','custom') DEFAULT NULL,
  `item_name` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `menu_items`
--

INSERT INTO `menu_items` (`item_id`, `menu_id`, `category`, `item_name`) VALUES
(1, 1, 'main', 'Roast Chicken'),
(2, 1, 'drink', 'Iced Tea'),
(3, 2, 'main', 'Vegetable Stir Fry'),
(4, 3, 'main', 'BBQ Ribs');

-- --------------------------------------------------------

--
-- Table structure for table `packages`
--

CREATE TABLE `packages` (
  `package_id` int(11) NOT NULL,
  `package_name` varchar(100) NOT NULL,
  `description` text DEFAULT NULL,
  `price` decimal(10,2) NOT NULL,
  `created_at` timestamp NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `packages`
--

INSERT INTO `packages` (`package_id`, `package_name`, `description`, `price`, `created_at`) VALUES
(1, 'Wedding Package', 'Includes full catering & venue setup', 5000.00, '2025-02-07 08:10:30'),
(2, 'Birthday Package', 'Catering for birthdays with decorations', 3000.00, '2025-02-07 08:10:30');

-- --------------------------------------------------------

--
-- Table structure for table `payments`
--

CREATE TABLE `payments` (
  `payment_id` int(11) NOT NULL,
  `payment_date` timestamp NULL DEFAULT current_timestamp(),
  `payment_method` enum('gcash','maya','bank_transfer') NOT NULL,
  `user_id` int(11) NOT NULL,
  `amount` decimal(10,2) NOT NULL,
  `payment_status` enum('pending','completed','failed') NOT NULL,
  `reference_no` varchar(20) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `payments`
--

INSERT INTO `payments` (`payment_id`, `payment_date`, `payment_method`, `user_id`, `amount`, `payment_status`, `reference_no`) VALUES
(17, '2025-02-07 16:09:09', 'gcash', 1, 50000.00, 'pending', '123123');

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE `users` (
  `user_id` int(11) NOT NULL,
  `username` varchar(50) NOT NULL,
  `password_hash` varchar(255) NOT NULL,
  `email` varchar(100) NOT NULL,
  `phone_number` varchar(100) NOT NULL,
  `phone_number2` varchar(100) DEFAULT NULL,
  `created_at` timestamp NULL DEFAULT current_timestamp(),
  `role` enum('admin','customer') NOT NULL,
  `firstname` varchar(255) NOT NULL,
  `middlename` varchar(255) NOT NULL,
  `lastname` varchar(255) NOT NULL,
  `suffix` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`user_id`, `username`, `password_hash`, `email`, `phone_number`, `phone_number2`, `created_at`, `role`, `firstname`, `middlename`, `lastname`, `suffix`) VALUES
(1, 'admin', 'scrypt:32768:8:1$tS8h2gat5BIWovJa$3c0ce02b21caa524c24ad1c045a5697c70821511a1ef208f81b94b91ccb7aa86d48d87affedc068fda8729d98c0c9f26892c73018b801b1bc67aed0528225415', 'domain@domain.com', '0912', '0912', '2025-01-27 13:12:28', 'customer', 'first', 'middle', 'last', 'iv'),
(5, 'admin1', 'scrypt:32768:8:1$yO096vuuHzn7tAJP$8f208d86524c0918a1ae3816b8902b2afbe38c8e45dff09dc56f75badf7126fc7a69f1085ba9a81b5c5df5c507a9e78f57bb4de85dcce8b62d24bb77c633bf11', 'domain1@domain.com', '09121', '0912', '2025-01-27 13:13:36', 'customer', 'first', 'middle', 'last', 'iv'),
(6, 'user', 'scrypt:32768:8:1$kxuYiNokPyWsmipR$3dc29ecbee483c9f16de908341f0bb09c472ed9c9036a813b0b576a2b42943c420aff9b2f48cb44f42e1698675716a5c8a37df480b4200b05494797c6c484bb5', 'stephenonline25@gmail.com', '09159035852', '09159035852', '2025-02-07 07:51:53', 'customer', 'first', 'middle', 'last', ''),
(7, 'a', 'scrypt:32768:8:1$N4J8jLiIiCL3FQjY$5aca158c29d7b84ce2662e31c06e23e9e6890a8dcf5e5a513139a513663202447268e2a2212c0d6c249c7b30d35aa394486cf753a70ee03991f1203d16c88951', 'a@gmaill.com', '000', '000', '2025-02-07 07:58:01', 'customer', 'a', 'a', 'a', 'a');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `alembic_version`
--
ALTER TABLE `alembic_version`
  ADD PRIMARY KEY (`version_num`);

--
-- Indexes for table `bookings`
--
ALTER TABLE `bookings`
  ADD PRIMARY KEY (`booking_id`),
  ADD KEY `user_id` (`user_id`),
  ADD KEY `event_id` (`event_id`),
  ADD KEY `package_id` (`package_id`),
  ADD KEY `payment_id` (`payment_id`);

--
-- Indexes for table `event_details`
--
ALTER TABLE `event_details`
  ADD PRIMARY KEY (`event_id`);

--
-- Indexes for table `event_menu_choices`
--
ALTER TABLE `event_menu_choices`
  ADD PRIMARY KEY (`choice_id`),
  ADD KEY `menu_id` (`menu_id`),
  ADD KEY `event_id` (`event_id`);

--
-- Indexes for table `menu`
--
ALTER TABLE `menu`
  ADD PRIMARY KEY (`menu_id`);

--
-- Indexes for table `menu_items`
--
ALTER TABLE `menu_items`
  ADD PRIMARY KEY (`item_id`),
  ADD KEY `menu_id` (`menu_id`);

--
-- Indexes for table `packages`
--
ALTER TABLE `packages`
  ADD PRIMARY KEY (`package_id`);

--
-- Indexes for table `payments`
--
ALTER TABLE `payments`
  ADD PRIMARY KEY (`payment_id`),
  ADD UNIQUE KEY `reference_no` (`reference_no`),
  ADD KEY `user_id` (`user_id`);

--
-- Indexes for table `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`user_id`),
  ADD UNIQUE KEY `username` (`username`),
  ADD UNIQUE KEY `email` (`email`),
  ADD UNIQUE KEY `phone_number` (`phone_number`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `bookings`
--
ALTER TABLE `bookings`
  MODIFY `booking_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=21;

--
-- AUTO_INCREMENT for table `event_details`
--
ALTER TABLE `event_details`
  MODIFY `event_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=33;

--
-- AUTO_INCREMENT for table `event_menu_choices`
--
ALTER TABLE `event_menu_choices`
  MODIFY `choice_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=47;

--
-- AUTO_INCREMENT for table `menu`
--
ALTER TABLE `menu`
  MODIFY `menu_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT for table `menu_items`
--
ALTER TABLE `menu_items`
  MODIFY `item_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- AUTO_INCREMENT for table `packages`
--
ALTER TABLE `packages`
  MODIFY `package_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT for table `payments`
--
ALTER TABLE `payments`
  MODIFY `payment_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=18;

--
-- AUTO_INCREMENT for table `users`
--
ALTER TABLE `users`
  MODIFY `user_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `bookings`
--
ALTER TABLE `bookings`
  ADD CONSTRAINT `bookings_ibfk_2` FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`),
  ADD CONSTRAINT `bookings_ibfk_3` FOREIGN KEY (`event_id`) REFERENCES `event_details` (`event_id`),
  ADD CONSTRAINT `bookings_ibfk_4` FOREIGN KEY (`package_id`) REFERENCES `packages` (`package_id`),
  ADD CONSTRAINT `bookings_ibfk_5` FOREIGN KEY (`payment_id`) REFERENCES `payments` (`payment_id`);

--
-- Constraints for table `event_menu_choices`
--
ALTER TABLE `event_menu_choices`
  ADD CONSTRAINT `event_menu_choices_ibfk_1` FOREIGN KEY (`menu_id`) REFERENCES `menu` (`menu_id`),
  ADD CONSTRAINT `event_menu_choices_ibfk_2` FOREIGN KEY (`event_id`) REFERENCES `event_details` (`event_id`);

--
-- Constraints for table `menu_items`
--
ALTER TABLE `menu_items`
  ADD CONSTRAINT `menu_items_ibfk_1` FOREIGN KEY (`menu_id`) REFERENCES `menu` (`menu_id`);

--
-- Constraints for table `payments`
--
ALTER TABLE `payments`
  ADD CONSTRAINT `payments_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
