---
description: Design (then, after approval, build) a Direct Lake semantic model from the gold tables
---
Goal: a Direct Lake semantic model named **Customer 360 Gold** in Fabric workspace
**🕵️ Model Detective Agency**, on lakehouse **LH_C360_Lab**, using only tables whose names start with
`dim_` or `fact_`.

**Step 1: Plan only (no changes).** List the tables and their columns. Propose the star schema:
fact tables, dimensions, relationships (from -> to, cardinality, direction, active or inactive),
the Date table, columns to hide, friendly table names, and the measures below with their DAX.
Then wait for my approval.

**Step 2: Build, after I approve.**
- Create the Direct Lake model with those tables. Rename tables: dim_customer -> Customer,
  dim_market -> Market, dim_date -> Date, dim_plan -> Plan, dim_newsletter -> Newsletter,
  dim_event -> Event, dim_advertiser -> Advertiser, fact_subscription -> Subscriptions,
  fact_web_engagement_daily -> Web Engagement, fact_newsletter_signup -> Newsletter Signups,
  fact_event_registration -> Event Registrations, fact_ad_order -> Ad Orders.
- Relationships: many-to-one, single direction, from each fact to its dimensions on the
  `*_key` columns. Date relationships: Subscriptions[start_date] (active) and
  Subscriptions[end_date] (inactive); Web Engagement[activity_date]; Newsletter
  Signups[signup_date]; Event Registrations[event_date] (active) and [registration_date]
  (inactive); Ad Orders[order_date]. Ad Orders[contact_customer_key] -> Customer[customer_key].
  Do not relate Customer to Market (Customer[home_market] is an attribute) and do not relate
  Event to Market.
- Mark Date as the date table on Date[date]. Sort Date[month_name] by Date[month_number].
- Hide every `*_key` column and technical column. Summarize By = None on keys, year and
  month_number.
- Measures (each with a description, format string and display folder):
  - **Customers**: customers in Customer, excluding the Unknown member (customer_key = -1).
  - **Active Subscriptions**: subscriptions with start_date on or before the last date in
    the current date context and end_date blank or after that date (ignore the date
    relationship inside this measure).
  - **New Subscriptions**: subscriptions by start_date.
  - **Cancellations**: subscriptions with status "Cancelled", counted by end_date
    (use the inactive relationship).
  - **Churn Rate**: Cancellations divided by Active Subscriptions (DIVIDE).
  - **Page Views**: sum of page_views.
  - **Readers**: distinct known customers (customer_key > 0) with articles_read > 0.
  - **Event Attendees**: distinct customers with attended = TRUE.
  - **Readers Who Attended Events**: known customers who are both Readers and Event
    Attendees in the same filter context.
  - **Ad Revenue**: sum of amount.
- Add descriptions to every table, visible column and measure (plain English, with synonyms).

**Step 3: Validate.** Run DAX queries for the answer-key questions (see the
validate-answer-key prompt) and show expected vs. actual side by side.
