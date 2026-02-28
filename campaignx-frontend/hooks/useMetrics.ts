import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { metricsAPI, launchAPI } from '@/lib/api';

export function useMetricsFetch(campaignId: string | undefined) {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: () => {
      if (!campaignId) throw new Error('Campaign ID is required');
      return metricsAPI.fetch(campaignId);
    },
    onSuccess: (data) => {
      if (campaignId) {
        queryClient.setQueryData(['metrics', campaignId], data);
      }
    },
  });
}

export function useMetrics(campaignId: string | undefined) {
  return useQuery({
    queryKey: ['metrics', campaignId],
    queryFn: () => {
      if (!campaignId) throw new Error('Campaign ID is required');
      return metricsAPI.fetch(campaignId);
    },
    enabled: false, // Only fetch when explicitly triggered
    retry: 1,
  });
}

export function useLaunchCampaign() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (campaignId: string) => launchAPI.launch(campaignId),
    onSuccess: (data, campaignId) => {
      queryClient.invalidateQueries({ queryKey: ['campaign', campaignId] });
    },
  });
}
