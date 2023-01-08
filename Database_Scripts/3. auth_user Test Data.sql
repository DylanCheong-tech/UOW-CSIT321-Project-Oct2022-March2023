-- 3. auth_user Test Data.sql

-- Test Data for django.contrib.auth as corresponsind to UserAccount

ALTER TABLE `auth_user`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=1;
COMMIT;

INSERT INTO `auth_user` (`id`, `password`, `last_login`, `is_superuser`, `username`, `first_name`, `last_name`, `email`, `is_staff`, `is_active`, `date_joined`) VALUES
(1, 'pbkdf2_sha256$390000$av7NEmZkkcONYPWnRZq42F$8ENkVRVAMMNjm8EHGqMXi8wezsYZrrO3zYRFRoILl/o=', NULL, 0, 'jamessmith@mail.com', '', '', '', 0, 1, '2023-01-08 04:15:28.751365'),
(2, 'pbkdf2_sha256$390000$7RV0Je9dOBwzYTg3KGDPWU$Rg3e5QKMYCkq+9HA2v4lD1CZxDOh0cLGaE+noVuaFwo=', NULL, 0, 'michaelgarcia@mail.com', '', '', '', 0, 1, '2023-01-08 04:15:38.252314'),
(3, 'pbkdf2_sha256$390000$djdMf9IQCbjWcz1okZZNnC$/tGy0sA4wGyRV9X41T2jTU5OR4+8+eRcwFiJ644uTz0=', NULL, 0, 'robertjohnson@mail.com', '', '', '', 0, 1, '2023-01-08 04:15:44.866353'),
(4, 'pbkdf2_sha256$390000$I9Uad3HN8eh3Ygt7FWk4ga$BMdgQ6uAxrJC4qNk/u6y5bEYwU14ML9s3CP48CTE8hw=', NULL, 0, 'mariarodriguez@mail.com', '', '', '', 0, 1, '2023-01-08 04:15:50.964782'),
(5, 'pbkdf2_sha256$390000$MCHXiv4DP0Z6gY2730UrhP$UD8O5YCoQgxApDqI7T5SwM35ed2CXgCuD2+LBdyqCjU=', NULL, 0, 'davidlim@mail.com', '', '', '', 0, 1, '2023-01-08 04:15:57.041957'),
(6, 'pbkdf2_sha256$390000$8SGaHGlVfhHAqGtf1Hpjss$UCqyLrmMt34XJtgfWAYuZ4uOQn9sFWV+S2+JwvaLcDs=', NULL, 0, 'maryleong@mail.com', '', '', '', 0, 1, '2023-01-08 04:16:04.169576'),
(7, 'pbkdf2_sha256$390000$EFIVHirne8VwM5uoVENSAm$HCZ2VbUaYuG3QH9IKMuGAzbzVwOZHvO24u4++ds7QWs=', NULL, 0, 'susanmiller@mail.com', '', '', '', 0, 1, '2023-01-08 04:16:10.245848'),
(8, 'pbkdf2_sha256$390000$Xe9TXoLDAlRSAJwNzGIykG$yLBE2NLGxlKmoeUVep7ty05e3jVPDB1w3KyiatsmqNo=', NULL, 0, 'goergelim@mail.com', '', '', '', 0, 1, '2023-01-08 04:16:16.869361'),
(9, 'pbkdf2_sha256$390000$bbceRChnKL90PZLjXCdBSp$f3x+9Xo2UKn4ntV1sWBvGxZBaTUFu+0/H2Tw69XwLCc=', NULL, 0, 'elizataylor@mail.com', '', '', '', 0, 1, '2023-01-08 04:16:22.400841'),
(10, 'pbkdf2_sha256$390000$uzj15Qe1qiYoTodJWIqgcM$TBmPdm873XYL0z2msHk2sggLdTjWE8ePIigj5MztWr0=', NULL, 0, 'henryroderick@mail.com', '', '', '', 0, 1, '2023-01-08 04:16:28.981743');

