# 🚀 QUICK COMMAND REFERENCE

## Initial Setup (ONE TIME ONLY)

```bash
# 1. Register and get API key
cd backend
python3 signup.py
# Follow prompts - API key saved to .env automatically
```

## Testing

```bash
# Test API integration
python3 test_api_real.py

# Quick verification
python3 -c "from agents.api_agent import APIAgent; agent = APIAgent(); print(f'✅ {len(agent.discover_endpoints())} endpoints discovered')"
```

## Using in Code

```python
from agents.api_agent import APIAgent

agent = APIAgent()

# 1. Get customer cohort (required before every send)
cohort = agent.get_customer_cohort()
customer_ids = [c['customer_id'] for c in cohort['data'][:100]]

# 2. Generate future send time
send_time = agent.generate_future_send_time(minutes=10)

# 3. Send campaign
response = agent.send_campaign(
    subject="Special Offer 🎉",
    body="Visit https://example.com for amazing deals!",
    customer_ids=customer_ids,
    send_time=send_time
)

campaign_id = response['campaign_id']
print(f"Campaign sent: {campaign_id}")

# 4. Wait for delivery (5-10 minutes)
import time
time.sleep(600)

# 5. Get performance report
report = agent.get_report(campaign_id)
metrics = agent.compute_metrics(report)

print(f"Opens: {metrics['opens']} ({metrics['open_rate']:.1%})")
print(f"Clicks: {metrics['clicks']} ({metrics['click_rate']:.1%})")
```

## Troubleshooting

```bash
# Check if API key is set
cat .env | grep CAMPAIGNX_API_KEY

# View discovered endpoints
python3 -c "from agents.api_agent import APIAgent; agent = APIAgent(); print('\n'.join(agent.discover_endpoints()))"

# Check OpenAPI spec
head -n 10 openapi.json
```

## Rate Limit Tracking

- **Limit:** 100 calls per day
- **Endpoints that count:** get_customer_cohort, send_campaign, get_report
- **Does NOT count:** signup (one-time only)

## Important Reminders

1. ✅ Call `get_customer_cohort()` before EVERY send
2. ✅ Use `generate_future_send_time()` for proper format
3. ✅ Max 5000 customer IDs per campaign
4. ❌ Never commit .env to git
5. ⚠️  API key shown only once during signup

## Demo Commands

```bash
# Show OpenAPI spec integration
cat openapi.json | head -n 20

# Show endpoint discovery
python3 -c "from agents.api_agent import APIAgent; agent = APIAgent(); [print(f'  {ep}') for ep in agent.discover_endpoints()]"

# Test cohort fetch (uses 1 API call)
python3 -c "from agents.api_agent import APIAgent; agent = APIAgent(); cohort = agent.get_customer_cohort(); print(f'✅ Fetched {cohort.get(\"total_count\", 0)} customers')"
```

---

**Quick Start:** `python3 signup.py` → `python3 test_api_real.py` → Start coding!
