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
    const response = await axiosInstance.get(`/campaigns/${campaignId}`);
    return response.data;
  },

  /**
   * Get all variants for a campaign
   */
  getVariants: async (campaignId: string): Promise<APIResponse<{ campaign_id: string; variants: Variant[] }>> => {
    const response = await axiosInstance.get(`/campaigns/${campaignId}/variants`);
    return response.data;
  },

  /**
   * Approve campaign
   */
  approve: async (campaignId: string): Promise<APIResponse<any>> => {
    const response = await axiosInstance.post(`/campaigns/${campaignId}/approve`);
    return response.data;
  },

  /**
   * Reject campaign
   */
  reject: async (campaignId: string): Promise<APIResponse<any>> => {
    const response = await axiosInstance.post(`/campaigns/${campaignId}/reject`);
    return response.data;
  },
};

// ============================================
// METRICS API
// ============================================

export const metricsAPI = {
  /**
   * Fetch metrics for a campaign
   */
  fetch: async (campaignId: string): Promise<APIResponse<MetricsResponse>> => {
    const response = await axiosInstance.post(`/fetch-metrics/${campaignId}`);
    return response.data;
  },

  /**
   * Get metrics for a campaign
   */
  get: async (campaignId: string): Promise<APIResponse<MetricsResponse>> => {
    const response = await axiosInstance.get(`/campaigns/${campaignId}/metrics`);
    return response.data;
  },
};

// ============================================
// OPTIMIZATION API
// ============================================

export const optimizationAPI = {
  /**
   * Optimize a campaign
   */
  optimize: async (campaignId: string): Promise<APIResponse<OptimizationResponse>> => {
    const response = await axiosInstance.post(`/optimize/${campaignId}`);
    return response.data;
  },

  /**
   * Start autonomous optimization loop
   */
  autonomousLoop: async (campaignId: string): Promise<APIResponse<any>> => {
    const response = await axiosInstance.post(`/full-optimization-loop/${campaignId}`);
    return response.data;
  },
};

// ============================================
// LOGS API
// ============================================

export const logsAPI = {
  /**
   * Get decision logs for a campaign
   */
  get: async (campaignId: string): Promise<APIResponse<LogsResponse>> => {
    const response = await axiosInstance.get(`/campaigns/${campaignId}/logs`);
    return response.data;
  },
};

// ============================================
// LAUNCH API
// ============================================

export const launchAPI = {
  /**
   * Launch a campaign
   */
  launch: async (campaignId: string): Promise<APIResponse<any>> => {
    const response = await axiosInstance.post(`/launch-campaign/${campaignId}`);
    return response.data;
  },
};
