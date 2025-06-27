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

 Date: 27/06/2025 21:06:45
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for drawing_multimodal_analysis
-- ----------------------------
DROP TABLE IF EXISTS `drawing_multimodal_analysis`;
CREATE TABLE `drawing_multimodal_analysis`  (
  `id` int NOT NULL AUTO_INCREMENT COMMENT '主键ID',
  `image_id` char(36) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '关联图片ID',
  `analysis_type` enum('caption','qa','classification','scene','object_detection') CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '分析类型',
  `analysis_result` json NOT NULL COMMENT '分析结果（JSON格式）',
  `llm_model` varchar(100) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '使用的LLM模型',
  `confidence` float NOT NULL COMMENT '分析置信度（0-1）',
  `analysis_time` datetime(3) NOT NULL DEFAULT CURRENT_TIMESTAMP(3) COMMENT '分析时间',
  `create_user_id` int NOT NULL COMMENT '创建用户ID',
  `create_datetime` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_datetime` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '更新时间',
  `delete_datetime` datetime NULL DEFAULT NULL COMMENT '删除时间',
  `is_delete` tinyint(1) NOT NULL COMMENT '是否软删除',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci COMMENT = '多模态分析结果表' ROW_FORMAT = DYNAMIC;

SET FOREIGN_KEY_CHECKS = 1;
