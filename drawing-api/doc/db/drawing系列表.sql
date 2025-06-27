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

 Date: 27/06/2025 20:44:15
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for drawing_resource_images
-- ----------------------------
DROP TABLE IF EXISTS `drawing_resource_images`;
CREATE TABLE `drawing_resource_images`  (
  `id` int NOT NULL AUTO_INCREMENT COMMENT '主键ID',
  `filename` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '文件名',
  `image_url` varchar(1024) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NOT NULL COMMENT '图片URL',
  `file_size` bigint NULL DEFAULT NULL COMMENT '文件大小（字节）',
  `image_type` varchar(50) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '图片类型（如jpg、png）',
  `width` int NULL DEFAULT NULL COMMENT '图片宽度',
  `height` int NULL DEFAULT NULL COMMENT '图片高度',
  `is_public` tinyint(1) NULL DEFAULT 0 COMMENT '是否公开（0-否，1-是）',
  `description` text CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL COMMENT '图片描述',
  `tags` varchar(512) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci NULL DEFAULT NULL COMMENT '标签（以逗号分隔的关键词）',
  `create_user_id` int NOT NULL COMMENT '创建用户ID',
  `create_datetime` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_datetime` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '更新时间',
  `delete_datetime` datetime NULL DEFAULT NULL COMMENT '删除时间',
  `is_delete` tinyint(1) NOT NULL COMMENT '是否软删除',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 12 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci COMMENT = '绘图资源图片表' ROW_FORMAT = Dynamic;

SET FOREIGN_KEY_CHECKS = 1;



CREATE TABLE `drawing_image_text`  (
  `id` int NOT NULL AUTO_INCREMENT COMMENT '主键ID',
  image_id CHAR(36) NOT NULL COMMENT '关联图片ID',
  extracted_text TEXT NOT NULL COMMENT '提取的文本',
  text_region JSON NOT NULL COMMENT '文本区域坐标（JSON格式）',
  ocr_engine VARCHAR(100) NOT NULL COMMENT 'OCR引擎',
  recognition_confidence FLOAT NOT NULL COMMENT '识别置信度（0-1）',
  `create_user_id` int NOT NULL COMMENT '创建用户ID',
  `create_datetime` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_datetime` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '更新时间',
  `delete_datetime` datetime NULL DEFAULT NULL COMMENT '删除时间',
  `is_delete` tinyint(1) NOT NULL COMMENT '是否软删除',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB COMMENT = '图片标签' ROW_FORMAT = Dynamic;


CREATE TABLE `drawing_image_embeddings`  (
  `id` int NOT NULL AUTO_INCREMENT COMMENT '主键ID',
  image_id CHAR(36) NOT NULL COMMENT '关联图片ID',
  embedding_model VARCHAR(100) NOT NULL COMMENT '特征提取模型',
  embedding_dim INT NOT NULL COMMENT '向量维度',
  embedding BLOB NOT NULL COMMENT '特征向量（二进制存储）',
  `create_user_id` int NOT NULL COMMENT '创建用户ID',
  `create_datetime` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
  `update_datetime` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '更新时间',
  `delete_datetime` datetime NULL DEFAULT NULL COMMENT '删除时间',
  `is_delete` tinyint(1) NOT NULL COMMENT '是否软删除',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='图像特征向量';