-- ==========================================
-- TELECOM ANALYTICS
-- MYSQL VALIDATION QUERIES
-- ==========================================

USE TelecomAnalytics;


-- ==========================================
-- VERIFY ANALYTICAL TABLES
-- ==========================================

SELECT
    TABLE_SCHEMA,
    TABLE_NAME
FROM INFORMATION_SCHEMA.TABLES
WHERE TABLE_SCHEMA = 'TelecomAnalytics'
  AND TABLE_TYPE = 'BASE TABLE'
  AND TABLE_NAME IN ('Experience', 'Engagement', 'Satisfaction')
ORDER BY TABLE_NAME;


-- ==========================================
-- ROW COUNT VALIDATION
-- ==========================================

SELECT
    'Experience' AS Dataset_Name,
    COUNT(*) AS Total_Rows
FROM Experience

UNION ALL

SELECT
    'Engagement' AS Dataset_Name,
    COUNT(*) AS Total_Rows
FROM Engagement

UNION ALL

SELECT
    'Satisfaction' AS Dataset_Name,
    COUNT(*) AS Total_Rows
FROM Satisfaction;


-- ==========================================
-- SAMPLE DATA VALIDATION
-- Purpose:
-- Verify that the uploaded analytical tables
-- contain the expected customer-level data.
-- ==========================================


-- Verify Experience Dataset

SELECT
    MSISDN_Number,
    Average_TCP_Retransmission,
    Average_RTT,
    Handset_Type,
    Average_Throughput,
    Experience_Cluster
FROM Experience
LIMIT 10;


-- Verify Engagement Dataset

SELECT
    MSISDN_Number,
    xDR_Sessions,
    Total_Session_Duration_ms,
    Total_Traffic_Bytes,
    Engagement_Cluster
FROM Engagement
LIMIT 10;


-- Verify Satisfaction Dataset

SELECT
    MSISDN_Number,
    Engagement_Score,
    Experience_Score,
    Satisfaction_Score,
    Satisfaction_Cluster
FROM Satisfaction
LIMIT 10;


-- ==========================================
-- TOP 10 SATISFIED CUSTOMERS
-- Purpose:
-- Identify the top 10 customers based on
-- the calculated Satisfaction Score.
-- Higher score = higher distance from the
-- less-engaged and weaker-experience reference
-- clusters used in the project.
-- ==========================================

SELECT
    MSISDN_Number,
    Engagement_Score,
    Experience_Score,
    Satisfaction_Score,
    Satisfaction_Cluster
FROM Satisfaction
ORDER BY Satisfaction_Score DESC
LIMIT 10;

USE TelecomAnalytics;

SHOW TABLES;