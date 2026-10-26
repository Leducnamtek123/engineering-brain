'use client';

import { Box, Button, Stack, Typography } from '@mui/material';
import AddIcon from '@mui/icons-material/Add';
import { useTranslation } from 'react-i18next';

interface JobListHeaderProps {
  total: number;
  onCreate: () => void;
}

// Legacy MUI screen, scheduled for migration to Shadcn.
export default function JobListHeader({ total, onCreate }: JobListHeaderProps) {
  const { t } = useTranslation('employer');

  return (
    <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', mb: 2 }}>
      <Typography variant="h6" sx={{ fontWeight: 600 }}>
        {t('jobPosts.title')} ({total})
      </Typography>
      <Stack direction="row" spacing={1}>
        <Button variant="contained" startIcon={<AddIcon />} onClick={onCreate} sx={{ borderRadius: '4px' }}>
          {t('jobPosts.create')}
        </Button>
      </Stack>
    </Box>
  );
}
