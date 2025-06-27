/*
 Navicat Premium Dump SQL

 Source Server         : 192.168.124.23
 Source Server Type    : MySQL
 Source Server Version : 80405 (8.4.5)
 Source Host           : 192.168.124.23:3306
 Source Schema         : drawingInit

 Target Server Type    : MySQL
 Target Server Version : 80405 (8.4.5)
 File Encoding         : 65001

 Date: 27/06/2025 21:06:35
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for drawing_image_text
-- ----------------------------
DROP TABLE IF EXISTS `drawing_image_text`;
CREATE TABLE `drawing_image_text`  (
  `id` int NOT NULL AUTO_INCREMENT COMMENT '主键ID',
  `image_id` char(36) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '关联图片ID',
  `extracted_text` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '提取的文本',
  `text_region` json NOT NULL COMMENT '文本区域坐标（JSON格式）',
  `ocr_engine` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT 'OCR引擎',
  `recognition_confidence` float NOT NULL COMMENT '识别置信度（0-1）',
  `create_user_id` int NOT NULL COMMENT '创建用户ID',
  `create_datetime` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_datetime` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '更新时间',
  `delete_datetime` datetime NULL DEFAULT NULL COMMENT '删除时间',
  `is_delete` tinyint(1) NOT NULL COMMENT '是否软删除',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci COMMENT = '图片文本提取' ROW_FORMAT = DYNAMIC;

SET FOREIGN_KEY_CHECKS = 1;
