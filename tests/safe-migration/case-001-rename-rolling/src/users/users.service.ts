import { Injectable } from '@nestjs/common';
import { PrismaService } from '../prisma.service';

@Injectable()
export class UsersService {
  constructor(private readonly prisma: PrismaService) {}

  findOne(id: string) {
    return this.prisma.user.findUnique({ where: { id }, select: { id: true, email: true, name: true } });
  }

  rename(id: string, name: string) {
    return this.prisma.user.update({ where: { id }, data: { name } });
  }
}
