# =============================================================================
# Synthetic "Customer 360" data for the semantic-model MCP lab
# -----------------------------------------------------------------------------
# 100% synthetic. No real company data, no real people. Company names are fictitious;
# e-mail domains use the reserved ".example" top-level domain.
#
# Produces two layers from the same underlying synthetic population:
#   1) AS-IS  ("pbi_*" tables)  - shaped like a typical legacy Customer 360
#      model: e-mail keys, wide snapshot table, inconsistent market names,
#      text-typed numbers, float currency, ETL columns. Used for the REVIEW demo.
#   2) GOLD   ("dim_*" / "fact_*") - a clean star schema with integer keys and
#      one shared Market table. Used for the BUILD demo.
# Plus an ANSWER KEY computed independently in pandas, so the numbers the AI
# agent produces with DAX can be checked against known-good values.
#
# Works with pandas 2.x and 3.x and numpy >= 1.24.
# =============================================================================
import numpy as np
import pandas as pd

AS_OF = pd.Timestamp("2026-09-30")
HISTORY_START = pd.Timestamp("2024-01-01")
WEB_START = pd.Timestamp("2025-10-01")
SNAPSHOT_DATE = pd.Timestamp("2026-06-30")   # the stale snapshot in the wide table
SCALES = {"small": 20_000, "demo": 150_000, "large": 600_000}

# (standard market name, region, principal city, state, zip prefix, weight, [name variants used by different source systems])
MARKETS = [
    ("Albany", "Northeast", "Albany", "NY", "122", 1.0, ["Albany", "Capital Region"]),
    ("Atlanta", "Southeast", "Atlanta", "GA", "303", 3.0, ["Atlanta", "ATL"]),
    ("Austin", "South Central", "Austin", "TX", "787", 2.0, ["Austin"]),
    ("Baltimore", "Mid-Atlantic", "Baltimore", "MD", "212", 1.5, ["Baltimore"]),
    ("Birmingham", "Southeast", "Birmingham", "AL", "352", 1.0, ["Birmingham"]),
    ("Boston", "Northeast", "Boston", "MA", "021", 3.0, ["Boston", "Boston Metro"]),
    ("Buffalo", "Northeast", "Buffalo", "NY", "142", 1.0, ["Buffalo"]),
    ("Charlotte", "Southeast", "Charlotte", "NC", "282", 2.0, ["Charlotte"]),
    ("Chicago", "Midwest", "Chicago", "IL", "606", 3.0, ["Chicago", "Chicagoland"]),
    ("Cincinnati", "Midwest", "Cincinnati", "OH", "452", 1.2, ["Cincinnati"]),
    ("Columbus", "Midwest", "Columbus", "OH", "432", 1.5, ["Columbus"]),
    ("Dallas", "South Central", "Dallas", "TX", "752", 3.0, ["Dallas", "Dallas-Fort Worth", "DFW"]),
    ("Dayton", "Midwest", "Dayton", "OH", "454", 0.8, ["Dayton"]),
    ("Denver", "Mountain", "Denver", "CO", "802", 2.0, ["Denver"]),
    ("Hawaii", "Pacific", "Honolulu", "HI", "968", 0.8, ["Hawaii", "Honolulu"]),
    ("Houston", "South Central", "Houston", "TX", "770", 2.5, ["Houston"]),
    ("Jacksonville", "Southeast", "Jacksonville", "FL", "322", 1.0, ["Jacksonville"]),
    ("Kansas City", "Midwest", "Kansas City", "MO", "641", 1.2, ["Kansas City"]),
    ("Los Angeles", "Pacific", "Los Angeles", "CA", "900", 2.5, ["Los Angeles", "LA"]),
    ("Louisville", "Southeast", "Louisville", "KY", "402", 1.0, ["Louisville"]),
    ("Memphis", "Southeast", "Memphis", "TN", "381", 0.8, ["Memphis"]),
    ("Milwaukee", "Midwest", "Milwaukee", "WI", "532", 1.0, ["Milwaukee"]),
    ("Minneapolis-St. Paul", "Midwest", "Minneapolis", "MN", "554", 2.0, ["Minneapolis-St. Paul", "Twin Cities", "Minneapolis"]),
    ("Nashville", "Southeast", "Nashville", "TN", "372", 1.5, ["Nashville"]),
    ("New Mexico", "Mountain", "Albuquerque", "NM", "871", 0.8, ["New Mexico", "Albuquerque"]),
    ("New York", "Northeast", "New York", "NY", "100", 3.0, ["New York", "NYC"]),
    ("Orlando", "Southeast", "Orlando", "FL", "328", 1.2, ["Orlando"]),
    ("Philadelphia", "Mid-Atlantic", "Philadelphia", "PA", "191", 2.0, ["Philadelphia", "Philly"]),
    ("Phoenix", "Mountain", "Phoenix", "AZ", "850", 2.0, ["Phoenix"]),
    ("Pittsburgh", "Mid-Atlantic", "Pittsburgh", "PA", "152", 1.2, ["Pittsburgh"]),
    ("Portland", "Pacific", "Portland", "OR", "972", 1.2, ["Portland"]),
    ("Sacramento", "Pacific", "Sacramento", "CA", "958", 1.0, ["Sacramento"]),
    ("San Antonio", "South Central", "San Antonio", "TX", "782", 1.2, ["San Antonio"]),
    ("San Francisco", "Pacific", "San Francisco", "CA", "941", 2.5, ["San Francisco", "Bay Area"]),
    ("San Jose", "Pacific", "San Jose", "CA", "951", 1.5, ["San Jose", "Silicon Valley"]),
    ("Seattle", "Pacific", "Seattle", "WA", "981", 2.0, ["Seattle", "Puget Sound"]),
    ("South Florida", "Southeast", "Miami", "FL", "331", 2.5, ["South Florida", "Miami"]),
    ("St. Louis", "Midwest", "St. Louis", "MO", "631", 1.2, ["St. Louis"]),
    ("Tampa Bay", "Southeast", "Tampa", "FL", "336", 1.5, ["Tampa Bay", "Tampa"]),
    ("Triad", "Southeast", "Greensboro", "NC", "274", 0.8, ["Triad", "Greensboro"]),
    ("Triangle", "Southeast", "Raleigh", "NC", "276", 1.5, ["Triangle", "Raleigh-Durham"]),
    ("Washington", "Mid-Atlantic", "Washington", "DC", "200", 3.0, ["Washington", "Washington DC", "DC"]),
    ("Wichita", "Midwest", "Wichita", "KS", "672", 0.6, ["Wichita"]),
]

FIRST = ["James","Mary","Robert","Patricia","John","Jennifer","Michael","Linda","David","Elizabeth","William","Barbara",
         "Richard","Susan","Joseph","Jessica","Thomas","Sarah","Carlos","Karen","Daniel","Lisa","Matthew","Nancy","Anthony",
         "Betty","Mark","Sandra","Donald","Ashley","Steven","Kimberly","Andrew","Emily","Paul","Donna","Joshua","Michelle",
         "Kenneth","Carol","Kevin","Amanda","Brian","Melissa","Priya","Deborah","Wei","Stephanie","Luis","Rebecca","Ahmed",
         "Laura","Ryan","Sharon","Jacob","Cynthia","Gary","Kathleen","Nicholas","Amy","Eric","Angela","Jonathan","Rocio",
         "Diego","Mei","Omar","Fatima","Hiro","Ana"]
LAST = ["Smith","Johnson","Williams","Brown","Jones","Garcia","Miller","Davis","Rodriguez","Martinez","Hernandez","Lopez",
        "Gonzalez","Wilson","Anderson","Thomas","Taylor","Moore","Jackson","Martin","Lee","Perez","Thompson","White","Harris",
        "Sanchez","Clark","Ramirez","Lewis","Robinson","Walker","Young","Allen","King","Wright","Scott","Torres","Nguyen",
        "Hill","Flores","Green","Adams","Nelson","Baker","Hall","Rivera","Campbell","Mitchell","Carter","Roberts","Patel",
        "Chen","Kim","Singh","Okafor","Novak","Rossi","Schmidt","Kowalski","Ivanova","Tanaka","Silva","Cohen","Murphy",
        "Bennett","Brooks","Price","Hughes","Foster","Reed"]
CO_PREFIX = ["Apex","Summit","Harbor","Pinnacle","Riverbend","Keystone","Lakeside","Ironwood","Bluewater","Granite",
             "Meridian","Cedar","Northstar","Silverline","Oakmont","Crescent","Liberty","Beacon","Contoso","Fabrikam",
             "Northwind","Tailspin","Woodgrove","Litware","Proseware","Relecloud","Wingtip","Lucerne","Alpine","Coho"]
CO_SUFFIX = ["Capital","Health","Builders","Logistics","Realty","Bank","Partners","Technologies","Law Group","Insurance",
             "Energy","Foods","Manufacturing","Hospitality","Media","Consulting","Architects","Advisors"]
TITLES = ["CEO","CFO","President","Owner","Founder","Managing Partner","VP Marketing","Head of Marketing","Director of Sales",
          "Sales Manager","HR Director","Controller","Financial Analyst","Account Executive","Attorney","Commercial Broker",
          "Developer","Banker","Consultant","Office Manager"]
NEWSLETTERS = [  # name, topic, frequency
    ("Morning Edition","General business","Daily"),("Afternoon Edition","General business","Daily"),
    ("Weekly Recap","General business","Weekly"),("Commercial Real Estate","Real estate","Weekly"),
    ("Residential Real Estate","Real estate","Weekly"),("Health Care","Health care","Weekly"),
    ("Technology","Technology","Weekly"),("Banking & Finance","Finance","Weekly"),
    ("Startups & Innovation","Technology","Weekly"),("Events Insider","Events","Monthly")]
EVENT_FRANCHISES = [  # name, type, base ticket price
    ("Rising Leaders 40","Awards",95.0),("Top Workplaces Awards","Awards",85.0),("Finance Leader of the Year","Awards",110.0),
    ("Women in Business Awards","Awards",95.0),("Annual Lists Celebration","Networking",65.0),
    ("Commercial Real Estate Awards","Awards",120.0),("Fast Growth 50","Awards",90.0),("Health Care Heroes","Awards",85.0),
    ("Power Breakfast","Forum",55.0),("Innovation Summit","Forum",149.0),("C-Suite Awards","Awards",125.0),
    ("Top CEO Awards","Awards",125.0)]
PLANS = [  # plan_key, plan_name, product_type, billing_cycle, list_price, weight
    (1,"Digital Monthly","Digital","Monthly",19.99,0.30),(2,"Digital Annual","Digital","Annual",179.00,0.30),
    (3,"Print + Digital Annual","Print + Digital","Annual",249.00,0.20),(4,"All-Access Annual","All-Access","Annual",399.00,0.08),
    (5,"Enterprise Seat","Enterprise","Annual",99.00,0.12)]
AD_PRODUCTS = [("Digital Display",0.30,4500.0),("Newsletter Sponsorship",0.20,2500.0),("Print Full Page",0.12,9000.0),
               ("Print Half Page",0.12,5200.0),("Event Sponsorship",0.14,7500.0),("Sponsored Content",0.12,6000.0)]
CANCEL_REASONS = ["Price","Not enough local coverage","Moved to enterprise license","Payment failed","Too many emails","Other"]
CHANNELS = ["Website","Email campaign","Direct mail","Event bundle","Sales rep","Newsletter promo"]
DEVICES = ["Desktop","Mobile","Tablet","App"]


def _days(n):
    return pd.to_timedelta(n, unit="D")


def _rand_dates(rng, start, end, n):
    span = (end - start).days
    return start + _days(rng.integers(0, span + 1, n))


def _variant(rng, market_idx, source_bias, n=None):
    """Pick a market-name variant. Each source system has its own habit:
    source_bias = probability of using a NON-standard variant when one exists."""
    market_idx = np.asarray(market_idx)
    out = np.empty(market_idx.shape[0], dtype=object)
    use_alt = rng.random(market_idx.shape[0]) < source_bias
    for i, m in enumerate(MARKETS):
        mask = market_idx == i
        if not mask.any():
            continue
        variants = m[6]
        if len(variants) == 1:
            out[mask] = variants[0]
        else:
            alt = rng.integers(1, len(variants), mask.sum())
            chosen = np.where(use_alt[mask], np.array(variants, dtype=object)[alt], variants[0])
            out[mask] = chosen
    return out


def generate(scale="demo", seed=2026):
    """Return (asis: dict[str, DataFrame], gold: dict[str, DataFrame])."""
    n = SCALES[scale] if isinstance(scale, str) else int(scale)
    rng = np.random.default_rng(seed)

    # ------------------------------------------------------------------ markets
    w = np.array([m[5] for m in MARKETS]); w = w / w.sum()
    dim_market = pd.DataFrame({
        "market_key": np.arange(1, len(MARKETS) + 1, dtype="int64"),
        "market_name": [m[0] for m in MARKETS],
        "region": [m[1] for m in MARKETS],
        "principal_city": [m[2] for m in MARKETS],
        "state": [m[3] for m in MARKETS],
        "legacy_name_variants": [", ".join(m[6]) for m in MARKETS],
    })

    # ---------------------------------------------------------------- customers
    ck = np.arange(1, n + 1, dtype="int64")
    mkt = rng.choice(len(MARKETS), n, p=w)
    fn = np.array(FIRST, dtype=object)[rng.integers(0, len(FIRST), n)]
    ln = np.array(LAST, dtype=object)[rng.integers(0, len(LAST), n)]
    companies = np.array([f"{p} {s}" for p in CO_PREFIX for s in CO_SUFFIX], dtype=object)
    comp_idx = rng.integers(0, len(companies), n)
    company = companies[comp_idx]
    personal = rng.random(n) < 0.35
    domain = np.where(personal, "mail.example",
                      pd.Series(company).str.lower().str.replace(" ", "", regex=False).str.replace("&", "and", regex=False).to_numpy() + ".example")
    email = (pd.Series(fn).str.lower() + "." + pd.Series(ln).str.lower() + "." + pd.Series(ck).astype(str) + "@" + pd.Series(domain)).to_numpy()
    title = np.array(TITLES, dtype=object)[rng.integers(0, len(TITLES), n)]
    is_ent = (~personal) & (rng.random(n) < 0.12)
    signup = _rand_dates(rng, pd.Timestamp("2015-01-01"), AS_OF - pd.Timedelta(days=1), n)
    zip_prefix = np.array([m[4] for m in MARKETS], dtype=object)[mkt]
    postal = (pd.Series(zip_prefix) + pd.Series(rng.integers(0, 100, n)).astype(str).str.zfill(2)).to_numpy()
    city = np.array([m[2] for m in MARKETS], dtype=object)[mkt]
    state = np.array([m[3] for m in MARKETS], dtype=object)[mkt]

    # ------------------------------------------------------------ subscriptions
    n_subs = rng.choice([0, 1, 2, 3], n, p=[0.30, 0.50, 0.15, 0.05])
    s_cust = np.repeat(np.arange(n), n_subs)
    m_s = s_cust.shape[0]
    plan_w = np.array([p[5] for p in PLANS])
    plan_idx = np.empty(m_s, dtype=int)
    ent_mask = is_ent[s_cust]
    plan_idx[~ent_mask] = rng.choice(len(PLANS), (~ent_mask).sum(), p=plan_w / plan_w.sum())
    pw_ent = np.array([0.05, 0.10, 0.05, 0.10, 0.70])
    plan_idx[ent_mask] = rng.choice(len(PLANS), ent_mask.sum(), p=pw_ent)
    start = _rand_dates(rng, HISTORY_START, AS_OF, m_s)
    monthly = np.array([PLANS[i][3] == "Monthly" for i in plan_idx])
    months = rng.geometric(0.06, m_s)
    years = rng.geometric(0.35, m_s)
    dur_days = np.where(monthly, months * 30, years * 365)
    end = start + _days(dur_days)
    active = end > AS_OF
    end = end.where(~active, pd.NaT)
    cancelled = (~active) & (rng.random(m_s) < 0.70)
    status = np.where(active, "Active", np.where(cancelled, "Cancelled", "Expired")).astype(object)
    reason = np.where(cancelled, np.array(CANCEL_REASONS, dtype=object)[rng.integers(0, len(CANCEL_REASONS), m_s)], None)
    channel = np.array(CHANNELS, dtype=object)[rng.integers(0, len(CHANNELS), m_s)]
    s_mkt = np.where(rng.random(m_s) < 0.92, mkt[s_cust], rng.choice(len(MARKETS), m_s, p=w))
    list_price = np.array([PLANS[i][4] for i in plan_idx])
    monthly_price = np.where(monthly, list_price, list_price / 12.0)
    sub_id = np.array([f"CB-{x:07d}" for x in rng.permutation(np.arange(1000000, 1000000 + m_s))], dtype=object)

    fact_subscription = pd.DataFrame({
        "subscription_id": sub_id,
        "customer_key": ck[s_cust],
        "plan_key": np.array([PLANS[i][0] for i in plan_idx], dtype="int64"),
        "market_key": (s_mkt + 1).astype("int64"),
        "start_date": start.normalize(),
        "end_date": end.normalize(),
        "status": status,
        "monthly_price": np.round(monthly_price, 2),
        "sales_channel": channel,
        "cancel_reason": reason,
    })

    # ------------------------------------------------------------- web activity
    has_active = np.zeros(n, dtype=bool); has_active[s_cust[active]] = True
    had_sub = n_subs > 0
    lam = np.where(has_active, 14.0, np.where(had_sub, 4.0, 2.0))
    n_days = rng.poisson(lam)
    w_cust = np.repeat(np.arange(n), n_days)
    m_w = w_cust.shape[0]
    w_date = _rand_dates(rng, WEB_START, AS_OF, m_w)
    w_ts = w_date + pd.to_timedelta(rng.integers(0, 86400, m_w), unit="s")
    sessions = 1 + rng.poisson(0.5, m_w)
    page_views = sessions * (1 + rng.poisson(3, m_w))
    articles = rng.binomial(page_views, 0.6)
    device = np.array(DEVICES, dtype=object)[rng.choice(4, m_w, p=[0.45, 0.35, 0.05, 0.15])]
    # ~1.5% of activity comes from readers who are not in the customer table (orphans)
    n_orphan = int(round(m_w * 0.015))
    orphan_ids = rng.integers(1, max(2, n // 10), n_orphan)
    orphan_mkt = rng.choice(len(MARKETS), n_orphan, p=w)
    o_date = _rand_dates(rng, WEB_START, AS_OF, n_orphan)
    o_ts = o_date + pd.to_timedelta(rng.integers(0, 86400, n_orphan), unit="s")
    o_sessions = 1 + rng.poisson(0.3, n_orphan)
    o_pv = o_sessions * (1 + rng.poisson(2, n_orphan))
    o_art = rng.binomial(o_pv, 0.6)
    o_dev = np.array(DEVICES, dtype=object)[rng.integers(0, 4, n_orphan)]

    web_all = pd.DataFrame({
        "customer_key": np.concatenate([ck[w_cust], np.full(n_orphan, -1, dtype="int64")]),
        "email": np.concatenate([email[w_cust], np.array([f"reader{x}@mail.example" for x in orphan_ids], dtype=object)]),
        "market_idx": np.concatenate([mkt[w_cust], orphan_mkt]),
        "activity_ts": np.concatenate([w_ts.to_numpy(), o_ts.to_numpy()]),
        "sessions": np.concatenate([sessions, o_sessions]).astype("int64"),
        "page_views": np.concatenate([page_views, o_pv]).astype("int64"),
        "articles_read": np.concatenate([articles, o_art]).astype("int64"),
        "device_type": np.concatenate([device, o_dev]),
    })
    web_all["activity_date"] = pd.to_datetime(web_all["activity_ts"]).dt.normalize()

    # -------------------------------------------------------------- newsletters
    n_nl = np.minimum(rng.poisson(1.2, n), 5)
    nl_cust = np.repeat(np.arange(n), n_nl)
    nl_idx = rng.integers(0, len(NEWSLETTERS), nl_cust.shape[0])
    nl = pd.DataFrame({"cust": nl_cust, "nl": nl_idx}).drop_duplicates().reset_index(drop=True)
    m_n = len(nl)
    lo = np.maximum(signup[nl["cust"].to_numpy()].to_numpy(), np.datetime64("2022-01-01"))
    span = (np.datetime64(AS_OF.date()) - lo.astype("datetime64[D]")).astype(int)
    nl_signup = pd.to_datetime(lo).normalize() + _days(np.floor(rng.random(m_n) * np.maximum(span, 1)).astype(int))
    unsub = rng.random(m_n) < 0.20
    nl_status = np.where(unsub, "Unsubscribed", "Subscribed").astype(object)
    open_rate = np.where(unsub, rng.random(m_n) * 0.15, 0.15 + rng.random(m_n) * 0.55)
    dim_newsletter = pd.DataFrame({
        "newsletter_key": np.arange(1, len(NEWSLETTERS) + 1, dtype="int64"),
        "newsletter_name": [x[0] for x in NEWSLETTERS], "topic": [x[1] for x in NEWSLETTERS],
        "frequency": [x[2] for x in NEWSLETTERS]})
    fact_newsletter = pd.DataFrame({
        "customer_key": ck[nl["cust"].to_numpy()],
        "newsletter_key": (nl["nl"].to_numpy() + 1).astype("int64"),
        "market_key": (mkt[nl["cust"].to_numpy()] + 1).astype("int64"),
        "signup_date": nl_signup,
        "status": nl_status,
        "open_rate": np.round(open_rate, 4),
    })

    # ------------------------------------------------------------------- events
    ev_rows = []
    ek = 1
    for mi, m in enumerate(MARKETS):
        n_ev = int(round(8 + m[5] * 4))
        fr_idx = rng.choice(len(EVENT_FRANCHISES), n_ev, replace=True)
        dates = _rand_dates(rng, HISTORY_START, AS_OF, n_ev)
        for f, d in zip(fr_idx, dates):
            fr = EVENT_FRANCHISES[f]
            ev_rows.append((ek, f"{m[0]} {fr[0]} {d.year}", fr[0], fr[1], mi + 1, d.normalize(), fr[2]))
            ek += 1
    dim_event = pd.DataFrame(ev_rows, columns=["event_key", "event_name", "event_franchise", "event_type",
                                               "market_key", "event_date", "base_ticket_price"])
    p_reg = np.where(has_active, 0.22, 0.06) + np.where(is_ent, 0.10, 0.0)
    n_reg = rng.poisson(p_reg)
    r_cust = np.repeat(np.arange(n), n_reg)
    m_r = r_cust.shape[0]
    r_mkt = mkt[r_cust]
    r_event = np.empty(m_r, dtype="int64")
    for mi in range(len(MARKETS)):
        mask = r_mkt == mi
        if mask.any():
            evs = dim_event.loc[dim_event["market_key"] == mi + 1, "event_key"].to_numpy()
            r_event[mask] = evs[rng.integers(0, len(evs), mask.sum())]
    ev_lookup = dim_event.set_index("event_key")
    ev_date = ev_lookup.loc[r_event, "event_date"].to_numpy()
    reg_date = pd.to_datetime(ev_date) - _days(rng.integers(1, 60, m_r))
    tt = rng.choice(["General admission", "VIP", "Table", "Sponsor comp"], m_r, p=[0.70, 0.12, 0.10, 0.08])
    base = ev_lookup.loc[r_event, "base_ticket_price"].to_numpy()
    price = np.where(tt == "VIP", base * 1.8, np.where(tt == "Table", base * 8, np.where(tt == "Sponsor comp", 0.0, base)))
    attended = rng.random(m_r) < 0.85
    fact_event = pd.DataFrame({
        "customer_key": ck[r_cust], "event_key": r_event, "market_key": (r_mkt + 1).astype("int64"),
        "registration_date": reg_date.normalize(), "event_date": pd.to_datetime(ev_date),
        "ticket_type": tt.astype(object), "ticket_price": np.round(price, 2), "attended": attended})
    fact_event = fact_event.drop_duplicates(subset=["customer_key", "event_key"]).reset_index(drop=True)

    # ---------------------------------------------------------------- advertising
    used_companies = np.unique(company[~personal])
    n_adv = min(len(used_companies), 400)
    adv_names = rng.choice(used_companies, n_adv, replace=False)
    industry = pd.Series(adv_names).str.split(" ", n=1).str[1].to_numpy()
    dim_advertiser = pd.DataFrame({"advertiser_key": np.arange(1, n_adv + 1, dtype="int64"),
                                   "advertiser_name": adv_names, "industry": industry})
    n_orders = 1 + rng.poisson(12, n_adv)
    a_adv = np.repeat(np.arange(n_adv), n_orders)
    m_a = a_adv.shape[0]
    prod_p = np.array([p[1] for p in AD_PRODUCTS]); prod_idx = rng.choice(len(AD_PRODUCTS), m_a, p=prod_p / prod_p.sum())
    amount = np.array([p[2] for p in AD_PRODUCTS])[prod_idx] * (0.6 + rng.random(m_a) * 0.9)
    is_digital = np.isin(prod_idx, [0, 1, 5])
    impressions = np.where(is_digital, rng.integers(20_000, 400_000, m_a), 0)
    a_mkt = rng.choice(len(MARKETS), m_a, p=w)
    a_date = _rand_dates(rng, HISTORY_START, AS_OF, m_a)
    # contact: an employee of the advertiser who is also in the customer table (if any), else unknown
    cust_by_company = pd.DataFrame({"company": company, "ck": ck, "email": email})[~personal].groupby("company").first()
    contact_ck = cust_by_company.reindex(adv_names[a_adv])["ck"].to_numpy()
    contact_email = cust_by_company.reindex(adv_names[a_adv])["email"].to_numpy()
    no_contact = rng.random(m_a) < 0.35
    contact_ck = np.where(no_contact | pd.isna(contact_ck), -1, contact_ck).astype("int64")
    contact_email = np.where(contact_ck == -1, np.array([f"marketing{x}@agency.example" for x in rng.integers(1, 500, m_a)], dtype=object), contact_email)
    fact_ad_order = pd.DataFrame({
        "order_id": np.array([f"AD-{x:06d}" for x in range(1, m_a + 1)], dtype=object),
        "advertiser_key": (a_adv + 1).astype("int64"), "contact_customer_key": contact_ck,
        "market_key": (a_mkt + 1).astype("int64"), "order_date": a_date.normalize(),
        "ad_product": np.array([p[0] for p in AD_PRODUCTS], dtype=object)[prod_idx],
        "impressions": impressions.astype("int64"), "amount": np.round(amount, 2)})

    # ---------------------------------------------------------------- dim_date
    d = pd.date_range(pd.Timestamp("2015-01-01"), pd.Timestamp("2026-12-31"), freq="D")
    dim_date = pd.DataFrame({
        "date": d, "date_key": (d.year * 10000 + d.month * 100 + d.day).astype("int64"),
        "year": d.year.astype("int64"), "quarter": ("Q" + d.quarter.astype(str)).astype(object),
        "month_number": d.month.astype("int64"), "month_name": d.strftime("%B").astype(object),
        "year_month": d.strftime("%Y-%m").astype(object),
        "week_start_date": (d - pd.to_timedelta(d.dayofweek, unit="D")),
        "day_of_week": d.strftime("%A").astype(object), "is_weekend": (d.dayofweek >= 5)})

    # ------------------------------------------------------------- dim_customer
    dim_customer = pd.DataFrame({
        "customer_key": ck, "email": email, "first_name": fn, "last_name": ln, "company_name": np.where(personal, None, company),
        "job_title": title, "city": city, "state": state, "postal_code": postal,
        "home_market": np.array([m[0] for m in MARKETS], dtype=object)[mkt], "market_key": (mkt + 1).astype("int64"),
        "signup_date": signup.normalize(), "is_enterprise": is_ent,
        "enterprise_account_name": np.where(is_ent, company, None)})
    unknown = pd.DataFrame([{"customer_key": -1, "email": "(unknown reader)", "first_name": "Unknown", "last_name": "Reader",
                             "company_name": None, "job_title": None, "city": None, "state": None, "postal_code": None,
                             "home_market": "Unknown", "market_key": -1, "signup_date": pd.NaT, "is_enterprise": False, "enterprise_account_name": None}])
    dim_customer = pd.concat([unknown, dim_customer], ignore_index=True)
    dim_market = pd.concat([pd.DataFrame([{"market_key": -1, "market_name": "Unknown", "region": "Unknown",
                                           "principal_city": None, "state": None, "legacy_name_variants": None}]), dim_market],
                           ignore_index=True)

    # gold web fact at daily grain
    fact_web = (web_all.assign(market_key=(web_all["market_idx"] + 1).astype("int64"))
                .groupby(["customer_key", "activity_date", "market_key", "device_type"], as_index=False)
                .agg(sessions=("sessions", "sum"), page_views=("page_views", "sum"), articles_read=("articles_read", "sum")))

    gold = {"dim_customer": dim_customer, "dim_market": dim_market, "dim_date": dim_date,
            "dim_plan": pd.DataFrame([p[:5] for p in PLANS], columns=["plan_key", "plan_name", "product_type", "billing_cycle", "list_price"]),
            "dim_newsletter": dim_newsletter, "dim_event": dim_event.drop(columns=["base_ticket_price"]),
            "dim_advertiser": dim_advertiser, "fact_subscription": fact_subscription,
            "fact_web_engagement_daily": fact_web, "fact_newsletter_signup": fact_newsletter,
            "fact_event_registration": fact_event, "fact_ad_order": fact_ad_order}

    # =========================================================== AS-IS tables
    cust_idx = {k: i for i, k in enumerate(ck)}
    # pbi_subscriptions  (Chargebee-style: mostly standard market names)
    s_m_idx = fact_subscription["market_key"].to_numpy() - 1
    pbi_subscriptions = pd.DataFrame({
        "SubscriptionID": fact_subscription["subscription_id"],
        "Email": email[fact_subscription["customer_key"].to_numpy() - 1],
        "PlanName": np.array([p[1] for p in PLANS], dtype=object)[fact_subscription["plan_key"].to_numpy() - 1],
        "MarketName": _variant(rng, s_m_idx, 0.15),
        "StartDate": fact_subscription["start_date"] + pd.to_timedelta(rng.integers(0, 86400, m_s), unit="s"),
        "EndDate": fact_subscription["end_date"],
        "sub_sts": fact_subscription["status"].map({"Active": "A", "Cancelled": "C", "Expired": "E"}),
        "plan_prc": monthly_price,                      # float, unrounded
        "bill_cyc": np.where(monthly, "M", "A").astype(object),
        "chnl": fact_subscription["sales_channel"],
        "CancelReason": fact_subscription["cancel_reason"],
        "_etl_load_ts": pd.Timestamp("2026-10-01 06:12:00"),
        "_source_file": "chargebee_export_20261001.csv"})

    # pbi_web_activity  (web analytics: prefers the nickname variants)
    pbi_web_activity = pd.DataFrame({
        "Email": web_all["email"], "ActivityDateTime": web_all["activity_ts"],
        "MarketName": _variant(rng, web_all["market_idx"].to_numpy(), 0.80),
        "Sessions": web_all["sessions"], "PageViews": web_all["page_views"], "ArticlesRead": web_all["articles_read"],
        "DeviceType": web_all["device_type"],
        "row_hash": pd.util.hash_pandas_object(web_all[["email", "activity_ts"]], index=False).astype(str).to_numpy(),
        "_etl_load_ts": pd.Timestamp("2026-10-01 06:40:00")})

    # pbi_newsletter_signups  (e-mail platform: mixed naming)
    pbi_newsletter_signups = pd.DataFrame({
        "Email": email[fact_newsletter["customer_key"].to_numpy() - 1],
        "NewsletterName": np.array([x[0] for x in NEWSLETTERS], dtype=object)[fact_newsletter["newsletter_key"].to_numpy() - 1],
        "MarketName": _variant(rng, fact_newsletter["market_key"].to_numpy() - 1, 0.50),
        "SignupDate": fact_newsletter["signup_date"], "Status": fact_newsletter["status"],
        "OpenRate": open_rate, "_etl_load_ts": pd.Timestamp("2026-10-01 05:55:00")})

    # pbi_event_registrations  (ticketing: price as text, attended as Y/N)
    pbi_event_registrations = pd.DataFrame({
        "Email": email[fact_event["customer_key"].to_numpy() - 1],
        "EventName": ev_lookup.loc[fact_event["event_key"].to_numpy(), "event_name"].to_numpy(),
        "EventDate": fact_event["event_date"], "MarketName": _variant(rng, fact_event["market_key"].to_numpy() - 1, 0.40),
        "TicketType": fact_event["ticket_type"],
        "TicketPrice": ("$" + pd.Series(fact_event["ticket_price"]).map(lambda v: f"{v:,.2f}")).to_numpy(),
        "Attended": np.where(fact_event["attended"], "Y", "N").astype(object),
        "_etl_load_ts": pd.Timestamp("2026-10-01 06:05:00")})

    # pbi_ad_orders  (ad system: advertiser + contact e-mail)
    pbi_ad_orders = pd.DataFrame({
        "OrderID": fact_ad_order["order_id"],
        "AdvertiserName": adv_names[fact_ad_order["advertiser_key"].to_numpy() - 1],
        "ContactEmail": contact_email, "MarketName": _variant(rng, fact_ad_order["market_key"].to_numpy() - 1, 0.50),
        "OrderDate": fact_ad_order["order_date"] + pd.to_timedelta(rng.integers(0, 86400, m_a), unit="s"),
        "AdProduct": fact_ad_order["ad_product"], "Impressions": fact_ad_order["impressions"],
        "Amount": amount, "_etl_load_ts": pd.Timestamp("2026-10-01 06:20:00")})

    # pbi_customer360  (wide, e-mail keyed, stale snapshot aggregates)
    latest = fact_subscription.sort_values("start_date").groupby("customer_key").tail(1).set_index("customer_key")
    lat = latest.reindex(ck)
    snap_web = web_all[(web_all["customer_key"] > 0) & (web_all["activity_date"] <= SNAPSHOT_DATE)]
    pv_snap = snap_web.groupby("customer_key")["page_views"].sum().reindex(ck).fillna(0).astype("int64").to_numpy()
    last_seen = web_all[web_all["customer_key"] > 0].groupby("customer_key")["activity_ts"].max().reindex(ck)
    last_seen = last_seen.fillna(pd.Series(signup.to_numpy(), index=ck)).to_numpy()
    ev_snap = fact_event[fact_event["registration_date"] <= SNAPSHOT_DATE].groupby("customer_key").size().reindex(ck).fillna(0).astype("int64").to_numpy()
    nl_cnt = fact_newsletter[fact_newsletter["status"] == "Subscribed"].groupby("customer_key").size().reindex(ck).fillna(0).astype("int64").to_numpy()
    lat_status = lat["status"].map({"Active": "A", "Cancelled": "C", "Expired": "E"}).fillna("N").to_numpy()
    seg = np.where(is_ent, "Enterprise", np.where(lat_status == "A", "Subscriber", np.where(np.isin(lat_status, ["C", "E"]), "Lapsed", "Prospect")))
    headlines = np.array(["expands headquarters", "names new CEO", "lands major contract", "plans layoffs",
                          "opens new office", "acquires rival", "raises Series B", "breaks ground on project"], dtype=object)
    renewal = (lat["start_date"] + pd.to_timedelta(365, unit="D")).where(lat["status"] == "Active")
    pbi_customer360 = pd.DataFrame({
        "Email": email, "FirstName": fn, "LastName": ln, "FullName": (pd.Series(fn) + " " + pd.Series(ln)).to_numpy(),
        "Company": np.where(personal, None, company), "JobTitle": title,
        "MarketName": _variant(rng, mkt, 0.45), "City": city, "State": state,
        "PostalCode": pd.Series(postal).astype("int64").to_numpy(),        # leading zeros lost on purpose
        "SignupDateTime": signup + pd.to_timedelta(rng.integers(0, 86400, n), unit="s"),
        "LastSeenDateTime": last_seen, "sub_sts": lat_status,
        "CurrentPlan": np.array([None] + [p[1] for p in PLANS], dtype=object)[lat["plan_key"].fillna(0).astype(int).to_numpy()],
        "plan_prc": lat["monthly_price"].to_numpy() * (1 + rng.random(n) * 1e-9),
        "RenewalDate": renewal.to_numpy(), "IsEnterprise": np.where(is_ent, "TRUE", "FALSE").astype(object),
        "EnterpriseAccountName": np.where(is_ent, company, None),
        "NewsletterCount": nl_cnt, "EventCount": ev_snap, "LifetimePageViews": pv_snap,
        "LastArticleTitle": (pd.Series(city) + " " + pd.Series(company).fillna("Local firm") + " " +
                             pd.Series(headlines[rng.integers(0, len(headlines), n)])).to_numpy(),
        "CustomerSegment": seg.astype(object),
        "_etl_load_ts": pd.Timestamp("2026-10-01 07:00:00"),
        "row_hash": pd.util.hash_pandas_object(pd.DataFrame({"e": email}), index=False).astype(str).to_numpy()})

    asis = {"pbi_customer360": pbi_customer360, "pbi_subscriptions": pbi_subscriptions,
            "pbi_web_activity": pbi_web_activity, "pbi_newsletter_signups": pbi_newsletter_signups,
            "pbi_event_registrations": pbi_event_registrations, "pbi_ad_orders": pbi_ad_orders}
    return asis, gold


def answer_key(asis, gold):
    """Known-good answers, computed in pandas, to check the agent's DAX results."""
    fs, fw, fe = gold["fact_subscription"], gold["fact_web_engagement_daily"], gold["fact_event_registration"]
    fa, dm, dc = gold["fact_ad_order"], gold["dim_market"], gold["dim_customer"]
    q3s, q3e = pd.Timestamp("2026-07-01"), pd.Timestamp("2026-09-30")
    h_s = pd.Timestamp("2026-04-01")
    active_asof = fs[(fs["start_date"] <= AS_OF) & (fs["end_date"].isna() | (fs["end_date"] > AS_OF))]
    readers = set(fw[(fw["activity_date"] >= h_s) & (fw["activity_date"] <= AS_OF) & (fw["articles_read"] > 0) & (fw["customer_key"] > 0)]["customer_key"])
    attendees = set(fe[(fe["event_date"] >= h_s) & (fe["event_date"] <= AS_OF) & (fe["attended"])]["customer_key"])
    sf_key = int(dm.loc[dm["market_name"] == "South Florida", "market_key"].iloc[0])
    ad26 = fa[(fa["order_date"] >= pd.Timestamp("2026-01-01")) & (fa["order_date"] <= AS_OF)]
    top5 = (ad26.merge(dm[["market_key", "market_name"]], on="market_key").groupby("market_name")["amount"].sum()
            .sort_values(ascending=False).head(5))
    asis_sub = asis["pbi_subscriptions"]
    asis_sf_active = int(((asis_sub["MarketName"] == "South Florida") & (asis_sub["sub_sts"] == "A")).sum())
    web = asis["pbi_web_activity"]
    orphan_rows = int((~web["Email"].isin(set(asis["pbi_customer360"]["Email"]))).sum())
    c360_pv = int(asis["pbi_customer360"]["LifetimePageViews"].sum())
    fact_pv_to_snapshot = int(fw[(fw["customer_key"] > 0) & (fw["activity_date"] <= SNAPSHOT_DATE)]["page_views"].sum())
    rows = [
        ("Q01", "Customers (excluding the Unknown member)", int((dc["customer_key"] > 0).sum())),
        ("Q02", "Active subscriptions as of 2026-09-30", len(active_asof)),
        ("Q03", "New subscriptions started in Q3 2026 (Jul 1 - Sep 30)", int(((fs["start_date"] >= q3s) & (fs["start_date"] <= q3e)).sum())),
        ("Q04", "Cancellations in Q3 2026 (status Cancelled, end date in Q3)", int(((fs["status"] == "Cancelled") & (fs["end_date"] >= q3s) & (fs["end_date"] <= q3e)).sum())),
        ("Q05", "Page views in September 2026 (all readers incl. unknown)", int(fw[(fw["activity_date"] >= pd.Timestamp("2026-09-01")) & (fw["activity_date"] <= AS_OF)]["page_views"].sum())),
        ("Q06", "Known customers who read >=1 article AND attended >=1 event, Apr 1 - Sep 30 2026", len(readers & attendees)),
        ("Q07", "Ad revenue 2026 YTD (Jan 1 - Sep 30), USD", round(float(ad26["amount"].sum()), 2)),
        ("Q08", "Active subscriptions as of 2026-09-30 in South Florida (gold, one Market table)", int((active_asof["market_key"] == sf_key).sum())),
        ("Q09", "AS-IS: rows tagged exactly 'South Florida' with status A (misses 'Miami')", asis_sf_active),
        ("Q10", "AS-IS: web activity rows whose Email is not in pbi_customer360 (orphans)", orphan_rows),
        ("Q11", "AS-IS: LifetimePageViews total in the wide table (stale snapshot)", c360_pv),
        ("Q12", "GOLD: page views by known customers through 2026-06-30 (should equal Q11)", fact_pv_to_snapshot),
        ("Q13", "GOLD: page views by known customers through 2026-09-30 (today's number; Q11 is stale)", int(fw[(fw["customer_key"] > 0) & (fw["activity_date"] <= AS_OF)]["page_views"].sum())),
    ]
    for i, (m, v) in enumerate(top5.items(), start=1):
        rows.append((f"Q07.{i}", f"Ad revenue 2026 YTD, rank {i} market: {m}", round(float(v), 2)))
    return pd.DataFrame(rows, columns=["question_id", "question", "expected_value"])


if __name__ == "__main__":
    import sys, time
    scale = sys.argv[1] if len(sys.argv) > 1 else "small"
    t = time.time()
    asis, gold = generate(scale)
    print(f"generated '{scale}' in {time.time() - t:.1f}s")
    for k, v in {**asis, **gold}.items():
        print(f"{k:28s} {len(v):>10,d} rows  {v.shape[1]:>3d} cols")
    print(answer_key(asis, gold).to_string(index=False))
