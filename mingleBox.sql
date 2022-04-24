-- phpMyAdmin SQL Dump
-- version 5.1.1
-- https://www.phpmyadmin.net/
--
-- Host: localhost
-- Generation Time: Apr 24, 2022 at 02:49 PM
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
(1, 1, 1, '2022-04-24 12:15:04', '6000'),
(2, 2, 1, '2022-04-24 12:43:33', '56000');

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
(1, 'Buyer', 'Buyer Company', 'buyer@gmail.com', '99f2bdf9942653ab32d9dfa0b43c72c3fbbb9679450fd965c590c224897b848a', '2022-04-24', 'yes', NULL);

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
(1, 'You won the bid for Python streaming project', '2022-04-24 12:15:14', 1, 'coder', 1, 'buyer'),
(2, 'You won the bid for Python Project', '2022-04-24 12:16:44', 1, 'buyer', 1, 'coder'),
(3, 'hello', '2022-04-24 12:17:53', 1, 'coder', 1, 'buyer'),
(4, 'hi there', '2022-04-24 12:17:59', 1, 'buyer', 1, 'coder'),
(5, 'when do you want the porject to be delivered?', '2022-04-24 12:18:23', 1, 'coder', 1, 'buyer'),
(6, 'is next week possible?', '2022-04-24 12:18:41', 1, 'buyer', 1, 'coder'),
(7, 'yes', '2022-04-24 12:18:50', 1, 'coder', 1, 'buyer'),
(8, 'ok then', '2022-04-24 12:19:00', 1, 'buyer', 1, 'coder'),
(9, 'expecting the complete project next week.!!', '2022-04-24 12:19:28', 1, 'buyer', 1, 'coder'),
(10, 'After the strict evaluation from our company side, we will issue the payment.', '2022-04-24 12:19:59', 1, 'buyer', 1, 'coder'),
(11, 'sure', '2022-04-24 12:20:07', 1, 'coder', 1, 'buyer');

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
(1, 'Coder', 'coder@gmail.com', '99f2bdf9942653ab32d9dfa0b43c72c3fbbb9679450fd965c590c224897b848a', '[\"python\", \"ML\"]', '2022-04-24', NULL);

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
(98, 'All of the above', 32),
(99, 'Computer learns itself', 33),
(100, 'Hard coding', 33),
(101, 'Manual coding', 33),
(102, 'None of the above', 33),
(103, 'A branch of machine learning', 34),
(104, 'A branch of computer coding', 34),
(105, 'A hard coding technique', 34),
(106, 'None of the above', 34),
(107, 'Yes', 35),
(108, 'Sometimes', 35),
(109, 'Never', 35),
(110, 'None of the above', 35),
(111, 'Supervised', 36),
(112, 'Unsupervised', 36),
(113, 'Semi-supervised', 36),
(114, 'Unsupervised', 36),
(115, 'Decision Tree', 37),
(116, 'Random Forest', 37),
(117, 'Logistic Regression', 37),
(118, 'K-Means', 37);

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
(1, '6000', 1, 1, '2022-04-24 12:16:05', 'Python streaming project payment.');

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
(1, 'Python streaming project', 'Python project', '[\"python\"]', '2022-04-24 12:14:22', '5000', '6000', 1, 1, '2022-04-24 17:45:13'),
(2, 'Machine Learning', 'Machine Learning Project for Coders', '[\"python\", \"ML\"]', '2022-04-24 12:43:06', '50000', NULL, 1, NULL, NULL);

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
(32, 'Arguments available in express route handler function', '98', 17),
(33, 'What is ML?', '99', 18),
(34, 'What is deep learning?', '103', 18),
(35, 'Does deep learning uses neurons?', '107', 18),
(36, 'Identify one which is not a type of learning', '113', 18),
(37, 'Which of the following algorithm uses unsupervised learning?', '118', 18);

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
(1, 'Python Project', '10000', 'Python project', '[\"python\"]', '2022-04-24 12:16:43', 1, 1, '9999', '2022-04-24 17:46:43'),
(2, 'Python backend', '60000', 'Python backend program', '[\"python\"]', '2022-04-24 12:21:31', 1, NULL, NULL, NULL);

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

--
-- Dumping data for table `responses`
--

INSERT INTO `responses` (`id`, `coderId`, `requestId`, `datetime`, `amount`) VALUES
(1, 1, 1, '2022-04-24 17:43:12', '9999'),
(2, 1, 2, '2022-04-24 17:51:56', '59000');

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
(1, 1, '100', 1),
(2, 18, '100', 1);

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
(17, 'express.js'),
(18, 'ML');

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
  ADD UNIQUE KEY `coderId` (`coderId`,`requestId`),
  ADD UNIQUE KEY `coderId_2` (`coderId`,`requestId`);

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
  MODIFY `id` int(255) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT for table `buyers`
--
ALTER TABLE `buyers`
  MODIFY `id` int(255) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `chat`
--
ALTER TABLE `chat`
  MODIFY `id` int(255) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=12;

--
-- AUTO_INCREMENT for table `coders`
--
ALTER TABLE `coders`
  MODIFY `id` int(255) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `options`
--
ALTER TABLE `options`
  MODIFY `id` int(255) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=119;

--
-- AUTO_INCREMENT for table `payments`
--
ALTER TABLE `payments`
  MODIFY `id` int(255) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `projects`
--
ALTER TABLE `projects`
  MODIFY `id` int(255) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT for table `questions`
--
ALTER TABLE `questions`
  MODIFY `id` int(255) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=38;

--
-- AUTO_INCREMENT for table `requests`
--
ALTER TABLE `requests`
  MODIFY `id` int(255) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT for table `responses`
--
ALTER TABLE `responses`
  MODIFY `id` int(255) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT for table `score`
--
ALTER TABLE `score`
  MODIFY `id` int(255) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT for table `technology`
--
ALTER TABLE `technology`
  MODIFY `id` int(255) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=19;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
