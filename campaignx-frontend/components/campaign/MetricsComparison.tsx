import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/Card';
import { MetricCard } from '@/components/ui/MetricCard';
import { formatPercentage, calculatePercentageChange } from '@/lib/utils';
import type { Metrics } from '@/lib/types';

interface MetricsComparisonProps {
  baseline: Metrics | null;
  optimized: Metrics | null;
}

export function MetricsComparison({ baseline, optimized }: MetricsComparisonProps) {
  if (!baseline && !optimized) {
    return (
      <Card>
        <CardContent className="py-12">
          <p className="text-center text-gray-500">No metrics available yet</p>
        </CardContent>
      </Card>
    );
  }

  const metrics = [
    {
      title: 'Open Rate',
      baseline: baseline?.open_rate,
      optimized: optimized?.open_rate,
    },
    {
      title: 'Click Rate',
      baseline: baseline?.click_rate,
      optimized: optimized?.click_rate,
    },
    {
      title: 'Conversion Rate',
      baseline: baseline?.conversion_rate,
      optimized: optimized?.conversion_rate,
    },
    {
      title: 'Revenue',
      baseline: baseline?.revenue,
      optimized: optimized?.revenue,
      isCurrency: true,
    },
  ];

  return (
    <Card>
      <CardHeader>
        <CardTitle>Performance Metrics</CardTitle>
      </CardHeader>
      <CardContent>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4">
          {metrics.map((metric) => {
            const baseValue = metric.baseline ?? 0;
            const optValue = metric.optimized ?? 0;
            const change = calculatePercentageChange(baseValue, optValue);

            return (
              <MetricCard
                key={metric.title}
                title={metric.title}
                value={
                  metric.isCurrency
                    ? `$${optValue.toLocaleString()}`
                    : formatPercentage(optValue)
                }
                trend={change > 0 ? 'up' : change < 0 ? 'down' : 'neutral'}
                subtitle={
                  baseline && optimized
                    ? `${change > 0 ? '+' : ''}${change.toFixed(1)}% vs baseline`
                    : baseline
                    ? 'Baseline'
                    : 'Current'
                }
              />
            );
          })}
        </div>

        {baseline && optimized && (
          <div className="mt-6 pt-6 border-t border-gray-100">
            <h3 className="text-sm font-medium text-gray-700 mb-3">Detailed Comparison</h3>
            <div className="space-y-2">
              {metrics.map((metric) => {
                const baseValue = metric.baseline ?? 0;
                const optValue = metric.optimized ?? 0;
                const change = calculatePercentageChange(baseValue, optValue);

                return (
                  <div key={metric.title} className="flex justify-between items-center py-2">
                    <span className="text-sm text-gray-600">{metric.title}</span>
                    <div className="flex items-center gap-4">
                      <span className="text-sm text-gray-500">
                        {metric.isCurrency ? `$${baseValue.toFixed(2)}` : formatPercentage(baseValue)}
                      </span>
                      <span className="text-sm text-gray-400">→</span>
                      <span className="text-sm font-medium text-gray-900">
                        {metric.isCurrency ? `$${optValue.toFixed(2)}` : formatPercentage(optValue)}
                      </span>
                      <span
                        className={`text-sm font-medium ${
                          change > 0 ? 'text-green-600' : change < 0 ? 'text-red-600' : 'text-gray-500'
                        }`}
                      >
                        ({change > 0 ? '+' : ''}{change.toFixed(1)}%)
                      </span>
                    </div>
                  </div>
                );
              })}
            </div>
          </div>
        )}
      </CardContent>
    </Card>
  );
}
