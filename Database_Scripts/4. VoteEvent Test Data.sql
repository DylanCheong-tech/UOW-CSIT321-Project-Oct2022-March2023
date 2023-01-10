-- 4. VoteEvent Test Data.sql

-- Test Data for VoteEvent Model

ALTER TABLE `evoting_voteevent`
  MODIFY `seqNo` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=1;

INSERT INTO `evoting_voteevent` (`seqNo`, `eventTitle`, `startDate`, `startTime`, `endDate`, `endTime`, `eventQuestion`, `status`, `createdBy_id`) VALUES
(1, 'Vote Event Title 1', '2024-09-18', '08:00:00.000000', '2024-09-22', '11:00:00.000000', 'Vote Event Question 1', 'PC', 1),
(2, 'Vote Event Title 2', '2024-04-26', '20:00:00.000000', '2024-05-10', '20:00:00.000000', 'Vote Event Question 2', 'PC', 1),
(3, 'Vote Event Title 3', '2024-06-13', '11:00:00.000000', '2024-07-06', '05:00:00.000000', 'Vote Event Question 3', 'PC', 1),
(4, 'Vote Event Title 4', '2024-02-29', '00:00:00.000000', '2024-03-16', '00:00:00.000000', 'Vote Event Question 4', 'PB', 1),
(5, 'Vote Event Title 5', '2024-11-06', '02:00:00.000000', '2024-11-17', '02:00:00.000000', 'Vote Event Question 5', 'PB', 1),
(6, 'Vote Event Title 6', '2024-10-17', '09:00:00.000000', '2024-11-08', '23:00:00.000000', 'Vote Event Question 6', 'PB', 1),
(7, 'Vote Event Title 7', '2024-03-16', '15:00:00.000000', '2024-04-06', '23:00:00.000000', 'Vote Event Question 7', 'VC', 1),
(8, 'Vote Event Title 8', '2024-05-19', '14:00:00.000000', '2024-06-06', '17:00:00.000000', 'Vote Event Question 8', 'FR', 1),
(9, 'Vote Event Title 9', '2024-07-23', '22:00:00.000000', '2024-08-14', '18:00:00.000000', 'Vote Event Question 9', 'RP', 1),
(10, 'Vote Event Title 10', '2024-07-25', '06:00:00.000000', '2024-08-20', '04:00:00.000000', 'Vote Event Question 10', 'RP', 1),
(11, 'Vote Event Title 11', '2024-02-25', '16:00:00.000000', '2024-03-22', '12:00:00.000000', 'Vote Event Question 11', 'PC', 2),
(12, 'Vote Event Title 12', '2024-02-05', '18:00:00.000000', '2024-02-16', '17:00:00.000000', 'Vote Event Question 12', 'PC', 2),
(13, 'Vote Event Title 13', '2024-04-14', '05:00:00.000000', '2024-05-12', '10:00:00.000000', 'Vote Event Question 13', 'PC', 2),
(14, 'Vote Event Title 14', '2024-10-09', '20:00:00.000000', '2024-10-27', '13:00:00.000000', 'Vote Event Question 14', 'PB', 2),
(15, 'Vote Event Title 15', '2024-09-10', '22:00:00.000000', '2024-10-09', '04:00:00.000000', 'Vote Event Question 15', 'PB', 2),
(16, 'Vote Event Title 16', '2024-05-27', '02:00:00.000000', '2024-05-31', '00:00:00.000000', 'Vote Event Question 16', 'PB', 2),
(17, 'Vote Event Title 17', '2024-02-24', '23:00:00.000000', '2024-03-07', '03:00:00.000000', 'Vote Event Question 17', 'VC', 2),
(18, 'Vote Event Title 18', '2024-01-26', '20:00:00.000000', '2024-02-02', '10:00:00.000000', 'Vote Event Question 18', 'FR', 2),
(19, 'Vote Event Title 19', '2024-12-15', '18:00:00.000000', '2025-01-14', '15:00:00.000000', 'Vote Event Question 19', 'RP', 2),
(20, 'Vote Event Title 20', '2024-08-17', '00:00:00.000000', '2024-08-28', '10:00:00.000000', 'Vote Event Question 20', 'RP', 2),
(21, 'Vote Event Title 21', '2024-12-12', '12:00:00.000000', '2024-12-17', '18:00:00.000000', 'Vote Event Question 21', 'PC', 3),
(22, 'Vote Event Title 22', '2024-05-29', '14:00:00.000000', '2024-06-12', '09:00:00.000000', 'Vote Event Question 22', 'PC', 3),
(23, 'Vote Event Title 23', '2024-01-01', '04:00:00.000000', '2024-01-11', '23:00:00.000000', 'Vote Event Question 23', 'PC', 3),
(24, 'Vote Event Title 24', '2024-10-29', '11:00:00.000000', '2024-11-07', '09:00:00.000000', 'Vote Event Question 24', 'PB', 3),
(25, 'Vote Event Title 25', '2024-11-30', '19:00:00.000000', '2024-12-24', '12:00:00.000000', 'Vote Event Question 25', 'PB', 3),
(26, 'Vote Event Title 26', '2024-06-25', '23:00:00.000000', '2024-07-15', '21:00:00.000000', 'Vote Event Question 26', 'PB', 3),
(27, 'Vote Event Title 27', '2024-06-18', '02:00:00.000000', '2024-06-25', '14:00:00.000000', 'Vote Event Question 27', 'VC', 3),
(28, 'Vote Event Title 28', '2024-02-18', '05:00:00.000000', '2024-02-19', '21:00:00.000000', 'Vote Event Question 28', 'FR', 3),
(29, 'Vote Event Title 29', '2024-04-17', '18:00:00.000000', '2024-05-09', '06:00:00.000000', 'Vote Event Question 29', 'RP', 3),
(30, 'Vote Event Title 30', '2024-01-27', '08:00:00.000000', '2024-02-03', '00:00:00.000000', 'Vote Event Question 30', 'RP', 3),
(31, 'Vote Event Title 31', '2024-12-19', '08:00:00.000000', '2025-01-03', '16:00:00.000000', 'Vote Event Question 31', 'PC', 4),
(32, 'Vote Event Title 32', '2024-08-11', '15:00:00.000000', '2024-09-09', '05:00:00.000000', 'Vote Event Question 32', 'PC', 4),
(33, 'Vote Event Title 33', '2024-01-12', '20:00:00.000000', '2024-01-16', '06:00:00.000000', 'Vote Event Question 33', 'PC', 4),
(34, 'Vote Event Title 34', '2024-01-14', '10:00:00.000000', '2024-01-16', '22:00:00.000000', 'Vote Event Question 34', 'PB', 4),
(35, 'Vote Event Title 35', '2024-09-14', '05:00:00.000000', '2024-09-16', '17:00:00.000000', 'Vote Event Question 35', 'PB', 4),
(36, 'Vote Event Title 36', '2024-12-17', '12:00:00.000000', '2024-12-19', '14:00:00.000000', 'Vote Event Question 36', 'PB', 4),
(37, 'Vote Event Title 37', '2024-02-29', '04:00:00.000000', '2024-03-03', '00:00:00.000000', 'Vote Event Question 37', 'VC', 4),
(38, 'Vote Event Title 38', '2024-08-03', '11:00:00.000000', '2024-09-01', '04:00:00.000000', 'Vote Event Question 38', 'FR', 4),
(39, 'Vote Event Title 39', '2024-11-07', '17:00:00.000000', '2024-11-09', '15:00:00.000000', 'Vote Event Question 39', 'RP', 4),
(40, 'Vote Event Title 40', '2024-07-27', '18:00:00.000000', '2024-08-09', '07:00:00.000000', 'Vote Event Question 40', 'RP', 4),
(41, 'Vote Event Title 41', '2024-11-24', '08:00:00.000000', '2024-12-09', '13:00:00.000000', 'Vote Event Question 41', 'PC', 5),
(42, 'Vote Event Title 42', '2024-01-15', '19:00:00.000000', '2024-01-22', '01:00:00.000000', 'Vote Event Question 42', 'PC', 5),
(43, 'Vote Event Title 43', '2024-11-24', '04:00:00.000000', '2024-11-28', '17:00:00.000000', 'Vote Event Question 43', 'PC', 5),
(44, 'Vote Event Title 44', '2024-04-04', '15:00:00.000000', '2024-04-23', '20:00:00.000000', 'Vote Event Question 44', 'PB', 5),
(45, 'Vote Event Title 45', '2024-04-27', '18:00:00.000000', '2024-05-23', '18:00:00.000000', 'Vote Event Question 45', 'PB', 5),
(46, 'Vote Event Title 46', '2024-06-21', '11:00:00.000000', '2024-06-24', '14:00:00.000000', 'Vote Event Question 46', 'PB', 5),
(47, 'Vote Event Title 47', '2024-08-19', '22:00:00.000000', '2024-09-13', '22:00:00.000000', 'Vote Event Question 47', 'VC', 5),
(48, 'Vote Event Title 48', '2024-07-24', '02:00:00.000000', '2024-08-10', '22:00:00.000000', 'Vote Event Question 48', 'FR', 5),
(49, 'Vote Event Title 49', '2024-07-14', '14:00:00.000000', '2024-08-11', '01:00:00.000000', 'Vote Event Question 49', 'RP', 5),
(50, 'Vote Event Title 50', '2024-06-03', '04:00:00.000000', '2024-06-24', '01:00:00.000000', 'Vote Event Question 50', 'RP', 5),
(51, 'Vote Event Title 51', '2024-04-13', '16:00:00.000000', '2024-04-19', '05:00:00.000000', 'Vote Event Question 51', 'PC', 6),
(52, 'Vote Event Title 52', '2024-03-24', '11:00:00.000000', '2024-03-29', '13:00:00.000000', 'Vote Event Question 52', 'PC', 6),
(53, 'Vote Event Title 53', '2024-11-23', '02:00:00.000000', '2024-11-26', '04:00:00.000000', 'Vote Event Question 53', 'PC', 6),
(54, 'Vote Event Title 54', '2024-06-04', '05:00:00.000000', '2024-06-15', '17:00:00.000000', 'Vote Event Question 54', 'PB', 6),
(55, 'Vote Event Title 55', '2024-05-12', '08:00:00.000000', '2024-06-01', '18:00:00.000000', 'Vote Event Question 55', 'PB', 6),
(56, 'Vote Event Title 56', '2024-12-02', '23:00:00.000000', '2024-12-22', '15:00:00.000000', 'Vote Event Question 56', 'PB', 6),
(57, 'Vote Event Title 57', '2024-09-12', '11:00:00.000000', '2024-10-05', '17:00:00.000000', 'Vote Event Question 57', 'VC', 6),
(58, 'Vote Event Title 58', '2024-10-07', '07:00:00.000000', '2024-10-14', '11:00:00.000000', 'Vote Event Question 58', 'FR', 6),
(59, 'Vote Event Title 59', '2024-04-14', '19:00:00.000000', '2024-04-21', '00:00:00.000000', 'Vote Event Question 59', 'RP', 6),
(60, 'Vote Event Title 60', '2024-01-19', '20:00:00.000000', '2024-01-27', '03:00:00.000000', 'Vote Event Question 60', 'RP', 6),
(61, 'Vote Event Title 61', '2024-12-29', '06:00:00.000000', '2025-01-26', '00:00:00.000000', 'Vote Event Question 61', 'PC', 7),
(62, 'Vote Event Title 62', '2024-10-02', '07:00:00.000000', '2024-10-14', '23:00:00.000000', 'Vote Event Question 62', 'PC', 7),
(63, 'Vote Event Title 63', '2024-04-25', '18:00:00.000000', '2024-05-20', '06:00:00.000000', 'Vote Event Question 63', 'PC', 7),
(64, 'Vote Event Title 64', '2024-11-13', '22:00:00.000000', '2024-11-14', '03:00:00.000000', 'Vote Event Question 64', 'PB', 7),
(65, 'Vote Event Title 65', '2024-09-15', '15:00:00.000000', '2024-09-20', '00:00:00.000000', 'Vote Event Question 65', 'PB', 7),
(66, 'Vote Event Title 66', '2024-08-02', '09:00:00.000000', '2024-08-13', '19:00:00.000000', 'Vote Event Question 66', 'PB', 7),
(67, 'Vote Event Title 67', '2024-01-11', '01:00:00.000000', '2024-01-27', '21:00:00.000000', 'Vote Event Question 67', 'VC', 7),
(68, 'Vote Event Title 68', '2024-11-06', '02:00:00.000000', '2024-11-11', '14:00:00.000000', 'Vote Event Question 68', 'FR', 7),
(69, 'Vote Event Title 69', '2024-11-18', '12:00:00.000000', '2024-12-12', '19:00:00.000000', 'Vote Event Question 69', 'RP', 7),
(70, 'Vote Event Title 70', '2024-06-04', '17:00:00.000000', '2024-06-22', '00:00:00.000000', 'Vote Event Question 70', 'RP', 7),
(71, 'Vote Event Title 71', '2024-11-04', '20:00:00.000000', '2024-11-26', '02:00:00.000000', 'Vote Event Question 71', 'PC', 8),
(72, 'Vote Event Title 72', '2024-11-20', '16:00:00.000000', '2024-12-06', '00:00:00.000000', 'Vote Event Question 72', 'PC', 8),
(73, 'Vote Event Title 73', '2024-08-18', '14:00:00.000000', '2024-09-06', '15:00:00.000000', 'Vote Event Question 73', 'PC', 8),
(74, 'Vote Event Title 74', '2024-03-15', '23:00:00.000000', '2024-04-03', '21:00:00.000000', 'Vote Event Question 74', 'PB', 8),
(75, 'Vote Event Title 75', '2024-02-02', '06:00:00.000000', '2024-02-14', '10:00:00.000000', 'Vote Event Question 75', 'PB', 8),
(76, 'Vote Event Title 76', '2024-02-19', '15:00:00.000000', '2024-02-21', '13:00:00.000000', 'Vote Event Question 76', 'PB', 8),
(77, 'Vote Event Title 77', '2024-11-14', '21:00:00.000000', '2024-11-21', '18:00:00.000000', 'Vote Event Question 77', 'VC', 8),
(78, 'Vote Event Title 78', '2024-04-20', '22:00:00.000000', '2024-05-07', '23:00:00.000000', 'Vote Event Question 78', 'FR', 8),
(79, 'Vote Event Title 79', '2024-06-20', '11:00:00.000000', '2024-06-26', '12:00:00.000000', 'Vote Event Question 79', 'RP', 8),
(80, 'Vote Event Title 80', '2024-04-06', '19:00:00.000000', '2024-04-24', '19:00:00.000000', 'Vote Event Question 80', 'RP', 8),
(81, 'Vote Event Title 81', '2024-11-23', '06:00:00.000000', '2024-12-19', '03:00:00.000000', 'Vote Event Question 81', 'PC', 9),
(82, 'Vote Event Title 82', '2024-05-20', '09:00:00.000000', '2024-06-18', '16:00:00.000000', 'Vote Event Question 82', 'PC', 9),
(83, 'Vote Event Title 83', '2024-12-27', '08:00:00.000000', '2025-01-23', '11:00:00.000000', 'Vote Event Question 83', 'PC', 9),
(84, 'Vote Event Title 84', '2024-09-28', '22:00:00.000000', '2024-10-20', '21:00:00.000000', 'Vote Event Question 84', 'PB', 9),
(85, 'Vote Event Title 85', '2024-05-21', '20:00:00.000000', '2024-05-31', '22:00:00.000000', 'Vote Event Question 85', 'PB', 9),
(86, 'Vote Event Title 86', '2024-02-28', '00:00:00.000000', '2024-03-13', '23:00:00.000000', 'Vote Event Question 86', 'PB', 9),
(87, 'Vote Event Title 87', '2024-01-10', '22:00:00.000000', '2024-01-11', '20:00:00.000000', 'Vote Event Question 87', 'VC', 9),
(88, 'Vote Event Title 88', '2024-12-12', '02:00:00.000000', '2024-12-23', '19:00:00.000000', 'Vote Event Question 88', 'FR', 9),
(89, 'Vote Event Title 89', '2024-05-02', '02:00:00.000000', '2024-05-19', '17:00:00.000000', 'Vote Event Question 89', 'RP', 9),
(90, 'Vote Event Title 90', '2024-03-17', '00:00:00.000000', '2024-04-09', '18:00:00.000000', 'Vote Event Question 90', 'RP', 9),
(91, 'Vote Event Title 91', '2024-09-05', '05:00:00.000000', '2024-09-14', '18:00:00.000000', 'Vote Event Question 91', 'PC', 10),
(92, 'Vote Event Title 92', '2024-08-07', '11:00:00.000000', '2024-08-18', '07:00:00.000000', 'Vote Event Question 92', 'PC', 10),
(93, 'Vote Event Title 93', '2024-02-17', '16:00:00.000000', '2024-02-27', '22:00:00.000000', 'Vote Event Question 93', 'PC', 10),
(94, 'Vote Event Title 94', '2024-10-10', '12:00:00.000000', '2024-10-22', '14:00:00.000000', 'Vote Event Question 94', 'PB', 10),
(95, 'Vote Event Title 95', '2024-09-29', '22:00:00.000000', '2024-10-27', '23:00:00.000000', 'Vote Event Question 95', 'PB', 10),
(96, 'Vote Event Title 96', '2024-07-03', '01:00:00.000000', '2024-07-29', '05:00:00.000000', 'Vote Event Question 96', 'PB', 10),
(97, 'Vote Event Title 97', '2024-06-08', '20:00:00.000000', '2024-07-01', '12:00:00.000000', 'Vote Event Question 97', 'VC', 10),
(98, 'Vote Event Title 98', '2024-03-21', '05:00:00.000000', '2024-04-03', '05:00:00.000000', 'Vote Event Question 98', 'FR', 10),
(99, 'Vote Event Title 99', '2024-08-27', '06:00:00.000000', '2024-09-20', '14:00:00.000000', 'Vote Event Question 99', 'RP', 10),
(100, 'Vote Event Title 100', '2024-06-20', '02:00:00.000000', '2024-07-17', '16:00:00.000000', 'Vote Event Question 100', 'RP', 10);
