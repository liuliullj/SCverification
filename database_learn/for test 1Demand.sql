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

 Date: 13/04/2024 15:11:05
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for for test 1Demand
-- ----------------------------
DROP TABLE IF EXISTS `for test 1Demand`;
CREATE TABLE `for test 1Demand` (
  `id` int NOT NULL AUTO_INCREMENT,
  `demandname` varchar(255) NOT NULL,
  `category` varchar(255) NOT NULL,
  `demanddescription` varchar(255) DEFAULT NULL,
  `parentD` int DEFAULT NULL,
  `creattime` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `parentD` (`parentD`),
  CONSTRAINT `for test 1demand_ibfk_1` FOREIGN KEY (`parentD`) REFERENCES `for test 1Demand` (`id`) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- ----------------------------
-- Records of for test 1Demand
-- ----------------------------
BEGIN;
COMMIT;

SET FOREIGN_KEY_CHECKS = 1;
