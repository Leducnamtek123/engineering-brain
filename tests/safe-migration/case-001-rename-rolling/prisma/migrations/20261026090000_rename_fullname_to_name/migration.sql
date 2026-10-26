-- Rename User.fullName to User.name (edited by hand so Prisma does not drop the column)
ALTER TABLE "User" RENAME COLUMN "fullName" TO "name";
