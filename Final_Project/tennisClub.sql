-- phpMyAdmin SQL Dump
-- version 5.2.0
-- https://www.phpmyadmin.net/
--
-- 主机： localhost:8889
-- 生成日期： 2023-06-21 11:35:04
-- 服务器版本： 5.7.39
-- PHP 版本： 7.4.33

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- 数据库： `tennisClub`
--

-- --------------------------------------------------------

--
-- 表的结构 `Challenge`
--

CREATE TABLE `Challenge` (
  `CID` int(11) NOT NULL,
  `ChallengerMEID` int(11) NOT NULL,
  `ChallengedMEID` int(11) NOT NULL,
  `DateOfChallenge` datetime NOT NULL,
  `Status` int(1) DEFAULT NULL,
  `Notes` varchar(100) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- 转存表中的数据 `Challenge`
--

INSERT INTO `Challenge` (`CID`, `ChallengerMEID`, `ChallengedMEID`, `DateOfChallenge`, `Status`, `Notes`) VALUES
(1, 1, 2, '2023-06-20 00:00:00', 0, NULL),
(3, 1, 2, '2023-06-20 00:00:00', 0, 'lets have a match at monday'),
(4, 1, 4, '2023-06-20 00:00:00', 0, 'hello mr wang'),
(5, 1, 1, '2023-06-20 00:00:00', 0, ' come on!!!'),
(7, 2, 4, '2023-06-21 18:02:35', 0, 'go match today!'),
(8, 2, 1, '2023-06-21 18:02:49', 0, 'Long time no match!');

-- --------------------------------------------------------

--
-- 表的结构 `member`
--

CREATE TABLE `member` (
  `MEID` int(11) NOT NULL,
  `FirstName` varchar(50) NOT NULL,
  `LastName` varchar(50) DEFAULT NULL,
  `Email` varchar(50) NOT NULL,
  `MPassword` varchar(30) NOT NULL,
  `Phone` varchar(20) NOT NULL,
  `Age` int(11) NOT NULL,
  `Gender` varchar(10) NOT NULL,
  `UTR` float NOT NULL,
  `DateOfCreation` date NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- 转存表中的数据 `member`
--

INSERT INTO `member` (`MEID`, `FirstName`, `LastName`, `Email`, `MPassword`, `Phone`, `Age`, `Gender`, `UTR`, `DateOfCreation`) VALUES
(1, 'WENTIAN', 'lv', '2404830642@qq.com', '123456789', '13548333395', 12, 'F', 12, '2023-06-17'),
(2, 'hua', 'flora', 'floraluo@163.com', '123456780', '12345666678', 14, 'F', 13, '2023-06-17'),
(4, 'dk', 'wang', 'dk@google.com', '123780271048012046', '90878333312', 23, 'M', 4, '2023-06-17'),
(5, 'henry', 'shi', 'shi@163.com', '990880890787', '09842900293', 20, 'M', 5, '2023-06-17'),
(6, 'JOE', 'ESTRADA', 'newark@google.com', 'nihao1230123', '0300074321', 64, 'M', 14, '2023-06-17'),
(7, 'MARIAH', 'DODGE', 'Wilmington@126.com', 'qweasdzxc', '55553932', 34, 'F', 3, '2023-06-17'),
(8, 'ROBERTO', 'MORALES', 'master@qq.com', '0921-12 34 65', '062108460', 20, 'M', 1, '2023-06-17'),
(9, 'LUKE', 'BRAZZI', 'JAPAN@come.com', '15000001213', '77788989', 34, 'F', 14, '2023-06-17'),
(10, 'TOM', 'DYSON', 'TOM@swufe.edu.cn', 'wersdfxcv@', '09811922', 30, 'M', 7, '2023-06-18'),
(11, 'Lrting', 'Zhan', 'lrting@google.com', 'poi123ijn', '13568036616', 45, 'F', 6, '2023-06-18'),
(13, 'NORAH', 'HAI', 'showper@126.com', '//qwertyuio', '082611933', 34, 'F', 6, '2023-06-19'),
(14, 'test1', '', 'test@qq.com', '@#$//098unt,1', '90889616', 40, 'M', 4, '2023-06-19'),
(18, 'testforjump', 'yy', 'jumpgo@google.com', 'jumpgo@google', '0728082422', 27, 'F', 10, '2023-06-19'),
(20, 'trytry', 'ha', 'try10086@163.com', 'aaaaawuuuutian', '886778112', 29, 'M', 15, '2023-06-19'),
(21, 'opp', 'qq', 'telunsu@126.com', 'qwertyuiop', '1234560099', 40, 'M', 1, '2023-06-19');

-- --------------------------------------------------------

--
-- 表的结构 `Membership`
--

CREATE TABLE `Membership` (
  `MSID` int(11) NOT NULL,
  `MEID` int(11) NOT NULL,
  `StartDate` date NOT NULL,
  `EndDate` date NOT NULL,
  `InvoiceDate` date NOT NULL,
  `DueDate` date NOT NULL,
  `Amount` decimal(10,0) NOT NULL,
  `PaidDate` date DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- --------------------------------------------------------

--
-- 表的结构 `TMatch`
--

CREATE TABLE `TMatch` (
  `MAID` int(11) NOT NULL,
  `CID` int(11) DEFAULT NULL,
  `DateOfMatch` datetime NOT NULL,
  `MEID1Set1Score` int(1) NOT NULL,
  `MEID2Set1Score` int(1) NOT NULL,
  `MEID1Set2Score` int(1) DEFAULT NULL,
  `MEID2Set2Score` int(1) DEFAULT NULL,
  `MEID1Set3Score` int(1) DEFAULT NULL,
  `MEID2Set3Score` int(1) DEFAULT NULL,
  `WinnerMEID` int(11) DEFAULT NULL,
  `LoserMEID` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

--
-- 转存表中的数据 `TMatch`
--

INSERT INTO `TMatch` (`MAID`, `CID`, `DateOfMatch`, `MEID1Set1Score`, `MEID2Set1Score`, `MEID1Set2Score`, `MEID2Set2Score`, `MEID1Set3Score`, `MEID2Set3Score`, `WinnerMEID`, `LoserMEID`) VALUES
(1, 1, '2023-06-20 11:40:29', 1, 1, 1, 1, 1, 1, 1, 2),
(2, 1, '2023-06-20 11:40:29', 1, 1, 1, 1, 1, 1, 2, 1);

--
-- 转储表的索引
--

--
-- 表的索引 `Challenge`
--
ALTER TABLE `Challenge`
  ADD PRIMARY KEY (`CID`);

--
-- 表的索引 `member`
--
ALTER TABLE `member`
  ADD PRIMARY KEY (`MEID`);

--
-- 表的索引 `Membership`
--
ALTER TABLE `Membership`
  ADD PRIMARY KEY (`MSID`);

--
-- 表的索引 `TMatch`
--
ALTER TABLE `TMatch`
  ADD PRIMARY KEY (`MAID`);

--
-- 在导出的表使用AUTO_INCREMENT
--

--
-- 使用表AUTO_INCREMENT `Challenge`
--
ALTER TABLE `Challenge`
  MODIFY `CID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=9;

--
-- 使用表AUTO_INCREMENT `member`
--
ALTER TABLE `member`
  MODIFY `MEID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=22;

--
-- 使用表AUTO_INCREMENT `Membership`
--
ALTER TABLE `Membership`
  MODIFY `MSID` int(11) NOT NULL AUTO_INCREMENT;

--
-- 使用表AUTO_INCREMENT `TMatch`
--
ALTER TABLE `TMatch`
  MODIFY `MAID` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
