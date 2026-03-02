# 🚀 REAL API QUICK START

## 1️⃣ Get Your API Key (ONE TIME ONLY)

```bash
cd backend
python3 signup.py
```

Follow prompts. API key automatically saved to `.env`.

## 2️⃣ Test Integration

```bash
python3 test_api_real.py
```

Should see 4/4 tests pass.

## 3️⃣ Use in Code

```python
from agents.api_agent import APIAgent

agent = APIAgent()

# Get customers (required before every send)
cohort = agent.get_customer_cohort()
customer_ids = [c['customer_id'] for c in cohort['data'][:100]]

# Send campaign
send_time = agent.generate_future_send_time(minutes=10)
response = agent.send_campaign(
    subject="Test Campaign 🎉",
    body="Visit https://example.com",
    customer_ids=customer_ids,
    send_time=send_time
)

campaign_id = response['campaign_id']

# Wait for campaign to send (5-10 minutes)
import time
time.sleep(600)

# Get real metrics
report = agent.get_report(campaign_id)
metrics = agent.compute_metrics(report)

print(f"Opens: {metrics['opens']} ({metrics['open_rate']:.1%})")
print(f"Clicks: {metrics['clicks']} ({metrics['click_rate']:.1%})")
```

## ⚠️ CRITICAL RULES

1. **Rate Limit:** 100 calls/day
2. **Fresh Cohort:** Call `get_customer_cohort()` before EVERY send
3. **Send Time:** Use `generate_future_send_time()` helper
4. **Customer IDs:** Must be from cohort (max 5000)
5. **API Key:** Never commit to git (already in .gitignore)

## 📊 API Endpoints

| Endpoint | Method | Purpose | Rate Limit |
|----------|--------|---------|------------|
| `/api/v1/signup` | POST | Get API key (once) | - |
| `/api/v1/get_customer_cohort` | GET | Fetch 5000 customers | 100/day |
| `/api/v1/send_campaign` | POST | Send campaign | 100/day |
| `/api/v1/get_report` | GET | Get performance | 100/day |

## 🔗 More Info

See `REAL_API_INTEGRATION.md` for complete documentation.

---

**Status:** ✅ Production-ready  
**Mock Data:** ❌ DELETED  
**Real API:** ✅ ACTIVE
