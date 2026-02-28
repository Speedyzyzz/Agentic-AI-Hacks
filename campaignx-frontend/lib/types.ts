// ============================================
// API RESPONSE TYPES
// ============================================

export interface APIResponse<T = any> {
  success: boolean;
  data: T | null;
  error: string | null;
  message: string | null;
}

// ============================================
// CAMPAIGN TYPES
// ============================================

export interface ParsedBrief {
  product_name: string;
  objective: 'engagement' | 'sales' | 'awareness';
  target_audience: string;
  key_features: string[];
  tone: string;
  kpis?: Record<string, any>;
}

export interface Segment {
  id: string;
  name: string;
  description?: string;
  reasoning: string;
}

export interface Plan {
  segments: Segment[];
  send_time: string;
  send_time_reasoning: string;
  strategy_reasoning: string;
}

export interface Variant {
  id: string;
  variant_id?: string;
  segment_name: string;
  segment?: Segment;
  subject: string;
  subject_line?: string;
  body: string;
  strategy: 'urgency' | 'social_proof' | 'value' | 'scarcity';
  reasoning?: string;
  version_number: number;
  send_time?: string;
  approved?: boolean;
}

export interface Campaign {
  id: string;
  campaign_id?: string;
  product_name: string;
  objective: string;
  target_audience?: string;
  status: 'draft' | 'pending_approval' | 'approved' | 'launched' | 'rejected' | 'optimized';
  created_at: string;
  updated_at: string;
}

export interface CampaignCreateResponse {
  campaign_id: string;
  status: string;
  approval_url: string;
  parsed_brief: ParsedBrief;
  plan: Plan;
  variants: Variant[];
}

// ============================================
// METRICS TYPES
// ============================================

export interface Metrics {
  open_rate: number;
  click_rate: number;
  conversion_rate: number;
  revenue: number;
}

export interface VariantMetric {
  variant_id: string;
  segment_name: string;
  subject: string;
  open_rate: number;
  click_rate: number;
  version_number: number;
  timestamp: string;
}

export interface MetricsSummary {
  avg_open_rate: number;
  avg_click_rate: number;
  total_variants: number;
}

export interface MetricsResponse {
  campaign_id: string;
  metrics_count: number;
  metrics: VariantMetric[];
  summary: MetricsSummary;
  baseline_metrics?: Metrics;
  optimized_metrics?: Metrics;
  logs?: DecisionLog[];
}

// ============================================
// OPTIMIZATION TYPES
// ============================================

export interface OptimizationChange {
  variant_id: string;
  old_version: number;
  new_version: number;
  old_subject: string;
  new_subject: string;
  reasoning: string;
  expected_improvement: string;
}

export interface PreservedVariant {
  variant_id: string;
  reason: string;
}

export interface OptimizationSummary {
  total_variants: number;
  optimized: number;
  preserved: number;
}

export interface OptimizationResponse {
  campaign_id: string;
  optimized: boolean;
  changes: OptimizationChange[];
  preserved: PreservedVariant[];
  summary: OptimizationSummary;
}

// ============================================
// LOGS TYPES
// ============================================

export interface DecisionLog {
  agent: string;
  decision?: string;
  reasoning?: string;
  timestamp: string;
  context?: Record<string, any>;
}

export interface AgentLog {
  id: string;
  agent_name: 'brief_parser' | 'planner' | 'content_generator' | 'analytics' | 'optimizer' | 'api_agent';
  decision: string;
  reasoning: string;
  timestamp: string;
  metadata?: Record<string, any>;
}

export interface LogsResponse {
  campaign_id: string;
  logs: AgentLog[];
  total_logs: number;
}
