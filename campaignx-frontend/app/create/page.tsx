'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';
import { useCampaignCreate } from '@/hooks/useCampaign';
import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/Card';
import { Button } from '@/components/ui/Button';
import { Loader } from '@/components/ui/Loader';

export default function CreateCampaignPage() {
  const router = useRouter();
  const [brief, setBrief] = useState('');
  const [error, setError] = useState<string | null>(null);

  const { mutate: createCampaign, isPending } = useCampaignCreate();

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);

    // Validation
    if (!brief.trim()) {
      setError('Please enter a campaign brief');
      return;
    }

    if (brief.trim().length < 20) {
      setError('Campaign brief must be at least 20 characters long');
      return;
    }

    createCampaign(brief, {
      onSuccess: (data) => {
        if (data.success && data.data?.campaign_id) {
          router.push(`/review/${data.data.campaign_id}`);
        } else {
          setError(data.error || 'Failed to create campaign');
        }
      },
      onError: (err: any) => {
        setError(err.message || 'Failed to create campaign. Please try again.');
      },
    });
  };

  return (
    <div className="min-h-screen bg-[#f5f7fb] py-12 px-4">
      <div className="max-w-3xl mx-auto">
        <div className="mb-8">
          <h1 className="text-3xl font-semibold text-gray-900 mb-2">
            Create New Campaign
          </h1>
          <p className="text-gray-600">
            Describe your product and campaign objectives. Our AI agents will generate
            optimized email variants for different customer segments.
          </p>
        </div>

        <Card>
          <CardHeader>
            <CardTitle>Campaign Brief</CardTitle>
          </CardHeader>
          <CardContent>
            <form onSubmit={handleSubmit} className="space-y-6">
              <div>
                <label
                  htmlFor="brief"
                  className="block text-sm font-medium text-gray-700 mb-2"
                >
                  Tell us about your campaign
                </label>
                <textarea
                  id="brief"
                  value={brief}
                  onChange={(e) => setBrief(e.target.value)}
                  placeholder="Example: Launch campaign for EcoBottle, a sustainable water bottle made from 100% recycled materials. Target environmentally conscious consumers aged 25-40. Goal: Drive 5000 pre-orders in first week."
                  rows={8}
                  className="w-full px-4 py-3 border border-gray-300 rounded-lg focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 outline-none transition-colors resize-none"
                  disabled={isPending}
                />
                <p className="mt-2 text-sm text-gray-500">
                  Include: product name, key features, target audience, and campaign goals
                </p>
              </div>

              {error && (
                <div className="p-4 bg-red-50 border border-red-200 rounded-lg">
                  <p className="text-sm text-red-700">{error}</p>
                </div>
              )}

              <div className="flex items-center justify-between pt-4 border-t border-gray-100">
                <div className="text-sm text-gray-500">
                  {isPending && (
                    <span className="flex items-center gap-2">
                      <Loader size="sm" />
                      AI agents are analyzing your brief...
                    </span>
                  )}
                </div>
                <Button
                  type="submit"
                  variant="primary"
                  size="lg"
                  disabled={isPending}
                  loading={isPending}
                >
                  Generate Campaign
                </Button>
              </div>
            </form>
          </CardContent>
        </Card>

        <div className="mt-8 p-6 bg-white rounded-lg border border-gray-200">
          <h3 className="text-sm font-medium text-gray-900 mb-3">What happens next?</h3>
          <ol className="space-y-2 text-sm text-gray-600">
            <li className="flex items-start gap-2">
              <span className="font-medium text-indigo-600">1.</span>
              <span>AI agents parse your brief and identify key objectives</span>
            </li>
            <li className="flex items-start gap-2">
              <span className="font-medium text-indigo-600">2.</span>
              <span>Segments are created based on customer behavior patterns</span>
            </li>
            <li className="flex items-start gap-2">
              <span className="font-medium text-indigo-600">3.</span>
              <span>Personalized email variants are generated for each segment</span>
            </li>
            <li className="flex items-start gap-2">
              <span className="font-medium text-indigo-600">4.</span>
              <span>You'll review and approve the campaign before launch</span>
            </li>
          </ol>
        </div>
      </div>
    </div>
  );
}
