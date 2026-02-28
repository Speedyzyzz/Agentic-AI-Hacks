import { Card, CardHeader, CardTitle, CardContent } from '@/components/ui/Card';
import { Badge } from '@/components/ui/Badge';
import type { DecisionLog } from '@/lib/types';
import { formatDate } from '@/lib/utils';

interface LogsPanelProps {
  logs: DecisionLog[];
}

export function LogsPanel({ logs }: LogsPanelProps) {
  if (!logs || logs.length === 0) {
    return (
      <Card>
        <CardHeader>
          <CardTitle>Agent Decision Logs</CardTitle>
        </CardHeader>
        <CardContent className="py-8">
          <p className="text-center text-gray-500">No decision logs available yet</p>
        </CardContent>
      </Card>
    );
  }

  return (
    <Card>
      <CardHeader>
        <CardTitle>Agent Decision Logs</CardTitle>
      </CardHeader>
      <CardContent>
        <div className="space-y-4">
          {logs.map((log, index) => (
            <div
              key={index}
              className="p-4 border border-gray-200 rounded-lg hover:border-indigo-200 transition-colors"
            >
              <div className="flex items-start justify-between mb-2">
                <div className="flex items-center gap-2">
                  <Badge variant="default">{log.agent}</Badge>
                  <span className="text-xs text-gray-500">{formatDate(log.timestamp)}</span>
                </div>
                {log.decision && (
                  <span className="text-xs font-medium text-indigo-600 bg-indigo-50 px-2 py-1 rounded">
                    {log.decision}
                  </span>
                )}
              </div>

              {log.reasoning && (
                <div className="mb-3">
                  <h4 className="text-sm font-medium text-gray-700 mb-1">Reasoning</h4>
                  <p className="text-sm text-gray-600 leading-relaxed">{log.reasoning}</p>
                </div>
              )}

              {log.context && Object.keys(log.context).length > 0 && (
                <div>
                  <h4 className="text-sm font-medium text-gray-700 mb-1">Context</h4>
                  <div className="bg-gray-50 rounded p-3">
                    <pre className="text-xs text-gray-600 overflow-x-auto">
                      {JSON.stringify(log.context, null, 2)}
                    </pre>
                  </div>
                </div>
              )}
            </div>
          ))}
        </div>
      </CardContent>
    </Card>
  );
}
