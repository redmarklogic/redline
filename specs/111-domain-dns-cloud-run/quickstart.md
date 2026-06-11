# Quickstart: Verify api.redmarklogic.com

Fast checks once implementation lands (full procedure: plan.md Phased Delivery;
durable runbook: `docs/infrastructure/domain-dns-runbook.md` after Phase 3).

```powershell
# 1. DNS resolves with Firebase values, grey cloud
Resolve-DnsName api.redmarklogic.com -Type A
Resolve-DnsName api.redmarklogic.com -Type TXT

# 2. Certificate active (Google Trust Services, correct host)
# (openssl via Git for Windows, or use a browser padlock)
openssl s_client -connect api.redmarklogic.com:443 -servername api.redmarklogic.com | Select-String "subject="

# 3. Backend answers on the branded address (confirm health path: /health vs /healthz)
curl.exe -sSi https://api.redmarklogic.com/health

# 4. Email unharmed: zone diff is additive-only (token from Secret Manager)
curl.exe -s "https://api.cloudflare.com/client/v4/zones/$env:CF_ZONE_ID/dns_records/export" -H "Authorization: Bearer $env:CF_API_TOKEN" > zone-post.txt
rtk git diff --no-index docs/infrastructure/zone-snapshot-pre-2026-06-11.txt zone-post.txt

# 5. Accepted limits (negative checks)
#    >60 s request -> HTTP 504 (proxy ceiling); direct run.app URL still answers (expected)
```
