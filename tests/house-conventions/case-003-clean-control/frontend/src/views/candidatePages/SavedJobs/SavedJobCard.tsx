import { useTranslation } from 'react-i18next';
import { Badge } from '@/components/ui/badge';
import { Button } from '@/components/ui/button';

export interface SavedJob {
  id: number;
  title: string;
  companyName: string;
  isClosed: boolean;
}

interface SavedJobCardProps {
  job: SavedJob;
  onUnsave: (id: number) => void;
}

export function SavedJobCard({ job, onUnsave }: SavedJobCardProps) {
  const { t } = useTranslation('candidate');

  return (
    <div className="flex items-center justify-between rounded-sm border p-4">
      <div>
        <p className="font-medium">{job.title}</p>
        <p className="text-sm text-muted-foreground">{job.companyName}</p>
        {job.isClosed && <Badge className="mt-1">{t('savedJobs.closed')}</Badge>}
      </div>
      <Button variant="outline" size="sm" onClick={() => onUnsave(job.id)}>
        {t('savedJobs.unsave')}
      </Button>
    </div>
  );
}
