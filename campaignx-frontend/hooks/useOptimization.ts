import { useMutation, useQueryClient } from '@tanstack/react-query';
import { optimizationAPI } from '@/lib/api';

/**
 * Hook for optimizing a campaign (surgical optimization)
 */
export function useOptimize() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (campaignId: string) => optimizationAPI.optimize(campaignId),
    onSuccess: (data, campaignId) => {
      // Invalidate campaign and metrics queries to refetch updated data
      queryClient.invalidateQueries({ queryKey: ['campaign', campaignId] });
      queryClient.invalidateQueries({ queryKey: ['metrics', campaignId] });
    },
  });
}

/**
 * Hook for starting autonomous optimization loop
 */
export function useAutonomousLoop() {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: (campaignId: string) => optimizationAPI.autonomousLoop(campaignId),
    onSuccess: (data, campaignId) => {
      // Invalidate all related queries
      queryClient.invalidateQueries({ queryKey: ['campaign', campaignId] });
      queryClient.invalidateQueries({ queryKey: ['metrics', campaignId] });
      queryClient.invalidateQueries({ queryKey: ['optimization', campaignId] });
    },
  });
}

/**
 * Hook to fetch optimization details
 */
export function useOptimizationDetails(campaignId: string) {
  const queryClient = useQueryClient();

  return useMutation({
    mutationFn: () => optimizationAPI.optimize(campaignId),
    onSuccess: (data) => {
      // Update query cache with optimization details
      queryClient.setQueryData(['optimization', campaignId], data);
    },
  });
}
