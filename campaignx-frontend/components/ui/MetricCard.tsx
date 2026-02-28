import { cn } from '@/lib/utils';
import { ReactNode } from 'react';

interface MetricCardProps {
  title: string;
  value: string | number;
  subtitle?: string;
  trend?: 'up' | 'down' | 'neutral';
  trendValue?: string;
  icon?: ReactNode;
  className?: string;
}

export function MetricCard({ title, value, subtitle, trend, trendValue, icon, className }: MetricCardProps) {
  const trendColors = {
    up: 'text-green-600 bg-green-50',
    down: 'text-red-600 bg-red-50',
    neutral: 'text-gray-600 bg-gray-50',
  };

  return (
    <div className={cn('bg-white rounded-[20px] shadow-sm border border-gray-100 p-6', className)}>
      <div className="flex items-center justify-between mb-2">
        <p className="text-sm font-medium text-gray-600">{title}</p>
        {icon && <div className="text-gray-400">{icon}</div>}
      </div>
      <div className="flex items-baseline gap-2">
        <p className="text-3xl font-bold text-gray-900">{value}</p>
        {trend && trendValue && (
          <span className={cn('inline-flex items-center px-2 py-0.5 rounded text-xs font-medium', trendColors[trend])}>
            {trend === 'up' && '↑'}
            {trend === 'down' && '↓'}
            {trendValue}
          </span>
        )}
      </div>
      {subtitle && <p className="text-sm text-gray-500 mt-1">{subtitle}</p>}
    </div>
  );
}
