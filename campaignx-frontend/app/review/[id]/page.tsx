'use client';

import { useParams, useRouter } from 'next/navigation';
import { useCampaign, useCampaignVariants, useCampaignApprove, useCampaignReject } from '@/hooks/useCampaign';
import { CampaignOverview } from '@/components/campaign/CampaignOverview';
import { VariantCard } from '@/components/campaign/VariantCard';
import { Button } from '@/components/ui/Button';
import { Loader } from '@/components/ui/Loader';
import { Card, CardContent } from '@/components/ui/Card';

export default function ReviewCampaignPage() {
  const params = useParams();
  const router = useRouter();
  const campaignId = params.id as string;

  const { data: campaignData, isLoading: campaignLoading, error: campaignError } = useCampaign(campaignId);
  const { data: variantsData, isLoading: variantsLoading } = useCampaignVariants(campaignId);
  
  const { mutate: approveCampaign, isPending: isApproving } = useCampaignApprove();
  const { mutate: rejectCampaign, isPending: isRejecting } = useCampaignReject();

  const handleApprove = () => {
    approveCampaign(campaignId, {
      onSuccess: (data) => {
        if (data.success) {
          router.push(`/dashboard/${campaignId}`);
        }
      },
    });
  };

  const handleReject = () => {
    rejectCampaign(campaignId, {
      onSuccess: (data) => {
        if (data.success) {
          router.push('/create');
        }
      },
    });
  };

  if (campaignLoading || variantsLoading) {
    return (
      <div className="min-h-screen bg-[#f5f7fb] flex items-center justify-center">
        <div className="text-center">
          <Loader size="lg" />
          <p className="mt-4 text-gray-600">Loading campaign details...</p>
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
  const variantsArray = variantsData?.success && Array.isArray(variantsData.data) 
    ? variantsData.data 
    : variantsData?.success && variantsData.data && typeof variantsData.data === 'object' && 'variants' in variantsData.data
    ? (variantsData.data as any).variants 
    : [];
  const isActionDisabled = isApproving || isRejecting;

  return (
    <div className="min-h-screen bg-[#f5f7fb] py-12 px-4">
      <div className="max-w-6xl mx-auto">
        <div className="mb-8">
          <h1 className="text-3xl font-semibold text-gray-900 mb-2">
            Review Campaign
          </h1>
          <p className="text-gray-600">
            Review the AI-generated email variants and approve or reject the campaign.
          </p>
        </div>

        <div className="space-y-6">
          <CampaignOverview campaign={campaign} />

          {variantsArray.length > 0 ? (
            <>
              <div>
                <h2 className="text-xl font-semibold text-gray-900 mb-4">
                  Email Variants ({variantsArray.length})
                </h2>
                <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                  {variantsArray.map((variant: any, index: number) => (
                    <VariantCard key={variant.variant_id || variant.id || index} variant={variant} index={index} />
                  ))}
                </div>
              </div>

              <Card>
                <CardContent className="py-6">
                  <div className="flex items-center justify-between">
                    <div>
                      <h3 className="text-lg font-medium text-gray-900 mb-1">
                        Ready to proceed?
                      </h3>
                      <p className="text-sm text-gray-600">
                        Approve to launch the campaign or reject to start over
                      </p>
                    </div>
                    <div className="flex items-center gap-3">
                      <Button
                        variant="secondary"
                        size="lg"
                        onClick={handleReject}
                        disabled={isActionDisabled}
                        loading={isRejecting}
                      >
                        Reject
                      </Button>
                      <Button
                        variant="primary"
                        size="lg"
                        onClick={handleApprove}
                        disabled={isActionDisabled}
                        loading={isApproving}
                      >
                        Approve & Continue
                      </Button>
                    </div>
                  </div>
                </CardContent>
              </Card>
            </>
          ) : (
            <Card>
              <CardContent className="py-12 text-center">
                <Loader size="md" />
                <p className="mt-4 text-gray-600">
                  AI agents are generating email variants...
                </p>
              </CardContent>
            </Card>
          )}
        </div>
      </div>
    </div>
  );
}
