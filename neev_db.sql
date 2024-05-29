-- phpMyAdmin SQL Dump
-- version 5.0.4
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Apr 03, 2024 at 09:15 PM
-- Server version: 10.4.17-MariaDB
-- PHP Version: 8.0.2

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `test`
--

-- --------------------------------------------------------

--
-- Table structure for table `active_courses`
--

CREATE TABLE `active_courses` (
  `i_id` int(11) NOT NULL,
  `c_id` int(11) NOT NULL,
  `start_date` date NOT NULL,
  `end_date` date NOT NULL,
  `active_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `active_courses`
--

INSERT INTO `active_courses` (`i_id`, `c_id`, `start_date`, `end_date`, `active_id`) VALUES
(101, 101, '2024-03-31', '2024-04-30', 1),
(103, 101, '2024-04-01', '2024-04-30', 2),
(105, 102, '2024-04-06', '2024-04-30', 3),
(105, 101, '2024-05-01', '2024-05-30', 4);

-- --------------------------------------------------------

--
-- Table structure for table `admin`
--

CREATE TABLE `admin` (
  `AD_ID` int(11) NOT NULL,
  `Email` varchar(255) NOT NULL,
  `Name` varchar(255) NOT NULL,
  `Password` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `admin`
--

INSERT INTO `admin` (`AD_ID`, `Email`, `Name`, `Password`) VALUES
(1, 'admin1@example.com', 'John Doe', 'johndoe123');

-- --------------------------------------------------------

--
-- Table structure for table `course`
--

CREATE TABLE `course` (
  `C_ID` int(11) NOT NULL,
  `Course_name` varchar(255) DEFAULT NULL,
  `Details` varchar(255) DEFAULT NULL,
  `Venue` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `course`
--

INSERT INTO `course` (`C_ID`, `Course_name`, `Details`, `Venue`) VALUES
(101, 'Mathematics', 'Basic of the Math', 'Room 202'),
(102, 'Literature', 'Shakespearean Plays Analysis', 'Auditorium'),
(103, 'History', 'World War II Overview', 'Room 101'),
(104, 'Computer Science', 'Python Programming Basics', 'Room 8'),
(105, 'Biology', 'Cellular Biology', 'Lab 301'),
(1232, 'Designing Course', 'Student will learn different art forms', 'Room 202'),
(3532, 'Creative Designing', 'Where student will learn different types of art forms', 'room 203');

-- --------------------------------------------------------

--
-- Table structure for table `donation`
--

CREATE TABLE `donation` (
  `D_ID` int(11) NOT NULL,
  `Donor_Name` varchar(255) DEFAULT NULL,
  `Amount` decimal(10,2) DEFAULT NULL,
  `Details` varchar(255) DEFAULT NULL,
  `Phone_No` varchar(15) DEFAULT NULL,
  `Email` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `donation`
--

INSERT INTO `donation` (`D_ID`, `Donor_Name`, `Amount`, `Details`, `Phone_No`, `Email`) VALUES
(0, 'Nidhi', '123.00', 'fgf f', '9865796780', 'himanitrivedi1874@gmail.com'),
(11, 'Joey Tribianni', '100.00', 'Transaction ID', '123-456-789', 'johntribianni@example.com'),
(12, 'Jane Smith', '250.00', 'Transaction ID', '987-654-321', 'janesmith@example.com'),
(23, 'Alice Lee', '50.00', 'Transaction ID', '555-123-456', 'alicelee@example.com'),
(54, 'Bob Johnson', '150.00', 'Transaction ID', '111-222-333', 'bobjohnson@example.com'),
(55, 'Sarah Brown', '75.00', 'Transaction ID', '444-555-666', 'sarahbrown@example.com');

-- --------------------------------------------------------

--
-- Table structure for table `funds`
--

CREATE TABLE `funds` (
  `D_ID` int(11) NOT NULL,
  `AD_ID` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `funds`
--

INSERT INTO `funds` (`D_ID`, `AD_ID`) VALUES
(11, 1),
(12, 1);

-- --------------------------------------------------------

--
-- Table structure for table `instructors`
--

CREATE TABLE `instructors` (
  `I_ID` int(11) NOT NULL,
  `Name` varchar(255) NOT NULL,
  `Email` varchar(255) NOT NULL,
  `Phone_No` varchar(12) NOT NULL,
  `Gender` enum('Male','Female') NOT NULL,
  `Identification_ID` varchar(9) NOT NULL,
  `Type` enum('Full','Part') NOT NULL,
  `S_ID` int(11) NOT NULL,
  `M_ID` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `instructors`
--

INSERT INTO `instructors` (`I_ID`, `Name`, `Email`, `Phone_No`, `Gender`, `Identification_ID`, `Type`, `S_ID`, `M_ID`) VALUES
(0, 'XYZ', 'himanitrivedi1874@gmail.com', '9327035695', 'Female', '24325436', 'Full', 12, 0),
(101, 'John Doe', 'johndoe@example.com', '9056745645', 'Female', '123456789', 'Part', 12, 1),
(102, 'Jane Smith', 'janesmith@example.com', '987-654-321', 'Female', '987654321', 'Part', 12, 1),
(103, 'Alex Lee', 'alexlee@example.com', '456-789-012', 'Male', '456789012', 'Full', 12, 1),
(105, 'Mark Kim', 'markkim@example.com', '369-258-147', 'Male', '369258147', 'Part', 12, 1);

-- --------------------------------------------------------

--
-- Table structure for table `neev_members`
--

CREATE TABLE `neev_members` (
  `M_id` int(11) NOT NULL,
  `Name` varchar(255) DEFAULT NULL,
  `Email` varchar(255) DEFAULT NULL,
  `Identification_ID` bigint(20) DEFAULT NULL,
  `Gender` enum('Male','Female') DEFAULT NULL,
  `Designation` varchar(255) DEFAULT NULL,
  `Photo` varchar(255) DEFAULT NULL,
  `Password` varchar(255) DEFAULT NULL,
  `Phone_No` varchar(20) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `neev_members`
--

INSERT INTO `neev_members` (`M_id`, `Name`, `Email`, `Identification_ID`, `Gender`, `Designation`, `Photo`, `Password`, `Phone_No`) VALUES
(3, 'Michael Lee', 'michael@example.com', 1357924680, 'Male', 'Analyst', 'video call template1920.png', 'password3', '967557578468'),
(4, 'Sarah Brown', 'sarah@example.com', 2468013579, 'Female', 'Designer', 'logo_final1127.jpeg', 'password4', '789-123-4560'),
(5, 'David Kim', 'david@example.com', 3692581470, 'Male', 'Intern in XyZ', 'bulb_off3721.jpg', 'password5', '321-654-9870'),
(8, 'Nidhi', 'nidhitrivedi912@gamilc.com', 123, 'Female', '243253', 'logo_final1877.jpeg', 'dsdgdsg', '9865796780');

-- --------------------------------------------------------

--
-- Table structure for table `students`
--

CREATE TABLE `students` (
  `S_ID` int(11) NOT NULL,
  `Name` varchar(255) DEFAULT NULL,
  `Email` varchar(255) DEFAULT NULL,
  `Identification_ID` bigint(20) DEFAULT NULL,
  `Gender` enum('Male','Female') DEFAULT NULL,
  `Photo` varchar(255) DEFAULT NULL,
  `phone_no` varchar(10) NOT NULL,
  `Family_Background` varchar(255) DEFAULT NULL,
  `Address` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `students`
--

INSERT INTO `students` (`S_ID`, `Name`, `Email`, `Identification_ID`, `Gender`, `Photo`, `phone_no`, `Family_Background`, `Address`) VALUES
(1, 'Johny Pal', 'john@example.com', 1234567890, 'Male', 'photo.jpg', '', 'Upper class', '123 Main St, City'),
(3, 'Michael Lee', 'michael@example.com', 4567890123, 'Male', 'image.jpg', '', 'Lower class', '789 Oak St, Village'),
(5, 'David Wilson', 'david@example.com', 1357902468, 'Male', 'photo2.jpg', '', 'Lower middle class', '654 Cedar St, Town'),
(6, 'Emily Davis', 'emily@example.com', 2468013579, 'Female', 'pic2.jpg', '', 'Upper class', '987 Maple St, City'),
(8, 'Olivia Taylor', 'olivia@example.com', 7024579135, 'Female', 'img2.jpg', '', 'Middle class', '753 Elm St, Town'),
(9, 'James Brown', 'james@example.com', 147852369, 'Male', 'ht_logo399.png', '2465778065', 'Lower Middle class', '159 Cedar St, City'),
(10, 'Sophia Garcia', 'sophia@example.com', 3691478520, 'Female', 'cress_zero2099.png', '9327035695', 'Upper middle class', '852 Pine St, Town'),
(11, 'himani_1874', 'himanitrivedi1874@gmail.com', 2346, 'Male', 'bulb1447.jpg', '9327035695', 'Upper class', 'sfd gsg'),
(12, NULL, NULL, NULL, NULL, NULL, '', NULL, NULL);

-- --------------------------------------------------------

--
-- Table structure for table `student_course`
--

CREATE TABLE `student_course` (
  `S_ID` int(11) NOT NULL,
  `active_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `student_course`
--

INSERT INTO `student_course` (`S_ID`, `active_id`) VALUES
(1, 1),
(3, 1),
(1, 4),
(9, 4),
(3, 4),
(3, 2);

-- --------------------------------------------------------

--
-- Table structure for table `volunteer`
--

CREATE TABLE `volunteer` (
  `V_ID` int(11) NOT NULL,
  `Name` varchar(255) DEFAULT NULL,
  `Email` varchar(255) DEFAULT NULL,
  `Identification_ID` bigint(20) DEFAULT NULL,
  `Gender` varchar(10) DEFAULT NULL,
  `Photo` varchar(255) DEFAULT NULL,
  `Phone_No` varchar(20) DEFAULT NULL,
  `M_ID` int(11) DEFAULT NULL,
  `Address` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `volunteer`
--

INSERT INTO `volunteer` (`V_ID`, `Name`, `Email`, `Identification_ID`, `Gender`, `Photo`, `Phone_No`, `M_ID`, `Address`) VALUES
(1, 'Steve Smith', 'steve@example.com', 123456789, 'male', 'cross3084.png', '8934567089', 1, '123 Main St, City'),
(4, 'Sarah Davis', 'sarah@example.com', 456789012, 'female', 'bulb_off2770.jpg', '9089786547', 4, '321 Pine St, County'),
(6, 'Himani', 'himanitrivedi1874@gmail.com', 2354646, 'female', 'cress_zero1470.png', '9327035695', NULL, 'Ahme');

-- --------------------------------------------------------

--
-- Table structure for table `volunteer_course`
--

CREATE TABLE `volunteer_course` (
  `V_ID` int(11) NOT NULL,
  `active_id` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

--
-- Dumping data for table `volunteer_course`
--

INSERT INTO `volunteer_course` (`V_ID`, `active_id`) VALUES
(1, 1),
(1, 2),
(4, 4);

--
-- Indexes for dumped tables
--

--
-- Indexes for table `active_courses`
--
ALTER TABLE `active_courses`
  ADD PRIMARY KEY (`active_id`),
  ADD KEY `c_id` (`c_id`),
  ADD KEY `instructor` (`i_id`);

--
-- Indexes for table `admin`
--
ALTER TABLE `admin`
  ADD PRIMARY KEY (`AD_ID`);

--
-- Indexes for table `course`
--
ALTER TABLE `course`
  ADD PRIMARY KEY (`C_ID`);

--
-- Indexes for table `donation`
--
ALTER TABLE `donation`
  ADD PRIMARY KEY (`D_ID`);

--
-- Indexes for table `funds`
--
ALTER TABLE `funds`
  ADD PRIMARY KEY (`D_ID`,`AD_ID`),
  ADD KEY `AD_ID` (`AD_ID`);

--
-- Indexes for table `instructors`
--
ALTER TABLE `instructors`
  ADD PRIMARY KEY (`I_ID`);

--
-- Indexes for table `neev_members`
--
ALTER TABLE `neev_members`
  ADD PRIMARY KEY (`M_id`);

--
-- Indexes for table `students`
--
ALTER TABLE `students`
  ADD PRIMARY KEY (`S_ID`);

--
-- Indexes for table `student_course`
--
ALTER TABLE `student_course`
  ADD KEY `course_add` (`active_id`),
  ADD KEY `student_id` (`S_ID`);

--
-- Indexes for table `volunteer`
--
ALTER TABLE `volunteer`
  ADD PRIMARY KEY (`V_ID`),
  ADD KEY `M_ID` (`M_ID`);

--
-- Indexes for table `volunteer_course`
--
ALTER TABLE `volunteer_course`
  ADD KEY `enroll_course` (`active_id`),
  ADD KEY `volunteer_id` (`V_ID`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `active_courses`
--
ALTER TABLE `active_courses`
  MODIFY `active_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT for table `admin`
--
ALTER TABLE `admin`
  MODIFY `AD_ID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `neev_members`
--
ALTER TABLE `neev_members`
  MODIFY `M_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=11;

--
-- AUTO_INCREMENT for table `students`
--
ALTER TABLE `students`
  MODIFY `S_ID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=13;

--
-- AUTO_INCREMENT for table `volunteer`
--
ALTER TABLE `volunteer`
  MODIFY `V_ID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `active_courses`
--
ALTER TABLE `active_courses`
  ADD CONSTRAINT `c_id` FOREIGN KEY (`c_id`) REFERENCES `course` (`C_ID`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `instructor` FOREIGN KEY (`i_id`) REFERENCES `instructors` (`I_ID`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `funds`
--
ALTER TABLE `funds`
  ADD CONSTRAINT `funds_ibfk_1` FOREIGN KEY (`D_ID`) REFERENCES `donation` (`D_ID`),
  ADD CONSTRAINT `funds_ibfk_2` FOREIGN KEY (`AD_ID`) REFERENCES `admin` (`AD_ID`);

--
-- Constraints for table `student_course`
--
ALTER TABLE `student_course`
  ADD CONSTRAINT `course_add` FOREIGN KEY (`active_id`) REFERENCES `active_courses` (`active_id`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `student_id` FOREIGN KEY (`S_ID`) REFERENCES `students` (`S_ID`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `volunteer_course`
--
ALTER TABLE `volunteer_course`
  ADD CONSTRAINT `enroll_course` FOREIGN KEY (`active_id`) REFERENCES `active_courses` (`active_id`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `volunteer_id` FOREIGN KEY (`V_ID`) REFERENCES `volunteer` (`V_ID`) ON DELETE CASCADE ON UPDATE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
