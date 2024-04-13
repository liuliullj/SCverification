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

 Date: 13/04/2024 15:12:03
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for test3Design
-- ----------------------------
DROP TABLE IF EXISTS `test3Design`;
CREATE TABLE `test3Design` (
  `id` int NOT NULL AUTO_INCREMENT,
  `pathname` varchar(255) DEFAULT NULL,
  `expression` varchar(255) DEFAULT NULL,
  `creattime` datetime DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- ----------------------------
-- Records of test3Design
-- ----------------------------
BEGIN;
INSERT INTO `test3Design` (`id`, `pathname`, `expression`, `creattime`) VALUES (1, 'trans', 'Workflow1.function1,workflow2.function2', '2024-04-11 19:42:11');
INSERT INTO `test3Design` (`id`, `pathname`, `expression`, `creattime`) VALUES (2, 'sfhdgs', 'asdasd', '2024-04-12 11:08:13');
INSERT INTO `test3Design` (`id`, `pathname`, `expression`, `creattime`) VALUES (3, 'jshdgfj', 'dsfjlsdf', '2024-04-12 11:09:09');
INSERT INTO `test3Design` (`id`, `pathname`, `expression`, `creattime`) VALUES (4, 'new', 'askdhijkas', '2024-04-12 11:21:09');
INSERT INTO `test3Design` (`id`, `pathname`, `expression`, `creattime`) VALUES (5, 'test2', 'dsjklsa', '2024-04-12 11:39:30');
INSERT INTO `test3Design` (`id`, `pathname`, `expression`, `creattime`) VALUES (6, 'test3', 'dkfjhkdsaf', '2024-04-12 11:39:42');
INSERT INTO `test3Design` (`id`, `pathname`, `expression`, `creattime`) VALUES (7, 'test4', 'sdjlfl', '2024-04-12 11:39:52');
INSERT INTO `test3Design` (`id`, `pathname`, `expression`, `creattime`) VALUES (8, 'test5new', 'sdkjfkds', '2024-04-12 11:40:00');
INSERT INTO `test3Design` (`id`, `pathname`, `expression`, `creattime`) VALUES (9, 'test6', 'sdfjsd', '2024-04-12 11:40:14');
INSERT INTO `test3Design` (`id`, `pathname`, `expression`, `creattime`) VALUES (10, 'test7', 'sdfjs', '2024-04-12 11:40:24');
INSERT INTO `test3Design` (`id`, `pathname`, `expression`, `creattime`) VALUES (11, 'test8', 'kdfef', '2024-04-12 11:40:33');
COMMIT;

SET FOREIGN_KEY_CHECKS = 1;
