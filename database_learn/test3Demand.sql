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

 Date: 13/04/2024 15:11:51
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for test3Demand
-- ----------------------------
DROP TABLE IF EXISTS `test3Demand`;
CREATE TABLE `test3Demand` (
  `id` int NOT NULL AUTO_INCREMENT,
  `demandname` varchar(255) NOT NULL,
  `category` varchar(255) NOT NULL,
  `demanddescription` varchar(255) DEFAULT NULL,
  `parentD` int DEFAULT NULL,
  `creattime` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `parentD` (`parentD`),
  CONSTRAINT `test3demand_ibfk_1` FOREIGN KEY (`parentD`) REFERENCES `test3Demand` (`id`) ON DELETE SET NULL
) ENGINE=InnoDB AUTO_INCREMENT=14 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- ----------------------------
-- Records of test3Demand
-- ----------------------------
BEGIN;
INSERT INTO `test3Demand` (`id`, `demandname`, `category`, `demanddescription`, `parentD`, `creattime`) VALUES (1, 'user', '条件语句', '用户描述', 1, '2024-04-08 20:49:51');
INSERT INTO `test3Demand` (`id`, `demandname`, `category`, `demanddescription`, `parentD`, `creattime`) VALUES (2, 'asdasd', '附加信息', 'gdfg', 1, '2024-04-10 16:17:47');
INSERT INTO `test3Demand` (`id`, `demandname`, `category`, `demanddescription`, `parentD`, `creattime`) VALUES (3, 'workflow1', '执行流程', 'sdhaksd', 1, '2024-04-11 15:59:25');
INSERT INTO `test3Demand` (`id`, `demandname`, `category`, `demanddescription`, `parentD`, `creattime`) VALUES (4, 'workflow2', '执行流程', 'dhfdsk', 1, '2024-04-11 15:59:45');
INSERT INTO `test3Demand` (`id`, `demandname`, `category`, `demanddescription`, `parentD`, `creattime`) VALUES (5, 'workflow3', '执行流程', 'dasd', 1, '2024-04-11 16:00:04');
INSERT INTO `test3Demand` (`id`, `demandname`, `category`, `demanddescription`, `parentD`, `creattime`) VALUES (6, 'function1', '方法', 'sdfdsf', 3, '2024-04-11 16:00:53');
INSERT INTO `test3Demand` (`id`, `demandname`, `category`, `demanddescription`, `parentD`, `creattime`) VALUES (7, 'function2', '方法', 'asdjsd', 4, '2024-04-11 16:01:16');
INSERT INTO `test3Demand` (`id`, `demandname`, `category`, `demanddescription`, `parentD`, `creattime`) VALUES (8, 'function3', '方法', 'sdkfhjds', 5, '2024-04-11 16:01:43');
INSERT INTO `test3Demand` (`id`, `demandname`, `category`, `demanddescription`, `parentD`, `creattime`) VALUES (9, 'workflow5', '执行流程', 'fsef', 1, '2024-04-11 17:45:19');
INSERT INTO `test3Demand` (`id`, `demandname`, `category`, `demanddescription`, `parentD`, `creattime`) VALUES (10, 'workflow6', '执行流程', 'dgdfg', 1, '2024-04-11 17:45:34');
INSERT INTO `test3Demand` (`id`, `demandname`, `category`, `demanddescription`, `parentD`, `creattime`) VALUES (11, 'function4', '方法', 'sfsdgf', 9, '2024-04-11 17:46:04');
INSERT INTO `test3Demand` (`id`, `demandname`, `category`, `demanddescription`, `parentD`, `creattime`) VALUES (12, 'function5', '方法', 'sdfkjdsf', 10, '2024-04-11 17:46:36');
INSERT INTO `test3Demand` (`id`, `demandname`, `category`, `demanddescription`, `parentD`, `creattime`) VALUES (13, 'function6', '方法', 'sdfhjsd', 9, '2024-04-11 17:47:31');
COMMIT;

SET FOREIGN_KEY_CHECKS = 1;
