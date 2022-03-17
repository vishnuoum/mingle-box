-- phpMyAdmin SQL Dump
-- version 5.1.1
-- https://www.phpmyadmin.net/
--
-- Host: localhost
-- Generation Time: Mar 17, 2022 at 05:26 PM
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
(3, 2, 1, '2022-03-16 16:14:54', '300000');

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
(1, 'hello3', 'hello', 'hello1@gmail.com', 'a665a45920422f9d417e4867efdc4fb8a04a1f3fff1fa07e998e86f7f7a27ae3', '2021-12-23', 'yes', NULL),
(8, 'Vishnu', 'UEC', 'hallellujah@gmail.com', 'a665a45920422f9d417e4867efdc4fb8a04a1f3fff1fa07e998e86f7f7a27ae3', '2021-12-29', 'yes', NULL);

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
(2, 'hello', '2022-03-04 14:50:49', 2, 'coder', 1, 'buyer'),
(3, 'hai', '2022-03-04 14:59:08', 2, 'coder', 1, 'buyer'),
(4, 'gg', '2022-03-08 14:46:37', 1, 'buyer', 2, 'coder'),
(5, 'hhh', '2022-03-08 15:06:01', 1, 'buyer', 2, 'coder'),
(6, 'ttt', '2022-03-08 15:06:13', 1, 'buyer', 2, 'coder'),
(7, 'gggg', '2022-03-08 15:06:31', 1, 'buyer', 2, 'coder'),
(8, 'jj', '2022-03-08 15:13:16', 1, 'buyer', 2, 'coder'),
(9, 'ii', '2022-03-08 15:13:46', 1, 'buyer', 2, 'coder'),
(10, 'jj', '2022-03-08 15:20:38', 1, 'buyer', 2, 'coder'),
(11, 'ggg', '2022-03-08 15:24:40', 1, 'buyer', 2, 'coder'),
(12, 'ggg', '2022-03-08 15:25:54', 1, 'buyer', 2, 'coder'),
(13, 'ggg', '2022-03-08 15:26:59', 1, 'buyer', 2, 'coder'),
(14, 'j', '2022-03-08 15:27:02', 1, 'buyer', 2, 'coder'),
(15, 'bbb', '2022-03-08 15:28:57', 1, 'buyer', 2, 'coder'),
(16, 'ff', '2022-03-08 15:30:27', 1, 'buyer', 2, 'coder'),
(17, 'tt', '2022-03-08 15:31:24', 1, 'buyer', 2, 'coder'),
(18, 'cc', '2022-03-08 15:31:38', 1, 'buyer', 2, 'coder'),
(19, 'hello', '2022-03-08 15:33:37', 1, 'buyer', 2, 'coder'),
(20, 'ddd', '2022-03-08 15:34:33', 1, 'buyer', 2, 'coder'),
(21, 'hh', '2022-03-08 15:38:26', 1, 'buyer', 2, 'coder'),
(22, 'ff', '2022-03-08 15:42:59', 1, 'buyer', 2, 'coder'),
(23, 'uu', '2022-03-08 15:44:54', 1, 'buyer', 2, 'coder'),
(24, 'ggg', '2022-03-08 15:47:43', 1, 'buyer', 2, 'coder'),
(25, 'uu', '2022-03-08 15:55:46', 1, 'buyer', 2, 'coder'),
(26, 'hh', '2022-03-08 15:56:26', 1, 'buyer', 2, 'coder'),
(27, 'hei', '2022-03-08 16:05:18', 1, 'buyer', 2, 'coder'),
(28, 'hhh', '2022-03-08 16:07:15', 1, 'buyer', 2, 'coder'),
(29, 'hh', '2022-03-08 16:12:29', 1, 'buyer', 2, 'coder'),
(30, 'hhi', '2022-03-08 16:12:54', 1, 'buyer', 2, 'coder'),
(31, 'gg', '2022-03-08 16:13:19', 1, 'buyer', 2, 'coder'),
(32, 'hh', '2022-03-08 16:15:19', 1, 'buyer', 2, 'coder'),
(33, 'xx', '2022-03-08 16:15:32', 1, 'buyer', 2, 'coder'),
(34, 'mm', '2022-03-08 16:16:26', 1, 'buyer', 2, 'coder'),
(35, 'dd', '2022-03-08 16:18:12', 1, 'buyer', 2, 'coder'),
(36, 'hhi', '2022-03-08 16:18:20', 1, 'buyer', 2, 'coder'),
(37, 'bb', '2022-03-08 16:18:57', 1, 'buyer', 2, 'coder'),
(38, 'gg', '2022-03-08 16:19:03', 1, 'buyer', 2, 'coder'),
(39, 'ygfh', '2022-03-08 16:19:11', 1, 'buyer', 2, 'coder'),
(40, 'yy', '2022-03-08 16:19:20', 1, 'buyer', 2, 'coder'),
(41, 'yy', '2022-03-08 16:22:20', 1, 'buyer', 2, 'coder'),
(42, 'hh', '2022-03-08 16:22:29', 1, 'buyer', 2, 'coder'),
(43, 'hi', '2022-03-08 16:24:09', 1, 'buyer', 2, 'coder'),
(44, 'tt', '2022-03-08 16:24:20', 1, 'buyer', 2, 'coder'),
(45, 'v', '2022-03-08 16:24:32', 1, 'buyer', 2, 'coder'),
(46, 'ii', '2022-03-08 16:34:21', 1, 'buyer', 2, 'coder'),
(47, 'gg', '2022-03-08 16:34:44', 1, 'buyer', 2, 'coder'),
(48, 'j', '2022-03-08 16:36:05', 1, 'buyer', 2, 'coder'),
(49, 'u', '2022-03-08 16:36:50', 1, 'buyer', 2, 'coder'),
(50, 'vv', '2022-03-08 17:06:10', 1, 'buyer', 2, 'coder'),
(51, 'ggg', '2022-03-08 17:16:36', 2, 'coder', 1, 'buyer'),
(52, 'gg', '2022-03-08 17:17:33', 2, 'coder', 1, 'buyer'),
(53, 'helloi', '2022-03-08 17:19:20', 2, 'coder', 1, 'buyer'),
(54, 'hey', '2022-03-08 17:20:32', 2, 'coder', 1, 'buyer'),
(55, 'oi', '2022-03-08 17:29:21', 1, 'buyer', 2, 'coder'),
(56, 'hh', '2022-03-08 17:32:01', 1, 'buyer', 2, 'coder'),
(57, 'hhi', '2022-03-08 17:32:13', 2, 'coder', 1, 'buyer'),
(58, 'hey', '2022-03-08 17:32:20', 1, 'buyer', 2, 'coder'),
(59, 'hello', '2022-03-08 17:32:27', 2, 'coder', 1, 'buyer'),
(60, 'da', '2022-03-08 17:32:36', 2, 'coder', 1, 'buyer'),
(61, 'da', '2022-03-08 17:32:50', 1, 'buyer', 2, 'coder'),
(62, 'hi', '2022-03-08 17:32:57', 2, 'coder', 1, 'buyer'),
(63, 'bye', '2022-03-08 17:33:06', 1, 'buyer', 2, 'coder'),
(64, 'hello', '2022-03-08 17:33:17', 1, 'buyer', 2, 'coder'),
(65, 'hey', '2022-03-15 15:59:52', 1, 'buyer', 2, 'coder'),
(66, 'hi', '2022-03-15 15:59:58', 2, 'coder', 1, 'buyer'),
(67, 'hello', '2022-03-15 16:00:02', 1, 'buyer', 2, 'coder'),
(68, 'hello', '2022-03-15 16:00:09', 1, 'buyer', 2, 'coder'),
(69, 'hi', '2022-03-15 16:00:14', 2, 'coder', 1, 'buyer'),
(70, 'hih', '2022-03-15 16:00:19', 1, 'buyer', 2, 'coder'),
(71, 'hi', '2022-03-15 16:00:20', 1, 'buyer', 2, 'coder'),
(72, 'hello', '2022-03-15 16:00:25', 2, 'coder', 1, 'buyer'),
(73, 'hi', '2022-03-15 17:24:21', 2, 'coder', 1, 'buyer'),
(74, 'fff', '2022-03-15 17:26:11', 2, 'coder', 1, 'buyer'),
(75, 'hei', '2022-03-15 17:26:24', 1, 'buyer', 2, 'coder'),
(76, 'gg', '2022-03-15 17:26:38', 1, 'buyer', 2, 'coder'),
(77, '  ', '2022-03-15 17:26:41', 2, 'coder', 1, 'buyer'),
(78, 'fff', '2022-03-15 17:28:35', 2, 'coder', 1, 'buyer'),
(79, 'hhh', '2022-03-15 17:28:40', 1, 'buyer', 2, 'coder'),
(80, 'hh', '2022-03-15 17:28:43', 1, 'buyer', 2, 'coder'),
(81, 'yyy', '2022-03-15 17:29:30', 2, 'coder', 1, 'buyer'),
(82, 'nn', '2022-03-15 17:29:42', 1, 'buyer', 2, 'coder'),
(83, 'kk', '2022-03-15 17:29:49', 2, 'coder', 1, 'buyer'),
(84, 'ttttggg', '2022-03-15 17:29:55', 1, 'buyer', 2, 'coder'),
(85, 'tttt', '2022-03-15 17:29:59', 2, 'coder', 1, 'buyer'),
(86, 'ggg', '2022-03-15 17:30:01', 2, 'coder', 1, 'buyer'),
(87, 'ji', '2022-03-15 17:30:25', 2, 'coder', 1, 'buyer'),
(88, 'he', '2022-03-15 17:30:37', 1, 'buyer', 2, 'coder'),
(89, 'ji', '2022-03-15 17:30:41', 2, 'coder', 1, 'buyer'),
(90, 'hi', '2022-03-15 17:38:10', 2, 'coder', 1, 'buyer'),
(91, 'hi', '2022-03-15 17:40:10', 1, 'buyer', 2, 'coder'),
(92, 'hei', '2022-03-15 17:40:19', 2, 'coder', 1, 'buyer'),
(93, 'hh', '2022-03-15 17:40:22', 1, 'buyer', 2, 'coder'),
(94, 'hhhhj', '2022-03-15 17:40:27', 2, 'coder', 1, 'buyer'),
(95, 'Interested', '2022-03-15 17:40:43', 2, 'coder', 1, 'buyer'),
(96, 'Interested', '2022-03-15 17:42:31', 2, 'coder', 1, 'buyer'),
(97, 'Interested in Needed Python Devs', '2022-03-15 17:44:31', 2, 'coder', 1, 'buyer'),
(98, 'Interested in TTS engine', '2022-03-15 17:45:21', 2, 'coder', 1, 'buyer'),
(99, 'Interested in Needed Python Devs 2', '2022-03-15 17:46:54', 2, 'coder', 1, 'buyer'),
(100, 'tt', '2022-03-16 05:41:16', 2, 'coder', 1, 'buyer'),
(101, 'jj', '2022-03-16 06:33:47', 2, 'coder', 1, 'buyer'),
(102, 'n', '2022-03-16 06:34:26', 2, 'coder', 1, 'buyer'),
(103, 'he', '2022-03-16 06:34:52', 2, 'coder', 1, 'buyer'),
(104, 'hhhh', '2022-03-16 06:34:59', 1, 'buyer', 2, 'coder'),
(105, 'ffffff', '2022-03-16 06:35:08', 2, 'coder', 1, 'buyer'),
(106, 'chj', '2022-03-16 06:35:19', 1, 'buyer', 2, 'coder'),
(107, 'hh', '2022-03-16 07:20:41', 1, 'buyer', 2, 'coder'),
(108, 'j', '2022-03-16 07:20:48', 2, 'coder', 1, 'buyer'),
(109, 'Hi', '2022-03-16 07:22:08', 1, 'buyer', 2, 'coder'),
(110, 'hey', '2022-03-16 16:14:11', 2, 'coder', 1, 'buyer');

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
(2, 'hello', 'hello@gmail.com', 'a665a45920422f9d417e4867efdc4fb8a04a1f3fff1fa07e998e86f7f7a27ae3', '[\"django\", \"flask\",\"python\"]', '2021-12-23', NULL),
(8, 'VM', 'hellohai@gmail.com', 'a665a45920422f9d417e4867efdc4fb8a04a1f3fff1fa07e998e86f7f7a27ae3', '[\"python\"]', '2021-12-29', NULL);

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
(10, 'List is a collection of data', 6);

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
(3, '25000', 1, 2, '2022-03-06 07:12:52', 'Mingle Box 3');

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
  `buyerId` int(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `projects`
--

INSERT INTO `projects` (`id`, `name`, `description`, `technology`, `timestamp`, `cost`, `finalCost`, `coderId`, `buyerId`) VALUES
(1, 'Mingle Box', 'hello', '[\"flask\"]', '2021-12-23 12:56:05', '15000', '28000', 2, 1),
(2, 'Agri', 'Agri', '[\"flask\"]', '2022-03-03 14:56:17', '2000', NULL, 2, NULL);

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
(6, 'What is list?', '10', 1);

-- --------------------------------------------------------

--
-- Table structure for table `requests`
--

CREATE TABLE `requests` (
  `id` int(255) NOT NULL,
  `name` varchar(50) NOT NULL,
  `description` text NOT NULL,
  `technology` longtext CHARACTER SET utf8mb4 COLLATE utf8mb4_bin NOT NULL CHECK (json_valid(`technology`)),
  `adddatetime` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp(),
  `buyerId` int(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `requests`
--

INSERT INTO `requests` (`id`, `name`, `description`, `technology`, `adddatetime`, `buyerId`) VALUES
(2, 'Mingle Box', 'hello', '[\"flask\"]', '2021-12-23 13:12:58', 1),
(3, 'TTS engine', 'hello', '[\"python\"]', '2021-12-30 13:54:37', 1),
(4, 'Needed Python Devs', 'Required python developers for project', '[\"python\"]', '2022-03-06 08:46:42', 1),
(5, 'Needed Python Devs 2', 'Mingle Box', '[\"python\", \"flask\"]', '2022-03-06 08:49:14', 1),
(6, 'Flask devs', 'Wanted Flask developers', '[\"flask\", \"python\"]', '2022-03-15 15:14:26', 1),
(7, 'Python', 'Python devs requried', '[\"python\"]', '2022-03-15 15:20:06', 1),
(8, 'Python devs needed', 'needed python devs for work', '[\"flask\"]', '2022-03-15 15:30:39', 1),
(9, 'python', 'python devs needed', '[\"python\"]', '2022-03-15 15:32:14', 1),
(10, 'flask devs', 'flask devs needed', '[\"flask\"]', '2022-03-15 15:39:43', 1),
(11, 'flask dev', 'flask', '[\"flask\"]', '2022-03-15 15:45:16', 1),
(12, 'python devs', 'python', '[\"python\"]', '2022-03-15 15:47:21', 1),
(13, 'TTS engine devs', 'TTS engine python developers', '[\"python\"]', '2022-03-15 15:52:12', 1);

-- --------------------------------------------------------

--
-- Table structure for table `responses`
--

CREATE TABLE `responses` (
  `id` int(255) NOT NULL,
  `coderId` int(255) NOT NULL,
  `requestId` int(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `responses`
--

INSERT INTO `responses` (`id`, `coderId`, `requestId`) VALUES
(1, 2, 2),
(3, 2, 5),
(2, 8, 2);

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
(2, 3, '75', 2),
(3, 4, '80', 2),
(5, 1, '100', 2),
(13, 1, '100', 8);

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
(2, 'node.js'),
(3, 'django'),
(4, 'flask');

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
  ADD PRIMARY KEY (`id`);

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
  MODIFY `id` int(255) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- AUTO_INCREMENT for table `buyers`
--
ALTER TABLE `buyers`
  MODIFY `id` int(255) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=9;

--
-- AUTO_INCREMENT for table `chat`
--
ALTER TABLE `chat`
  MODIFY `id` int(255) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=111;

--
-- AUTO_INCREMENT for table `coders`
--
ALTER TABLE `coders`
  MODIFY `id` int(255) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=9;

--
-- AUTO_INCREMENT for table `options`
--
ALTER TABLE `options`
  MODIFY `id` int(255) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;

--
-- AUTO_INCREMENT for table `payments`
--
ALTER TABLE `payments`
  MODIFY `id` int(255) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT for table `projects`
--
ALTER TABLE `projects`
  MODIFY `id` int(255) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT for table `questions`
--
ALTER TABLE `questions`
  MODIFY `id` int(255) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;

--
-- AUTO_INCREMENT for table `requests`
--
ALTER TABLE `requests`
  MODIFY `id` int(255) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=14;

--
-- AUTO_INCREMENT for table `responses`
--
ALTER TABLE `responses`
  MODIFY `id` int(255) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT for table `score`
--
ALTER TABLE `score`
  MODIFY `id` int(255) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=14;

--
-- AUTO_INCREMENT for table `technology`
--
ALTER TABLE `technology`
  MODIFY `id` int(255) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
