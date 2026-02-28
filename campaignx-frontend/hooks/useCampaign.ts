import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { campaignAPI } from '@/lib/api';
import type { Campaign, CampaignCreateResponse, Variant } from '@/lib/types';

export function useCampaignCreate() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (brief: string) => campaignAPI.create(brief),
    onSuccess: (data) => {
      if (data.success && data.data) {
        queryClient.setQueryData(['campaign', data.data.campaign_id], data.data);
      }
    },
  });
}

export function useCampaign(campaignId: string | undefined) {
  return useQuery({
    queryKey: ['campaign', campaignId],
    queryFn: () => {
      if (!campaignId) throw new Error('Campaign ID is required');
      return campaignAPI.get(campaignId);
    },
    enabled: !!campaignId,
    retry: 1,
  });
}

export function useCampaignVariants(campaignId: string | undefined) {
  return useQuery({
    queryKey: ['campaign-variants', campaignId],
    queryFn: () => {
      if (!campaignId) throw new Error('Campaign ID is required');
      return campaignAPI.getVariants(campaignId);
    },
    enabled: !!campaignId,
    retry: 1,
  });
}

export function useCampaignApprove() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (campaignId: string) => campaignAPI.approve(campaignId),
    onSuccess: (data, campaignId) => {
      queryClient.invalidateQueries({ queryKey: ['campaign', campaignId] });
      queryClient.invalidateQueries({ queryKey: ['campaign-variants', campaignId] });
    },
  });
}

export function useCampaignReject() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (campaignId: string) => campaignAPI.reject(campaignId),
    onSuccess: (data, campaignId) => {
      queryClient.invalidateQueries({ queryKey: ['campaign', campaignId] });
    },
  });
}
