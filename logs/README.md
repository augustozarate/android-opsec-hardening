# Manual – NextDNS Log Import

This guide describes **how to manually import** DNS logs exported from **NextDNS** and convert them into a clean domain list for further analysis.

---

## 1. `logs/` Directory

The `logs/` directory is used **exclusively** to store CSV files exported from NextDNS.


Example:

```
logs/
└── nextdns-export.csv
```
⚠️ These files are considered raw data (raw logs) and must not be edited manually.
⚠️ This directory is ignored by git by design (see .gitignore).
---
## 2. Export Data from NextDNS

Access the NextDNS dashboard

Export logs in CSV format

Save the file as:
```
logs/nextdns-export.csv
```
---
## 3. Generate - `dns_queries.txt`
From the project root, run the following command:
```
cut -d',' -f2 logs/nextdns-export.csv | tail -n +2 > opsec/data/dns_queries.txt
```
Note: If your CSV uses `;` instead of `,`, adjust the command accordingly:
```cut -d';' -f2 logs/nextdns-export.csv | tail -n +2 > opsec/data/dns_queries.txt
```
What does this command do?

- Extracts the column containing DNS domains
- Removes the CSV header row
- Produces a clean file with one domain per line
Import is intentionally manual (no automation) to preserve OPSEC control.
---
## 4. Quick Verification

Check the generated output:
```
head opsec/data/dns_queries.txt
```
The file should contain only domains, for example:
```
google.com
firebaseinstallations.googleapis.com
graph.facebook.com
pool.ntp.org
```
---
## 5. OPSEC Notes

Import is 100% manual, not automated

Each export overwrites the previous file

It is recommended not to version-control the - `logs/` directory

CSV files may contain sensitive information
---
## 6. Optional Cleanup

Remove the CSV after processing:
```
rm logs/nextdns-export.csv
```
---
🛡️ Keeping raw data separated from analysis improves traceability and OPSEC hygiene.
