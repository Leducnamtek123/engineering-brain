import { createParamDecorator, ExecutionContext, UnauthorizedException } from '@nestjs/common';

export interface AuthUser {
  id: string;
  orgId: string;
  role: 'member' | 'admin';
}

export const CurrentUser = createParamDecorator((_: unknown, ctx: ExecutionContext): AuthUser => {
  const user = ctx.switchToHttp().getRequest().user as AuthUser | undefined;
  if (!user?.id || !user?.orgId) throw new UnauthorizedException();
  return user;
});
