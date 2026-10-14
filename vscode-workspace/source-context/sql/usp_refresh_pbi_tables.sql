-- Synthetic example of the stored procedure that materializes the pbi.* tables nightly.
CREATE OR ALTER PROCEDURE pbi.usp_refresh_pbi_tables AS
BEGIN
    SET NOCOUNT ON;
    TRUNCATE TABLE pbi.customer360;         INSERT INTO pbi.customer360         SELECT * FROM pbi.vw_customer360;
    TRUNCATE TABLE pbi.web_activity;        INSERT INTO pbi.web_activity        SELECT * FROM pbi.vw_web_activity;
    TRUNCATE TABLE pbi.subscriptions;       INSERT INTO pbi.subscriptions       SELECT * FROM pbi.vw_subscriptions;
    TRUNCATE TABLE pbi.newsletter_signups;  INSERT INTO pbi.newsletter_signups  SELECT * FROM pbi.vw_newsletter_signups;
    TRUNCATE TABLE pbi.event_registrations; INSERT INTO pbi.event_registrations SELECT * FROM pbi.vw_event_registrations;
    TRUNCATE TABLE pbi.ad_orders;           INSERT INTO pbi.ad_orders           SELECT * FROM pbi.vw_ad_orders;
END;
