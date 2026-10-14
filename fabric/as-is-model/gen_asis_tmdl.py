"""Generate the TMDL for the deliberately flawed 'Customer 360 - As-Is' semantic model (Import mode).
Usage: python gen_asis_tmdl.py <schema.json> <sql_server> <out_dir>
schema.json: {table: [[column, sql_type], ...]} read from the lakehouse SQL endpoint INFORMATION_SCHEMA."""
import json, os, sys
schema, server, out = json.load(open(sys.argv[1])), sys.argv[2], sys.argv[3]
TYPES = {"varchar": "string", "bigint": "int64", "float": "double", "datetime2": "dateTime"}
tables = ["pbi_customer360", "pbi_subscriptions", "pbi_web_activity", "pbi_newsletter_signups",
          "pbi_event_registrations", "pbi_ad_orders"]
os.makedirs(f"{out}/definition/tables", exist_ok=True)

def w(path, text):
    with open(f"{out}/{path}", "w", encoding="utf-8", newline="\n") as f:
        f.write(text)

w("definition.pbism", json.dumps({"version": "4.2", "settings": {}}, indent=2))
w("definition/database.tmdl", "database\n\tcompatibilityLevel: 1604\n")
# Auto date/time left ON on purpose (planted issue). No measures, no descriptions, nothing hidden.
w("definition/model.tmdl",
  "model Model\n\tculture: en-US\n\tdefaultPowerBIDataSourceVersion: powerBI_V3\n\tsourceQueryCulture: en-US\n\n"
  "\tannotation __PBI_TimeIntelligenceEnabled = 1\n\n" + "".join(f"ref table {t}\n" for t in tables))

for t in tables:
    s = f"table {t}\n\tlineageTag: {t}\n\n"
    if t == "pbi_customer360":   # planted by hand in the original setup: TODAY()-based calculated column
        s += ("\tcolumn 'Tenure Days' = DATEDIFF ( pbi_customer360[SignupDateTime], TODAY (), DAY )\n"
              "\t\tdataType: int64\n\t\tformatString: 0\n\t\tsummarizeBy: sum\n\n")
    for col, typ in schema[t]:
        dt = TYPES[typ]
        s += f"\tcolumn {col}\n\t\tdataType: {dt}\n"
        if dt == "dateTime":
            s += "\t\tformatString: General Date\n"
        s += f"\t\tsourceColumn: {col}\n\t\tsummarizeBy: {'sum' if dt in ('int64','double') else 'none'}\n\n"
    s += (f"\tpartition {t} = m\n\t\tmode: import\n\t\tsource =\n\t\t\t\tlet\n"
          f"\t\t\t\t    Source = Sql.Database(\"{server}\", \"LH_C360_Lab\"),\n"
          f"\t\t\t\t    Data = Source{{[Schema=\"dbo\",Item=\"{t}\"]}}[Data]\n\t\t\t\tin\n\t\t\t\t    Data\n")
    w(f"definition/tables/{t}.tmdl", s)

rels = [("pbi_subscriptions", "Email", True), ("pbi_web_activity", "Email", False),
        ("pbi_newsletter_signups", "Email", False), ("pbi_event_registrations", "Email", False),
        ("pbi_ad_orders", "ContactEmail", False)]
r = ""
for i, (t, c, both) in enumerate(rels, 1):
    r += f"relationship rel{i}\n"
    if both:   # planted: bi-directional filter customer <-> subscriptions
        r += "\tcrossFilteringBehavior: bothDirections\n"
    r += f"\tfromColumn: {t}.{c}\n\ttoColumn: pbi_customer360.Email\n\n"
w("definition/relationships.tmdl", r)
print("TMDL written to", out)
