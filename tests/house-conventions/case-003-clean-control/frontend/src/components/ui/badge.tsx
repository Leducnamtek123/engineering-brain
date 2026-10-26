import * as React from 'react';
import { cn } from '@/lib/utils';

export function Badge({ className, ...props }: React.HTMLAttributes<HTMLSpanElement>) {
  return (
    <span
      className={cn('inline-flex items-center rounded-[3px] bg-muted px-1.5 text-xs font-medium', className)}
      {...props}
    />
  );
}
