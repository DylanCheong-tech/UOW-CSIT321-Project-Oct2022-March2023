-- 2. UserAccount Test Data.sql

-- Test Data for UserAccount Model

ALTER TABLE `evoting_useraccount`
  MODIFY `accountID` bigint(20) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=1;
COMMIT;

INSERT INTO `evoting_useraccount` (`accountID`, `email`, `password`, `firstName`, `lastName`, `gender`, `createdAt`) VALUES
(1, 'jamessmith@mail.com', 'a66c547ccb141e2b74bdcf579fa7f3a8', 'James', 'Smith', 'M', '2023-01-08 04:15:28.750572'),
(2, 'michaelgarcia@mail.com', 'c5bb53b95610ee080d178f8eb108b566', 'Michael', 'Garcia', 'F', '2023-01-08 04:15:38.251049'),
(3, 'robertjohnson@mail.com', 'b95c4b60fa109b37ff292c25f99b0528', 'Robert', 'Johnson', 'M', '2023-01-08 04:15:44.865229'),
(4, 'mariarodriguez@mail.com', 'fbd94b40ba25d3e73e834c52fbe339f8', 'Maria', 'Rodriguez', 'F', '2023-01-08 04:15:50.963511'),
(5, 'davidlim@mail.com', '1f458b54916badc00bba6d969ff299da', 'David', 'Lim', 'M', '2023-01-08 04:15:57.040884'),
(6, 'maryleong@mail.com', '660bc3a19176544cccfdd087d6182d36', 'Mary', 'Leong', 'F', '2023-01-08 04:16:04.168665'),
(7, 'susanmiller@mail.com', '25cf3304ee83aecbcb7cc51eac70e783', 'Susan', 'Miller', 'F', '2023-01-08 04:16:10.243703'),
(8, 'goergelim@mail.com', '20eed1a191172863db02d45e6f2e4258', 'George', 'Lim', 'M', '2023-01-08 04:16:16.867956'),
(9, 'elizataylor@mail.com', 'a08e1bafc5ccda8d88dfff579b8b2e6d', 'Eliza', 'Taylor', 'F', '2023-01-08 04:16:22.399989'),
(10, 'henryroderick@mail.com', 'e078514091f1490e3945d9ba4f3c3fe6', 'Henry', 'Roderick', 'M', '2023-01-08 04:16:28.980390');
