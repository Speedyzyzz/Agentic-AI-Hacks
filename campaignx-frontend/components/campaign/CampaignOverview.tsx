import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/Card';
import { Badge } from '@/components/ui/Badge';
import { getStatusColor } from '@/lib/utils';
import type { Campaign } from '@/lib/types';

interface CampaignOverviewProps {
  campaign: Campaign;
}

export function CampaignOverview({ campaign }: CampaignOverviewProps) {
  const statusVariant = getStatusColor(campaign.status) as 'default' | 'success' | 'warning' | 'danger';
  const displayId = campaign.campaign_id || campaign.id;

  return (
    <Card>
      <CardHeader>
        <div className="flex items-center justify-between">
          <CardTitle>Campaign Overview</CardTitle>
          <Badge variant={statusVariant}>{campaign.status}</Badge>
        </div>
      </CardHeader>
      <CardContent className="space-y-4">
        <div>
          <h3 className="text-sm font-medium text-gray-500">Product Name</h3>
          <p className="mt-1 text-base text-gray-900">{campaign.product_name}</p>
        </div>
        
        <div>
          <h3 className="text-sm font-medium text-gray-500">Objective</h3>
          <p className="mt-1 text-base text-gray-900">{campaign.objective}</p>
        </div>

        {campaign.target_audience && (
          <div>
            <h3 className="text-sm font-medium text-gray-500">Target Audience</h3>
            <p className="mt-1 text-base text-gray-900">{campaign.target_audience}</p>
          </div>
        )}

        <div className="grid grid-cols-2 gap-4 pt-4 border-t border-gray-100">
          <div>
            <h3 className="text-sm font-medium text-gray-500">Campaign ID</h3>
            <p className="mt-1 text-sm font-mono text-gray-900">{displayId}</p>
          </div>
          <div>
            <h3 className="text-sm font-medium text-gray-500">Created At</h3>
            <p className="mt-1 text-sm text-gray-900">
              {new Date(campaign.created_at).toLocaleDateString()}
            </p>
          </div>
        </div>
      </CardContent>
    </Card>
  );
}
