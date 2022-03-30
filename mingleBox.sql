-- phpMyAdmin SQL Dump
-- version 5.1.1
-- https://www.phpmyadmin.net/
--
-- Host: localhost
-- Generation Time: Mar 30, 2022 at 08:33 PM
-- Server version: 10.4.21-MariaDB
-- PHP Version: 8.0.10

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `mingleBox`
--

-- --------------------------------------------------------

--
-- Table structure for table `bids`
--

CREATE TABLE `bids` (
  `id` int(255) NOT NULL,
  `projectId` int(255) NOT NULL,
  `buyerId` int(255) NOT NULL,
  `datetime` timestamp NOT NULL DEFAULT current_timestamp(),
  `amount` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `bids`
--

INSERT INTO `bids` (`id`, `projectId`, `buyerId`, `datetime`, `amount`) VALUES
(1, 1, 1, '2022-03-06 10:35:19', '28000'),
(3, 2, 1, '2022-03-16 16:14:54', '300000'),
(7, 3, 1, '2022-03-23 15:13:30', '1500'),
(8, 4, 1, '2022-03-24 12:44:39', '2000');

-- --------------------------------------------------------

--
-- Table structure for table `buyers`
--

CREATE TABLE `buyers` (
  `id` int(255) NOT NULL,
  `username` varchar(50) NOT NULL,
  `company` varchar(100) NOT NULL,
  `mail` varchar(255) NOT NULL,
  `password` varchar(255) NOT NULL,
  `date` date NOT NULL DEFAULT current_timestamp(),
  `verified` varchar(5) NOT NULL DEFAULT 'no',
  `pushId` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `buyers`
--

INSERT INTO `buyers` (`id`, `username`, `company`, `mail`, `password`, `date`, `verified`, `pushId`) VALUES
(1, 'hello3', 'hello', 'hello1@gmail.com', '1bdc9965d79dfa166dc6110cc8a7eb4082aaf00a592d2ca820277fca9240fe81', '2021-12-23', 'yes', NULL),
(8, 'Vishnu', 'UEC', 'hallellujah@gmail.com', 'a665a45920422f9d417e4867efdc4fb8a04a1f3fff1fa07e998e86f7f7a27ae3', '2021-12-29', 'yes', NULL),
(9, '123', '123', '1237@gmail.com', 'a665a45920422f9d417e4867efdc4fb8a04a1f3fff1fa07e998e86f7f7a27ae3', '2022-03-18', 'yes', NULL),
(10, 'hello', 'Hellohat', 'hellohellohello@gmail.com', '1bdc9965d79dfa166dc6110cc8a7eb4082aaf00a592d2ca820277fca9240fe81', '2022-03-29', 'no', NULL);

-- --------------------------------------------------------

--
-- Table structure for table `chat`
--

CREATE TABLE `chat` (
  `id` int(255) NOT NULL,
  `message` text NOT NULL,
  `datetime` timestamp NOT NULL DEFAULT current_timestamp(),
  `sender` int(255) NOT NULL,
  `senderType` varchar(10) NOT NULL,
  `receiver` int(255) NOT NULL,
  `receiverType` varchar(10) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `chat`
--

INSERT INTO `chat` (`id`, `message`, `datetime`, `sender`, `senderType`, `receiver`, `receiverType`) VALUES
(145, 'Hi', '2022-03-20 17:39:12', 1, 'buyer', 2, 'coder'),
(146, 'hello', '2022-03-20 17:39:23', 1, 'buyer', 2, 'coder'),
(147, 'hi', '2022-03-20 17:39:29', 2, 'coder', 1, 'buyer'),
(148, 'Hi', '2022-03-20 17:40:04', 9, 'buyer', 2, 'coder'),
(149, '😂', '2022-03-20 17:40:45', 9, 'buyer', 2, 'coder'),
(150, '😆', '2022-03-20 17:40:49', 9, 'buyer', 2, 'coder'),
(151, 'hey', '2022-03-20 17:41:02', 2, 'coder', 9, 'buyer'),
(152, 'hi', '2022-03-22 15:18:29', 1, 'buyer', 2, 'coder'),
(153, 'hey', '2022-03-22 15:18:35', 1, 'buyer', 2, 'coder'),
(154, 'hello', '2022-03-22 15:18:39', 1, 'buyer', 2, 'coder'),
(155, 'You won the bid for Project', '2022-03-24 12:54:18', 2, 'coder', 1, 'buyer'),
(156, 'hello', '2022-03-24 12:54:57', 2, 'coder', 1, 'buyer'),
(157, 'You won the bid for Project', '2022-03-24 12:56:08', 2, 'coder', 1, 'buyer'),
(158, 'hello', '2022-03-24 13:12:46', 1, 'buyer', 2, 'coder'),
(159, 'helk', '2022-03-24 13:13:38', 2, 'coder', 9, 'buyer'),
(160, 'hi', '2022-03-24 13:15:18', 1, 'buyer', 2, 'coder'),
(161, 'Hi', '2022-03-24 13:17:43', 1, 'buyer', 9, 'coder'),
(162, 'Interested in Project', '2022-03-24 13:21:02', 2, 'coder', 1, 'buyer'),
(163, 'Interested in Project', '2022-03-24 13:23:45', 2, 'coder', 1, 'buyer'),
(164, 'hello', '2022-03-24 15:29:31', 2, 'coder', 1, 'buyer'),
(165, 'hello', '2022-03-24 15:36:10', 2, 'coder', 1, 'buyer');

-- --------------------------------------------------------

--
-- Table structure for table `coders`
--

CREATE TABLE `coders` (
  `id` int(255) NOT NULL,
  `username` varchar(50) NOT NULL,
  `mail` varchar(255) NOT NULL,
  `password` varchar(255) NOT NULL,
  `technology` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin DEFAULT '[]',
  `date` date NOT NULL DEFAULT current_timestamp(),
  `pushId` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `coders`
--

INSERT INTO `coders` (`id`, `username`, `mail`, `password`, `technology`, `date`, `pushId`) VALUES
(2, 'hello', 'hello@gmail.com', '99f2bdf9942653ab32d9dfa0b43c72c3fbbb9679450fd965c590c224897b848a', '[\"django\", \"flask\", \"python\", \"express.js\"]', '2021-12-23', NULL),
(8, 'VM', 'hellohai@gmail.com', 'a665a45920422f9d417e4867efdc4fb8a04a1f3fff1fa07e998e86f7f7a27ae3', '[\"python\"]', '2021-12-29', NULL),
(9, '123', '123@gmail.com', 'a665a45920422f9d417e4867efdc4fb8a04a1f3fff1fa07e998e86f7f7a27ae3', '[\"python\", \"django\", \"flask\", \"express.js\"]', '2022-03-18', NULL),
(14, 'Hello', 'hellohello@gmail.com', 'a665a45920422f9d417e4867efdc4fb8a04a1f3fff1fa07e998e86f7f7a27ae3', '[]', '2022-03-22', NULL),
(15, 'haihai', 'helloi@gmail.com', '1bdc9965d79dfa166dc6110cc8a7eb4082aaf00a592d2ca820277fca9240fe81', '[]', '2022-03-30', NULL);

-- --------------------------------------------------------

--
-- Table structure for table `options`
--

CREATE TABLE `options` (
  `id` int(255) NOT NULL,
  `optionText` text NOT NULL,
  `questionId` int(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `options`
--

INSERT INTO `options` (`id`, `optionText`, `questionId`) VALUES
(1, 'List is a set', 2),
(2, 'List is a collection of data', 2),
(3, 'List is a set', 3),
(4, 'List is a collection of data', 3),
(5, 'List is a set', 4),
(6, 'List is a collection of data', 4),
(7, 'List is a set', 5),
(8, 'List is a collection of data', 5),
(9, 'List is a set', 6),
(10, 'List is a collection of data', 6),
(75, 'Framework', 26),
(76, 'Library', 26),
(77, 'Micro framework', 27),
(78, 'Library', 27),
(79, 'Web app framework', 28),
(80, 'Library', 28),
(81, 'url', 28),
(82, 'site', 28),
(83, 'Python', 29),
(84, 'Node.js', 29),
(85, 'Java', 29),
(86, 'Lua', 29),
(87, 'Light weight', 30),
(88, 'Minimal', 30),
(89, 'Flexible', 30),
(90, 'All of the above', 30),
(91, 'Frontend', 31),
(92, 'Backend', 31),
(93, 'Both', 31),
(94, 'None of the above', 31),
(95, 'req', 32),
(96, 'res', 32),
(97, 'next', 32),
(98, 'All of the above', 32);

-- --------------------------------------------------------

--
-- Table structure for table `payments`
--

CREATE TABLE `payments` (
  `id` int(255) NOT NULL,
  `amount` varchar(50) NOT NULL,
  `senderId` int(255) NOT NULL,
  `receiverId` int(255) NOT NULL,
  `datetime` timestamp NOT NULL DEFAULT current_timestamp(),
  `description` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `payments`
--

INSERT INTO `payments` (`id`, `amount`, `senderId`, `receiverId`, `datetime`, `description`) VALUES
(1, '2500', 1, 2, '2021-12-30 16:43:14', 'Mingle Box payment'),
(2, '2500', 1, 2, '2022-03-06 07:11:04', 'Mingle Box 2'),
(3, '25000', 1, 2, '2022-03-06 07:12:52', 'Mingle Box 3'),
(4, '300000', 1, 2, '2022-03-23 13:33:30', 'Agri App payment'),
(5, '100', 1, 2, '2022-03-23 14:01:24', 'test'),
(6, '100', 1, 2, '2022-03-23 14:58:08', 'Test'),
(7, '2000', 1, 2, '2022-03-24 13:04:17', 'Project fund'),
(8, '100', 1, 2, '2022-03-24 13:06:40', 'test');

-- --------------------------------------------------------

--
-- Table structure for table `projects`
--

CREATE TABLE `projects` (
  `id` int(255) NOT NULL,
  `name` varchar(50) NOT NULL,
  `description` text NOT NULL,
  `technology` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL CHECK (json_valid(`technology`)),
  `timestamp` timestamp NOT NULL DEFAULT current_timestamp(),
  `cost` varchar(50) NOT NULL,
  `finalCost` varchar(50) DEFAULT NULL,
  `coderId` int(255) NOT NULL,
  `buyerId` int(255) DEFAULT NULL,
  `completeDate` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `projects`
--

INSERT INTO `projects` (`id`, `name`, `description`, `technology`, `timestamp`, `cost`, `finalCost`, `coderId`, `buyerId`, `completeDate`) VALUES
(1, 'Mingle Box', 'hello', '[\"flask\"]', '2021-12-23 12:56:05', '15000', '28000', 2, 1, '2022-03-10 19:05:41'),
(2, 'App', 'App', '[\"flask\"]', '2022-03-03 14:56:17', '2000', '300000', 2, 1, '2022-03-17 19:05:48'),
(3, 'Tesseract', 'Tesseract OCR', '[\"python\", \"flask\"]', '2022-03-23 15:11:44', '1500', '1500', 2, 1, '2022-03-23 20:43:48'),
(4, 'Project', 'Project', '[\"python\"]', '2022-03-24 12:43:30', '1000', '2000', 2, 1, '2022-03-24 18:26:07'),
(5, 'hello', 'hello', '[\"python\"]', '2022-03-30 18:13:26', '1200', NULL, 2, NULL, NULL);

-- --------------------------------------------------------

--
-- Table structure for table `questions`
--

CREATE TABLE `questions` (
  `id` int(255) NOT NULL,
  `question` text NOT NULL,
  `answer` varchar(50) NOT NULL,
  `technologyId` int(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `questions`
--

INSERT INTO `questions` (`id`, `question`, `answer`, `technologyId`) VALUES
(2, 'What is list?', '2', 1),
(3, 'What is list?', '4', 1),
(4, 'What is list?', '6', 1),
(5, 'What is list?', '8', 1),
(6, 'What is list?', '10', 1),
(26, 'Django is a.......?', '75', 3),
(27, 'Flask is .......?', '77', 4),
(28, 'What is express?', '79', 17),
(29, 'Express is used along?', '84', 17),
(30, 'Features of express?', '90', 17),
(31, 'Express is used in', '92', 17),
(32, 'Arguments available in express route handler function', '98', 17);

-- --------------------------------------------------------

--
-- Table structure for table `requests`
--

CREATE TABLE `requests` (
  `id` int(255) NOT NULL,
  `name` varchar(50) NOT NULL,
  `cost` varchar(255) NOT NULL,
  `description` text NOT NULL,
  `technology` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL CHECK (json_valid(`technology`)),
  `adddatetime` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  `buyerId` int(255) NOT NULL,
  `coderId` int(11) DEFAULT NULL,
  `finalCost` varchar(255) DEFAULT NULL,
  `completeDate` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `requests`
--

INSERT INTO `requests` (`id`, `name`, `cost`, `description`, `technology`, `adddatetime`, `buyerId`, `coderId`, `finalCost`, `completeDate`) VALUES
(2, 'Mingle Box', '10000', 'hello', '[\"flask\"]', '2022-03-30 17:20:36', 1, NULL, NULL, NULL),
(3, 'TTS engine', '10000', 'hello', '[\"python\"]', '2022-03-30 17:20:36', 1, NULL, NULL, NULL),
(4, 'Needed Python Devs', '10000', 'Required python developers for project', '[\"python\"]', '2022-03-30 17:20:36', 1, NULL, NULL, NULL),
(5, 'Needed Python Devs 2', '10000', 'Mingle Box', '[\"python\", \"flask\"]', '2022-03-30 17:20:36', 1, NULL, NULL, NULL),
(6, 'Flask devs', '10000', 'Wanted Flask developers', '[\"flask\", \"python\"]', '2022-03-30 17:20:36', 1, NULL, NULL, NULL),
(7, 'Python', '10000', 'Python devs requried', '[\"python\"]', '2022-03-30 17:20:36', 1, NULL, NULL, NULL),
(8, 'Python devs needed', '10000', 'needed python devs for work', '[\"flask\"]', '2022-03-30 17:20:36', 1, NULL, NULL, NULL),
(9, 'python', '10000', 'python devs needed', '[\"python\"]', '2022-03-30 17:20:36', 1, NULL, NULL, NULL),
(10, 'flask devs', '10000', 'flask devs needed', '[\"flask\"]', '2022-03-30 17:20:36', 1, NULL, NULL, NULL),
(11, 'flask dev', '10000', 'flask', '[\"flask\"]', '2022-03-30 17:20:36', 1, NULL, NULL, NULL),
(12, 'python devs', '10000', 'python', '[\"python\"]', '2022-03-30 17:20:36', 1, NULL, NULL, NULL),
(13, 'TTS engine devs', '10000', 'TTS engine python developers', '[\"python\"]', '2022-03-30 17:20:36', 1, NULL, NULL, NULL),
(14, 'Project', '10000', 'Project', '[\"python\"]', '2022-03-30 17:20:36', 1, NULL, NULL, NULL),
(15, 'Hello', '1000', 'hello', '[\"python\"]', '2022-03-30 17:39:35', 1, NULL, NULL, NULL);

-- --------------------------------------------------------

--
-- Table structure for table `responses`
--

CREATE TABLE `responses` (
  `id` int(255) NOT NULL,
  `coderId` int(255) NOT NULL,
  `requestId` int(255) NOT NULL,
  `datetime` datetime NOT NULL DEFAULT current_timestamp(),
  `amount` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- --------------------------------------------------------

--
-- Table structure for table `score`
--

CREATE TABLE `score` (
  `id` int(255) NOT NULL,
  `technologyId` int(255) NOT NULL,
  `score` varchar(50) NOT NULL,
  `coderId` int(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `score`
--

INSERT INTO `score` (`id`, `technologyId`, `score`, `coderId`) VALUES
(2, 3, '100', 2),
(3, 4, '100', 2),
(5, 1, '100', 2),
(13, 1, '100', 8),
(14, 17, '100', 2),
(18, 1, '80', 9),
(19, 3, '100', 9),
(20, 4, '100', 9),
(21, 17, '100', 9);

-- --------------------------------------------------------

--
-- Table structure for table `technology`
--

CREATE TABLE `technology` (
  `id` int(255) NOT NULL,
  `technology` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `technology`
--

INSERT INTO `technology` (`id`, `technology`) VALUES
(1, 'python'),
(3, 'django'),
(4, 'flask'),
(17, 'express.js');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `bids`
--
ALTER TABLE `bids`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `projectId` (`projectId`,`buyerId`);

--
-- Indexes for table `buyers`
--
ALTER TABLE `buyers`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `mail` (`mail`);

--
-- Indexes for table `chat`
--
ALTER TABLE `chat`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `coders`
--
ALTER TABLE `coders`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `mail` (`mail`);

--
-- Indexes for table `options`
--
ALTER TABLE `options`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `payments`
--
ALTER TABLE `payments`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `projects`
--
ALTER TABLE `projects`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `questions`
--
ALTER TABLE `questions`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `requests`
--
ALTER TABLE `requests`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `responses`
--
ALTER TABLE `responses`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `coderId` (`coderId`,`requestId`);

--
-- Indexes for table `score`
--
ALTER TABLE `score`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `technologyId` (`technologyId`,`coderId`);

--
-- Indexes for table `technology`
--
ALTER TABLE `technology`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `bids`
--
ALTER TABLE `bids`
  MODIFY `id` int(255) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=10;

--
-- AUTO_INCREMENT for table `buyers`
--
ALTER TABLE `buyers`
  MODIFY `id` int(255) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;

--
-- AUTO_INCREMENT for table `chat`
--
ALTER TABLE `chat`
  MODIFY `id` int(255) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=166;

--
-- AUTO_INCREMENT for table `coders`
--
ALTER TABLE `coders`
  MODIFY `id` int(255) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=16;

--
-- AUTO_INCREMENT for table `options`
--
ALTER TABLE `options`
  MODIFY `id` int(255) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=99;

--
-- AUTO_INCREMENT for table `payments`
--
ALTER TABLE `payments`
  MODIFY `id` int(255) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=9;

--
-- AUTO_INCREMENT for table `projects`
--
ALTER TABLE `projects`
  MODIFY `id` int(255) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT for table `questions`
--
ALTER TABLE `questions`
  MODIFY `id` int(255) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=33;

--
-- AUTO_INCREMENT for table `requests`
--
ALTER TABLE `requests`
  MODIFY `id` int(255) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=16;

--
-- AUTO_INCREMENT for table `responses`
--
ALTER TABLE `responses`
  MODIFY `id` int(255) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT for table `score`
--
ALTER TABLE `score`
  MODIFY `id` int(255) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=22;

--
-- AUTO_INCREMENT for table `technology`
--
ALTER TABLE `technology`
  MODIFY `id` int(255) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=18;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
