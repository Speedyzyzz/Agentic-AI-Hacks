import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/Card';
import { Badge } from '@/components/ui/Badge';
import type { Variant } from '@/lib/types';
import { truncate } from '@/lib/utils';

interface VariantCardProps {
  variant: Variant;
  index: number;
}

export function VariantCard({ variant, index }: VariantCardProps) {
  const segmentName = variant.segment?.name || variant.segment_name || 'Unknown Segment';
  const subjectLine = variant.subject_line || variant.subject || 'No subject';
  const segmentDescription = variant.segment?.description || variant.segment?.reasoning || '';

  return (
    <Card>
      <CardHeader>
        <div className="flex items-center justify-between">
          <CardTitle className="text-lg">Variant {index + 1}</CardTitle>
          <Badge variant="default">{segmentName}</Badge>
        </div>
      </CardHeader>
      <CardContent className="space-y-4">
        <div>
          <h3 className="text-sm font-medium text-gray-500">Subject Line</h3>
          <p className="mt-1 text-base font-medium text-gray-900">{subjectLine}</p>
        </div>

        <div>
          <h3 className="text-sm font-medium text-gray-500">Email Body</h3>
          <div className="mt-1 p-4 bg-gray-50 rounded-lg">
            <p className="text-sm text-gray-800 whitespace-pre-wrap">
              {truncate(variant.body, 300)}
            </p>
          </div>
        </div>

        <div className="pt-4 border-t border-gray-100 space-y-3">
          {segmentDescription && (
            <div>
              <h3 className="text-sm font-medium text-gray-500">Segment Details</h3>
              <p className="mt-1 text-sm text-gray-700">{segmentDescription}</p>
            </div>
          )}

          <div>
            <h3 className="text-sm font-medium text-gray-500">Strategy</h3>
            <p className="mt-1 text-sm text-gray-700">{variant.strategy}</p>
          </div>

          {variant.reasoning && (
            <div>
              <h3 className="text-sm font-medium text-gray-500">AI Reasoning</h3>
              <p className="mt-1 text-sm text-gray-600 italic">{variant.reasoning}</p>
            </div>
          )}
        </div>
      </CardContent>
    </Card>
  );
}
