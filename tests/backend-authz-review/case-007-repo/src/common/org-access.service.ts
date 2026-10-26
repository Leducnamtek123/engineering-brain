import { Injectable, NotFoundException } from '@nestjs/common';
import { AuthUser } from '../auth/current-user.decorator';

interface OrgScoped {
  orgId?: string | null;
}

@Injectable()
export class OrgAccessService {
  /**
   * Throws 404 when the resource belongs to another organisation.
   * Admins of the platform can read across organisations.
   */
  assertSameOrg(user: AuthUser, resource: OrgScoped | null): void {
    if (!resource) throw new NotFoundException();
    if (user.role === 'admin') return;
    if (resource.orgId && resource.orgId !== user.orgId) {
      throw new NotFoundException();
    }
  }
}
