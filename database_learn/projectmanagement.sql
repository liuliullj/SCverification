/*
 Navicat Premium Data Transfer

 Source Server         : try
 Source Server Type    : MySQL
 Source Server Version : 80035
 Source Host           : localhost:3306
 Source Schema         : database_learn

 Target Server Type    : MySQL
 Target Server Version : 80035
 File Encoding         : 65001

 Date: 13/04/2024 15:11:21
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for projectmanagement
-- ----------------------------
DROP TABLE IF EXISTS `projectmanagement`;
CREATE TABLE `projectmanagement` (
  `Id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) DEFAULT NULL,
  `description` varchar(255) DEFAULT NULL,
  `creatTime` datetime DEFAULT NULL,
  PRIMARY KEY (`Id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- ----------------------------
-- Records of projectmanagement
-- ----------------------------
BEGIN;
INSERT INTO `projectmanagement` (`Id`, `name`, `description`, `creatTime`) VALUES (1, 'for test 1', 'asdsdf', '2024-04-08 20:42:28');
INSERT INTO `projectmanagement` (`Id`, `name`, `description`, `creatTime`) VALUES (2, 'test2change', 'sfsdfsdf', '2024-04-08 20:42:52');
INSERT INTO `projectmanagement` (`Id`, `name`, `description`, `creatTime`) VALUES (3, 'test3', 'asfliasjdoiasd', '2024-04-08 20:46:33');
INSERT INTO `projectmanagement` (`Id`, `name`, `description`, `creatTime`) VALUES (4, 'test4', 'dfhkf', '2024-04-10 20:32:53');
INSERT INTO `projectmanagement` (`Id`, `name`, `description`, `creatTime`) VALUES (5, 'test5new', 'sadhasd', '2024-04-11 17:12:47');
COMMIT;

SET FOREIGN_KEY_CHECKS = 1;
