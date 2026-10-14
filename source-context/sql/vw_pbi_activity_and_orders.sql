-- Synthetic example. Each source system keeps its own market naming; nobody maps them to one list.
CREATE OR ALTER VIEW pbi.vw_subscriptions AS
SELECT subscription_id AS SubscriptionID, email AS Email, plan_name AS PlanName,
       market_name AS MarketName,               -- billing system: mostly standard names ("Miami" about 15% of the time)
       start_ts AS StartDate, end_date AS EndDate,
       status_code AS sub_sts, CAST(monthly_price AS FLOAT) AS plan_prc, billing_cycle_code AS bill_cyc,
       sales_channel AS chnl, cancel_reason AS CancelReason,
       SYSUTCDATETIME() AS _etl_load_ts, 'billing_export.csv' AS _source_file
FROM stage.billing_subscriptions;
GO
CREATE OR ALTER VIEW pbi.vw_web_activity AS
SELECT email AS Email, activity_ts AS ActivityDateTime,   -- event-level time stamp: about 1M distinct values
       market_name AS MarketName,                         -- web analytics prefers nicknames ("DFW", "Twin Cities")
       sessions AS Sessions, page_views AS PageViews, articles_read AS ArticlesRead, device_type AS DeviceType,
       CHECKSUM(email, activity_ts) AS row_hash, SYSUTCDATETIME() AS _etl_load_ts
FROM stage.web_analytics_daily;                           -- includes readers who never registered (no customer row)
GO
CREATE OR ALTER VIEW pbi.vw_newsletter_signups AS
SELECT email AS Email, newsletter_name AS NewsletterName, market_name AS MarketName,
       signup_date AS SignupDate, status AS Status, CAST(open_rate AS FLOAT) AS OpenRate, SYSUTCDATETIME() AS _etl_load_ts
FROM stage.email_platform_signups;
GO
CREATE OR ALTER VIEW pbi.vw_event_registrations AS
SELECT email AS Email, event_name AS EventName, event_date AS EventDate, market_name AS MarketName,
       ticket_type AS TicketType,
       '$' + FORMAT(ticket_price, 'N2') AS TicketPrice,   -- money as text
       CASE WHEN attended = 1 THEN 'Y' ELSE 'N' END AS Attended,
       SYSUTCDATETIME() AS _etl_load_ts
FROM stage.ticketing_registrations;
GO
CREATE OR ALTER VIEW pbi.vw_ad_orders AS
SELECT order_id AS OrderID, advertiser_name AS AdvertiserName, contact_email AS ContactEmail,
       market_name AS MarketName, order_ts AS OrderDate, ad_product AS AdProduct, impressions AS Impressions,
       CAST(amount AS FLOAT) AS Amount, SYSUTCDATETIME() AS _etl_load_ts
FROM stage.ad_system_orders;                              -- contact_email is blank on some orders