-- Synthetic example. Shows how a "first version" Customer 360 table is typically built.
-- The Power BI model imports this view into table pbi_customer360.
CREATE OR ALTER VIEW pbi.vw_customer360 AS
SELECT
    u.email                                   AS Email,          -- long text; used as the join key everywhere
    u.first_name                              AS FirstName,
    u.last_name                               AS LastName,
    u.first_name + ' ' + u.last_name          AS FullName,
    c.company_name                            AS Company,
    u.job_title                               AS JobTitle,
    u.market_name                             AS MarketName,     -- raw CRM value, not the standard Market list
    u.city, u.state,
    CAST(u.postal_code AS INT)                AS PostalCode,     -- leading zeros are lost here
    u.signup_ts                               AS SignupDateTime, -- full date-time; only the date is ever used
    w.last_seen_ts                            AS LastSeenDateTime,
    s.status_code                             AS sub_sts,
    s.plan_name                               AS CurrentPlan,
    CAST(s.monthly_price AS FLOAT)            AS plan_prc,       -- float currency
    DATEADD(DAY, 365, s.start_date)           AS RenewalDate,
    CASE WHEN c.is_enterprise = 1 THEN 'TRUE' ELSE 'FALSE' END AS IsEnterprise,  -- boolean as text
    c.company_name                            AS EnterpriseAccountName,
    snap.newsletter_count                     AS NewsletterCount,   -- values frozen by a nightly snapshot job
    snap.event_count                          AS EventCount,
    snap.lifetime_page_views                  AS LifetimePageViews, -- snapshot as of last quarter end, not live
    w.last_article_title                      AS LastArticleTitle,
    CASE WHEN c.is_enterprise = 1 THEN 'Enterprise'
         WHEN s.status_code = 'A' THEN 'Subscriber'
         WHEN s.status_code IN ('C','E') THEN 'Lapsed' ELSE 'Prospect' END AS CustomerSegment,
    SYSUTCDATETIME()                          AS _etl_load_ts,
    HASHBYTES('SHA2_256', u.email)            AS row_hash        -- unique per row; no analytical use
FROM stage.crm_users u
LEFT JOIN stage.crm_companies c       ON c.company_id = u.company_id
LEFT JOIN pbi.latest_subscription s   ON s.email = u.email
LEFT JOIN pbi.web_last_seen w         ON w.email = u.email
LEFT JOIN pbi.quarterly_snapshot snap ON snap.email = u.email;   -- joined on e-mail text