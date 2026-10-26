-- AlterTable
ALTER TABLE "Order" ADD COLUMN "channel" TEXT NOT NULL DEFAULT 'web';

-- CreateIndex
CREATE INDEX "Order_customerId_createdAt_idx" ON "Order"("customerId", "createdAt");
