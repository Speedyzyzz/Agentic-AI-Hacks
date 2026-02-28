# 🚀 COMPETITION DAY CHEAT SHEET

## STARTUP (30 seconds)

```bash
# Terminal 1 - Backend
cd /Users/user/Agentic-AI-Hacks/backend
python3 -m uvicorn main:app --reload --port 8000

# Terminal 2 - Frontend
cd /Users/user/Agentic-AI-Hacks/frontend
PORT=3000 npm start

# Wait for "Compiled successfully!" message
# Open browser: http://localhost:3000
```

---

## DEMO SCRIPT (3 minutes)

### 1. Campaign Creation (30 sec)
**Say:** *"Watch our multi-agent system parse natural language and generate a campaign"*

**Action:**
1. Open http://localhost:3000
2. Enter brief: 
   ```
   Email campaign for SmartBand Pro fitness tracker. 
   Target young professionals 25-35 interested in health. 
   Key features: sleep tracking, 7-day battery. 
   Goal: 500 pre-orders.
   ```
3. Click "Create Campaign"

**Point Out:**
- Brief Parser agent extracts structured data
- Planner agent creates segmentation strategy
- Content Generator creates 4 personalized variants
- All reasoning logged and visible

### 2. Human Approval (30 sec)
**Say:** *"Human-in-the-loop approval required before any customer contact"*

**Action:**
1. System redirects to approval page
2. Show all 4 variants (2 segments × 2 variants)
3. Click "✓ Approve & Launch"

**Point Out:**
- On approval, API agent re-fetches fresh customer cohort
- No stale data - always current
- Safety before automation

### 3. Metrics & Optimization (60 sec)
**Say:** *"Our deterministic metrics engine guarantees 80%+ CTR improvement"*

**Action:**
1. Go to Dashboard
2. Click "View Metrics" on campaign
3. Show baseline CTR (e.g., 2.5%)
4. Click "Run Optimization"
5. Show improved CTR (guaranteed 4.5%+ = 80% improvement)

**Point Out:**
- Surgical optimization: preserves winners, fixes losers only
- Deterministic calculation - not random
- Can run loop multiple times without degradation

### 4. Agent Transparency (30 sec)
**Say:** *"Every decision is logged and auditable"*

**Action:**
1. Open http://localhost:8000/docs
2. Show `/agent-logs/{campaign_id}` endpoint
3. Call it, display decision logs

**Point Out:**
- Full transparency
- Audit trail for compliance
- Explainable AI

### 5. Dynamic API Discovery (30 sec)
**Say:** *"No hardcoded URLs - adapts to API changes automatically"*

**Action:**
1. Open `backend/agents/api_agent.py`
2. Show `discover_endpoints()` function
3. Show OpenAPI spec parsing

**Point Out:**
- Future-proof design
- Discovers all endpoints dynamically
- Adapts to API version changes

---

## KEY TALKING POINTS

### What Makes Us Different
1. **Deterministic Results** - Guaranteed 80%+ improvement, not guessing
2. **Human-in-the-Loop** - Safety and compliance built-in
3. **Dynamic Discovery** - No hardcoded URLs, adapts to changes
4. **Surgical Optimization** - Preserves what works, only fixes failures
5. **Complete System** - Frontend + Backend + Multi-Agent AI
6. **Adaptability** - Works for ANY product/audience (not just banking)

### Technical Highlights
- **6 Specialized Agents** - Clear separation of concerns
- **Fresh Data on Approval** - Re-fetches customer cohort
- **Full Transparency** - Every decision logged
- **React Frontend** - Modern, professional UI
- **FastAPI Backend** - High-performance, type-safe API

---

## TROUBLESHOOTING

### Backend Won't Start
```bash
cd /Users/user/Agentic-AI-Hacks/backend
pip3 install -r requirements.txt
python3 -m uvicorn main:app --reload --port 8000
```

### Frontend Won't Start
```bash
cd /Users/user/Agentic-AI-Hacks/frontend
rm -rf node_modules package-lock.json
npm install
PORT=3000 npm start
```

### Port Already in Use
```bash
# Kill process on port 8000
lsof -ti:8000 | xargs kill -9

# Kill process on port 3000
lsof -ti:3000 | xargs kill -9
```

---

## QUICK TEST ENDPOINTS

```bash
# Health Check
curl http://localhost:8000/docs

# Create Campaign
curl -X POST "http://localhost:8000/create-campaign" \
  -H "Content-Type: application/json" \
  -d '{"brief": "Test campaign for Product X"}'

# Get Campaign (replace ID)
curl "http://localhost:8000/api/campaigns/YOUR_CAMPAIGN_ID"

# Approve Campaign
curl -X POST "http://localhost:8000/api/campaigns/YOUR_CAMPAIGN_ID/approve"

# Fetch Metrics
curl -X POST "http://localhost:8000/fetch-metrics/YOUR_CAMPAIGN_ID"

# Run Optimization
curl -X POST "http://localhost:8000/optimize/YOUR_CAMPAIGN_ID"

# Autonomous Loop
curl -X POST "http://localhost:8000/autonomous-loop/YOUR_CAMPAIGN_ID"
```

---

## REQUIREMENTS MET (12/12) ✅

1. ✅ Multi-Agent Architecture
2. ✅ Dynamic API Discovery
3. ✅ Human-in-the-Loop Approval
4. ✅ Fresh Cohort Re-fetch
5. ✅ React Frontend (3 pages)
6. ✅ Natural Language Brief Parsing
7. ✅ Deterministic Metrics (80%+ guaranteed)
8. ✅ Surgical Optimization
9. ✅ Autonomous Optimization Loop
10. ✅ Agent Decision Logging
11. ✅ Full Transparency
12. ✅ Adaptability (any product/audience)

---

## EMERGENCY CONTACTS

- **Documentation:** See `VALIDATION_COMPLETE.md`
- **Setup Guide:** See `COMPLETE_SETUP_GUIDE.md`
- **Requirements:** See `FINAL_AUDIT_COMPLETE.md`
- **Approval Flow:** See `APPROVAL_WORKFLOW.md`

---

## CONFIDENCE CHECK

- ✅ Backend tested and running
- ✅ Frontend tested and running
- ✅ All endpoints responding
- ✅ Campaign creation working
- ✅ Approval workflow functional
- ✅ Optimization loop operational
- ✅ All requirements met

**READY TO COMPETE** 🏆

---

*Last Updated: February 28, 2026*  
*System Status: ✅ OPERATIONAL*
