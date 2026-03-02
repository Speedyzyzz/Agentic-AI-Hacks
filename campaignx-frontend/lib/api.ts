import axiosInstance from './axios';
import type {
  APIResponse,
  Campaign,
  CampaignCreateResponse,
  Variant,
  MetricsResponse,
  OptimizationResponse,
  LogsResponse,
} from './types';

// ============================================
// CAMPAIGN API
// ============================================

export const campaignAPI = {
  /**
   * Create a new campaign from natural language brief
   */
  create: async (brief: string): Promise<APIResponse<CampaignCreateResponse>> => {
    const response = await axiosInstance.post('/create-campaign', { brief });
    return response.data;
  },

  /**
   * Get campaign details
   */
  get: async (campaignId: string): Promise<APIResponse<Campaign>> => {
    const response = await axiosInstance.get(`/api/campaigns/${campaignId}`);
    return response.data;
  },

  /**
   * Get all variants for a campaign
   */
  getVariants: async (campaignId: string): Promise<APIResponse<{ campaign_id: string; variants: Variant[] }>> => {
    const response = await axiosInstance.get(`/api/campaigns/${campaignId}/variants`);
    return response.data;
  },

  /**
   * Approve campaign (re-fetches fresh cohort)
   */
  approve: async (campaignId: string): Promise<APIResponse<any>> => {
    const response = await axiosInstance.post(`/api/campaigns/${campaignId}/approve`);
    return response.data;
  },

  /**
   * Reject campaign
   */
  reject: async (campaignId: string): Promise<APIResponse<any>> => {
    const response = await axiosInstance.post(`/api/campaigns/${campaignId}/reject`);
    return response.data;
  },
};

// ============================================
// METRICS API
// ============================================

export const metricsAPI = {
  /**
   * Fetch performance metrics for a campaign
   */
  fetch: async (campaignId: string): Promise<APIResponse<MetricsResponse>> => {
    const response = await axiosInstance.post(`/fetch-metrics/${campaignId}`);
    return response.data;
  },
};

// ============================================
// OPTIMIZATION API
// ============================================

export const optimizationAPI = {
  /**
   * Run surgical optimization on campaign
   */
  optimize: async (campaignId: string): Promise<APIResponse<OptimizationResponse>> => {
    const response = await axiosInstance.post(`/optimize/${campaignId}`);
    return response.data;
  },

  /**
   * Run full autonomous optimization loop
   */
  autonomousLoop: async (campaignId: string): Promise<APIResponse<any>> => {
    const response = await axiosInstance.post(`/autonomous-loop/${campaignId}`);
    return response.data;
  },
};

// ============================================
// LOGS API
// ============================================

export const logsAPI = {
  /**
   * Get agent decision logs for transparency
   */
  get: async (campaignId: string): Promise<APIResponse<LogsResponse>> => {
    const response = await axiosInstance.get(`/api/campaigns/${campaignId}/logs`);
    return response.data;
  },
};

// ============================================
// LAUNCH API
// ============================================

export const launchAPI = {
  /**
   * Launch approved campaign
   */
  launch: async (campaignId: string): Promise<APIResponse<any>> => {
    const response = await axiosInstance.post(`/launch/${campaignId}`);
    return response.data;
  },
};
