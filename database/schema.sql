-- Database schema for AI-Powered Intelligent Code Review and Software Defect Prediction System
-- Primary target: MySQL 8.0+

CREATE DATABASE IF NOT EXISTS `code_review_db` CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
USE `code_review_db`;

-- 1. Users table
CREATE TABLE IF NOT EXISTS `users` (
    `id` VARCHAR(36) PRIMARY KEY,
    `username` VARCHAR(100) NOT NULL UNIQUE,
    `email` VARCHAR(255) NOT NULL UNIQUE,
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    `updated_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 2. Projects table
CREATE TABLE IF NOT EXISTS `projects` (
    `id` VARCHAR(36) PRIMARY KEY,
    `user_id` VARCHAR(36) NULL,
    `name` VARCHAR(150) NOT NULL,
    `description` TEXT NULL,
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    `updated_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (`user_id`) REFERENCES `users`(`id`) ON DELETE SET NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 3. Files table
CREATE TABLE IF NOT EXISTS `files` (
    `id` VARCHAR(36) PRIMARY KEY,
    `project_id` VARCHAR(36) NULL,
    `filename` VARCHAR(255) NOT NULL,
    `language` VARCHAR(50) NOT NULL,
    `file_size_bytes` INT DEFAULT 0,
    `lines_of_code` INT DEFAULT 0,
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (`project_id`) REFERENCES `projects`(`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 4. Code Reviews table
CREATE TABLE IF NOT EXISTS `code_reviews` (
    `id` VARCHAR(36) PRIMARY KEY,
    `file_id` VARCHAR(36) NULL,
    `filename` VARCHAR(255) NOT NULL,
    `language` VARCHAR(50) NOT NULL,
    `source_code` MEDIUMTEXT NOT NULL,
    `quality_score` FLOAT NOT NULL DEFAULT 100.0,
    `risk_level` VARCHAR(20) NOT NULL DEFAULT 'Low', -- 'Low', 'Medium', 'High'
    `defect_probability` FLOAT NOT NULL DEFAULT 0.0,
    `total_issues` INT DEFAULT 0,
    `critical_issues` INT DEFAULT 0,
    `high_issues` INT DEFAULT 0,
    `medium_issues` INT DEFAULT 0,
    `low_issues` INT DEFAULT 0,
    `review_summary` TEXT NULL,
    `suggested_code` MEDIUMTEXT NULL,
    `ai_model_used` VARCHAR(100) DEFAULT 'Rule-Based Engine',
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (`file_id`) REFERENCES `files`(`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 5. Issues table
CREATE TABLE IF NOT EXISTS `issues` (
    `id` VARCHAR(36) PRIMARY KEY,
    `review_id` VARCHAR(36) NOT NULL,
    `issue_type` VARCHAR(50) NOT NULL, -- 'Security', 'Bug', 'Code Smell', 'Maintainability'
    `severity` VARCHAR(20) NOT NULL,   -- 'Critical', 'High', 'Medium', 'Low'
    `line_number` INT NULL,
    `title` VARCHAR(255) NOT NULL,
    `description` TEXT NOT NULL,
    `why_it_matters` TEXT NULL,
    `recommendation` TEXT NULL,
    `suggested_fix` TEXT NULL,
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (`review_id`) REFERENCES `code_reviews`(`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 6. Defect Predictions table
CREATE TABLE IF NOT EXISTS `defect_predictions` (
    `id` VARCHAR(36) PRIMARY KEY,
    `review_id` VARCHAR(36) NOT NULL,
    `defect_probability` FLOAT NOT NULL,
    `risk_level` VARCHAR(20) NOT NULL,
    `is_defect_prone` BOOLEAN NOT NULL DEFAULT FALSE,
    `model_name` VARCHAR(100) NOT NULL DEFAULT 'Random Forest Classifier',
    `cyclomatic_complexity` FLOAT DEFAULT 0.0,
    `loc` INT DEFAULT 0,
    `nesting_depth` INT DEFAULT 0,
    `function_count` INT DEFAULT 0,
    `class_count` INT DEFAULT 0,
    `smell_count` INT DEFAULT 0,
    `feature_vector_json` JSON NULL,
    `top_risk_factors_json` JSON NULL,
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (`review_id`) REFERENCES `code_reviews`(`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 7. Recommendations table
CREATE TABLE IF NOT EXISTS `recommendations` (
    `id` VARCHAR(36) PRIMARY KEY,
    `review_id` VARCHAR(36) NOT NULL,
    `category` VARCHAR(50) NOT NULL,
    `priority` VARCHAR(20) NOT NULL,
    `title` VARCHAR(255) NOT NULL,
    `action_plan` TEXT NOT NULL,
    `created_at` TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (`review_id`) REFERENCES `code_reviews`(`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Indexing for performance
CREATE INDEX `idx_reviews_created_at` ON `code_reviews` (`created_at` DESC);
CREATE INDEX `idx_reviews_risk_level` ON `code_reviews` (`risk_level`);
CREATE INDEX `idx_issues_severity` ON `issues` (`severity`);
CREATE INDEX `idx_issues_type` ON `issues` (`issue_type`);
