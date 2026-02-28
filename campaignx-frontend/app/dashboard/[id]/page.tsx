'use client';

import { useParams, useRouter } from 'next/navigation';
import { useCampaign } from '@/hooks/useCampaign';
import { useMetrics, useLaunchCampaign } from '@/hooks/useMetrics';
import { useOptimize, useAutonomousLoop } from '@/hooks/useOptimization';
import { CampaignOverview } from '@/components/campaign/CampaignOverview';
import { MetricsComparison } from '@/components/campaign/MetricsComparison';
import { LogsPanel } from '@/components/campaign/LogsPanel';
import { Button } from '@/components/ui/Button';
import { Loader } from '@/components/ui/Loader';
import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/Card';

export default function DashboardPage() {
  const params = useParams();
  const router = useRouter();
  const campaignId = params.id as string;

  const { data: campaignData, isLoading: campaignLoading, error: campaignError } = useCampaign(campaignId);
  const { data: metricsData, isLoading: metricsLoading } = useMetrics(campaignId);
  
  const { mutate: launchCampaign, isPending: isLaunching } = useLaunchCampaign();
  const { mutate: optimize, isPending: isOptimizing } = useOptimize();
  const { mutate: startAutonomous, isPending: isStartingLoop } = useAutonomousLoop();

  const handleLaunch = () => {
    launchCampaign(campaignId, {
      onSuccess: (data) => {
        if (!data.success) {
          alert(data.error || 'Failed to launch campaign');
        }
      },
    });
  };

  const handleOptimize = () => {
    optimize(campaignId, {
      onSuccess: (data) => {
        if (!data.success) {
          alert(data.error || 'Failed to optimize campaign');
        }
      },
    });
  };

  const handleAutonomousLoop = () => {
    startAutonomous(campaignId, {
      onSuccess: (data) => {
        if (!data.success) {
          alert(data.error || 'Failed to start autonomous loop');
        }
      },
    });
  };

  if (campaignLoading) {
    return (
      <div className="min-h-screen bg-[#f5f7fb] flex items-center justify-center">
        <div className="text-center">
          <Loader size="lg" />
          <p className="mt-4 text-gray-600">Loading dashboard...</p>
        </div>
      </div>
    );
  }

  if (campaignError || !campaignData?.success || !campaignData.data) {
    return (
      <div className="min-h-screen bg-[#f5f7fb] flex items-center justify-center">
        <Card className="max-w-md">
          <CardContent className="py-12 text-center">
            <p className="text-red-600 font-medium mb-2">Failed to load campaign</p>
            <p className="text-gray-600 text-sm mb-4">
              {campaignError?.message || campaignData?.error || 'Campaign not found'}
            </p>
            <Button variant="primary" onClick={() => router.push('/create')}>
              Back to Create
            </Button>
          </CardContent>
        </Card>
      </div>
    );
  }

  const campaign = campaignData.data;
  const metrics = metricsData?.success ? metricsData.data : null;
  const logs = (metrics as any)?.logs || [];

  const baselineMetrics = (metrics as any)?.baseline_metrics || null;
  const optimizedMetrics = (metrics as any)?.optimized_metrics || null;

  const isActionDisabled = isLaunching || isOptimizing || isStartingLoop;
  const showLaunchButton = campaign.status === 'approved' || campaign.status === 'draft';
  const showOptimizeButtons = campaign.status === 'launched' || campaign.status === 'optimized';

  return (
    <div className="min-h-screen bg-[#f5f7fb] py-12 px-4">
      <div className="max-w-7xl mx-auto">
        <div className="mb-8 flex items-center justify-between">
          <div>
            <h1 className="text-3xl font-semibold text-gray-900 mb-2">
              Campaign Dashboard
            </h1>
            <p className="text-gray-600">
              Monitor performance, optimize variants, and track AI decision logs.
            </p>
          </div>
          <Button
            variant="secondary"
            onClick={() => router.push('/create')}
          >
            New Campaign
          </Button>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
          <div className="lg:col-span-2 space-y-6">
            <CampaignOverview campaign={campaign} />

            {metricsLoading ? (
              <Card>
                <CardContent className="py-12 text-center">
                  <Loader size="md" />
                  <p className="mt-4 text-gray-600">Loading metrics...</p>
                </CardContent>
              </Card>
            ) : (
              <MetricsComparison baseline={baselineMetrics} optimized={optimizedMetrics} />
            )}

            <LogsPanel logs={logs} />
          </div>

          <div className="space-y-6">
            <Card>
              <CardHeader>
                <CardTitle>Actions</CardTitle>
              </CardHeader>
              <CardContent className="space-y-3">
                {showLaunchButton && (
                  <Button
                    variant="primary"
                    className="w-full"
                    onClick={handleLaunch}
                    disabled={isActionDisabled}
                    loading={isLaunching}
                  >
                    Launch Campaign
                  </Button>
                )}

                {showOptimizeButtons && (
                  <>
                    <Button
                      variant="primary"
                      className="w-full"
                      onClick={handleOptimize}
                      disabled={isActionDisabled}
                      loading={isOptimizing}
                    >
                      Optimize Campaign
                    </Button>
                    <Button
                      variant="secondary"
                      className="w-full"
                      onClick={handleAutonomousLoop}
                      disabled={isActionDisabled}
                      loading={isStartingLoop}
                    >
                      Start Autonomous Loop
                    </Button>
                  </>
                )}

                <div className="pt-4 border-t border-gray-100">
                  <p className="text-xs text-gray-500 leading-relaxed">
                    {showLaunchButton && 'Launch the campaign to start tracking metrics.'}
                    {showOptimizeButtons && 'Run optimization to improve performance based on current metrics.'}
                  </p>
                </div>
              </CardContent>
            </Card>

            <Card>
              <CardHeader>
                <CardTitle>Campaign Status</CardTitle>
              </CardHeader>
              <CardContent className="space-y-4">
                <div>
                  <h4 className="text-sm font-medium text-gray-700 mb-1">Current Status</h4>
                  <p className="text-lg font-semibold text-gray-900 capitalize">
                    {campaign.status}
                  </p>
                </div>
                <div>
                  <h4 className="text-sm font-medium text-gray-700 mb-1">Campaign ID</h4>
                  <p className="text-xs font-mono text-gray-600 break-all">
                    {campaign.campaign_id || campaign.id}
                  </p>
                </div>
                <div>
                  <h4 className="text-sm font-medium text-gray-700 mb-1">Created</h4>
                  <p className="text-sm text-gray-600">
                    {new Date(campaign.created_at).toLocaleDateString('en-US', {
                      year: 'numeric',
                      month: 'long',
                      day: 'numeric',
                    })}
                  </p>
                </div>
              </CardContent>
            </Card>

            {metrics && (
              <Card>
                <CardHeader>
                  <CardTitle>Quick Stats</CardTitle>
                </CardHeader>
                <CardContent className="space-y-3">
                  {optimizedMetrics && (
                    <>
                      <div className="flex justify-between items-center">
                        <span className="text-sm text-gray-600">Open Rate</span>
                        <span className="text-sm font-medium text-gray-900">
                          {(optimizedMetrics.open_rate * 100).toFixed(2)}%
                        </span>
                      </div>
                      <div className="flex justify-between items-center">
                        <span className="text-sm text-gray-600">Click Rate</span>
                        <span className="text-sm font-medium text-gray-900">
                          {(optimizedMetrics.click_rate * 100).toFixed(2)}%
                        </span>
                      </div>
                      <div className="flex justify-between items-center">
                        <span className="text-sm text-gray-600">Conversion Rate</span>
                        <span className="text-sm font-medium text-gray-900">
                          {(optimizedMetrics.conversion_rate * 100).toFixed(2)}%
                        </span>
                      </div>
                      <div className="flex justify-between items-center pt-3 border-t border-gray-100">
                        <span className="text-sm font-medium text-gray-700">Total Revenue</span>
                        <span className="text-base font-semibold text-gray-900">
                          ${optimizedMetrics.revenue.toLocaleString()}
                        </span>
                      </div>
                    </>
                  )}
                </CardContent>
              </Card>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}
