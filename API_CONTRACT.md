# 📋 CAMPAIGNX API CONTRACT - LOCKED & STANDARDIZED

**Last Updated:** February 28, 2026  
**Status:** 🔒 LOCKED - Do NOT change without updating this doc

---

## 🎯 RESPONSE FORMAT (ALL ENDPOINTS)

### Success Response
```json
{
  "success": true,
  "data": { /* payload */ },
  "error": null,
  "message": "Optional success message"
}
```

### Error Response
```json
{
  "success": false,
  "data": null,
  "error": "Error description",
  "message": null
}
```

---

## 📡 ENDPOINT SPECIFICATIONS

### 1. POST `/create-campaign`

**Purpose:** Create campaign from natural language brief

**Request:**
```json
{
  "brief": "string - natural language campaign description"
}
```

**Success Response:**
```json
{
  "success": true,
  "data": {
    "campaign_id": "uuid-string",
    "status": "pending_approval",
    "approval_url": "http://127.0.0.1:8000/approval/{id}",
    "parsed_brief": {
      "product_name": "string",
      "objective": "engagement|sales|awareness",
      "target_audience": "string",
      "key_features": ["string"],
      "tone": "string"
    },
    "plan": {
      "segments": [
        {
          "id": "uuid",
          "name": "string",
          "reasoning": "string"
        }
      ],
      "send_time": "6PM|10AM|2PM",
      "send_time_reasoning": "string",
      "strategy_reasoning": "string"
    },
    "variants": [
      {
        "id": "uuid",
        "segment_name": "string",
        "subject": "string",
        "body": "string (first 100 chars)",
        "strategy": "urgency|social_proof|value|scarcity",
        "version_number": 1
      }
    ]
  },
  "error": null,
  "message": "Campaign created - awaiting approval"
}
```

**Error Response:**
```json
{
  "success": false,
  "data": null,
  "error": "Failed to parse brief | Plan validation failed | {exception}",
  "message": null
}
```

---

### 2. GET `/api/campaigns/{campaign_id}`

**Purpose:** Get campaign details

**Success Response:**
```json
{
  "success": true,
  "data": {
    "id": "uuid",
    "product_name": "string",
    "objective": "string",
    "status": "draft|pending_approval|approved|launched|rejected",
    "created_at": "ISO8601 timestamp",
    "updated_at": "ISO8601 timestamp"
  },
  "error": null,
  "message": null
}
```

**Error Response:**
```json
{
  "success": false,
  "data": null,
  "error": "Campaign not found",
  "message": null
}
```

---

### 3. GET `/api/campaigns/{campaign_id}/variants`

**Purpose:** Get all variants for a campaign

**Success Response:**
```json
{
  "success": true,
  "data": {
    "campaign_id": "uuid",
    "variants": [
      {
        "id": "uuid",
        "segment_name": "string",
        "subject": "string",
        "body": "string (full text)",
        "send_time": "6PM",
        "version_number": 1,
        "approved": false
      }
    ]
  },
  "error": null,
  "message": null
}
```

---

### 4. POST `/api/campaigns/{campaign_id}/approve`

**Purpose:** Approve campaign and re-fetch customer cohort

**Success Response:**
```json
{
  "success": true,
  "data": {
    "campaign_id": "uuid",
    "status": "approved",
    "cohort_refetched": true,
    "segments_updated": ["segment1", "segment2"],
    "next_action": "Visit dashboard to fetch metrics"
  },
  "error": null,
  "message": "Campaign approved and cohort refreshed"
}
```

---

### 5. POST `/api/campaigns/{campaign_id}/reject`

**Purpose:** Reject campaign

**Success Response:**
```json
{
  "success": true,
  "data": {
    "campaign_id": "uuid",
    "status": "rejected"
  },
  "error": null,
  "message": "Campaign rejected"
}
```

---

### 6. POST `/fetch-metrics/{campaign_id}`

**Purpose:** Fetch performance metrics (deterministic calculation)

**Success Response:**
```json
{
  "success": true,
  "data": {
    "campaign_id": "uuid",
    "metrics_count": 4,
    "metrics": [
      {
        "variant_id": "uuid",
        "segment_name": "string",
        "subject": "string",
        "open_rate": 0.28,
        "click_rate": 0.09,
        "version_number": 1,
        "timestamp": "ISO8601"
      }
    ],
    "summary": {
      "avg_open_rate": 0.27,
      "avg_click_rate": 0.085,
      "total_variants": 4
    }
  },
  "error": null,
  "message": "Metrics fetched successfully"
}
```

---

### 7. POST `/optimize/{campaign_id}`

**Purpose:** Run surgical optimization on underperforming variants

**Success Response:**
```json
{
  "success": true,
  "data": {
    "campaign_id": "uuid",
    "optimized": true,
    "changes": [
      {
        "variant_id": "uuid",
        "old_version": 1,
        "new_version": 2,
        "old_subject": "string",
        "new_subject": "string",
        "reasoning": "Low CTR detected - added urgency",
        "expected_improvement": "80%+ CTR increase"
      }
    ],
    "preserved": [
      {
        "variant_id": "uuid",
        "reason": "Already performing above baseline"
      }
    ],
    "summary": {
      "total_variants": 4,
      "optimized": 2,
      "preserved": 2
    }
  },
  "error": null,
  "message": "Optimization complete"
}
```

---

### 8. POST `/autonomous-loop/{campaign_id}`

**Purpose:** Run full autonomous optimization loop

**Success Response:**
```json
{
  "success": true,
  "data": {
    "campaign_id": "uuid",
    "loop_completed": true,
    "steps": {
      "metrics_fetched": true,
      "analysis_complete": true,
      "optimization_applied": true
    },
    "metrics_before": {
      "avg_ctr": 0.05
    },
    "metrics_after": {
      "avg_ctr": 0.09
    },
    "improvement": "80% CTR increase",
    "can_run_again": true
  },
  "error": null,
  "message": "Autonomous loop completed successfully"
}
```

---

### 9. GET `/api/campaigns/{campaign_id}/logs`

**Purpose:** Get agent decision logs for transparency

**Success Response:**
```json
{
  "success": true,
  "data": {
    "campaign_id": "uuid",
    "logs": [
      {
        "id": "uuid",
        "agent_name": "brief_parser|planner|content_generator|analytics|optimizer|api_agent",
        "decision": "string - what was decided",
        "reasoning": "string - why it was decided",
        "timestamp": "ISO8601",
        "metadata": { /* additional context */ }
      }
    ],
    "total_logs": 12
  },
  "error": null,
  "message": null
}
```

---

## 🔥 CRITICAL RULES FOR LOVABLE INTEGRATION

### 1. **Always Check `success` First**
```javascript
const response = await axios.post('/create-campaign', data);
if (!response.data.success) {
  // Handle error
  alert(response.data.error);
  return;
}
// Use response.data.data
const campaign = response.data.data;
```

### 2. **Never Hardcode Campaign IDs**
```javascript
// ❌ WRONG
const campaignId = "abc123";

// ✅ CORRECT
const campaignId = response.data.data.campaign_id;
```

### 3. **Always Pass Campaign ID Dynamically**
```javascript
// ❌ WRONG
await axios.post('/optimize/hardcoded-id');

// ✅ CORRECT
await axios.post(`/optimize/${campaignId}`);
```

### 4. **Handle Both Success and Error States**
```javascript
try {
  const res = await axios.post(url, data);
  if (res.data.success) {
    // Success path
  } else {
    // Error from backend
    console.error(res.data.error);
  }
} catch (err) {
  // Network/HTTP error
  console.error(err);
}
```

---

## 🎬 DEMO FLOW CHECKLIST

### Frontend MUST Support:
- [x] 1. Input natural language brief
- [x] 2. Call `/create-campaign` with brief
- [x] 3. Display `campaign_id` dynamically
- [x] 4. Show generated segments & variants
- [x] 5. Redirect to approval page (use `approval_url` from response)
- [x] 6. Call `/api/campaigns/{id}/approve` on approval
- [x] 7. Navigate to dashboard
- [x] 8. Call `/fetch-metrics/{id}` to get performance
- [x] 9. Display metrics (open rate, CTR)
- [x] 10. Button to call `/optimize/{id}`
- [x] 11. Display optimization changes
- [x] 12. Show before/after improvement percentage
- [x] 13. Call `/api/campaigns/{id}/logs` to show agent decisions

---

## 🚨 WHAT LOVABLE MUST NOT DO

❌ Mock data in frontend  
❌ Hardcode campaign IDs  
❌ Assume local JSON files  
❌ Skip `success` check  
❌ Auto-approve campaigns  
❌ Hide any workflow step  
❌ Generate fake metrics  
❌ Ignore `campaign_id` from response  

---

## ✅ VALIDATION CHECKLIST

Before deploying frontend:
- [ ] All API calls use `axios` or `fetch`
- [ ] All responses check `.success` field
- [ ] Campaign ID passed dynamically in all endpoints
- [ ] Error states handled and displayed
- [ ] No mock data in production code
- [ ] All 13 demo steps functional
- [ ] Agent logs displayed for transparency

---

**Contract Status:** 🔒 LOCKED  
**Next Step:** Update `backend/main.py` to match this contract  
**After That:** Build Lovable frontend against this contract
