import { int, mysqlEnum, mysqlTable, text, timestamp, decimal, varchar } from "drizzle-orm/mysql-core";
import { orders } from "./schema";

/**
 * Payments table - stores payment transaction records
 * Following Stripe integration best practices: store only IDs and business-critical data
 */
export const payments = mysqlTable("payments", {
  id: int("id").autoincrement().primaryKey(),
  orderId: int("orderId").notNull().references(() => orders.id),
  
  // Payment processor info
  processor: mysqlEnum("processor", ["stripe", "payfast", "paystack", "paypal"]).notNull(),
  processorPaymentId: varchar("processorPaymentId", { length: 255 }), // External payment ID from processor
  
  // Payment details
  amount: decimal("amount", { precision: 10, scale: 2 }).notNull(),
  currency: varchar("currency", { length: 3 }).notNull().default("USD"),
  status: mysqlEnum("status", ["pending", "completed", "failed", "cancelled", "refunded"]).notNull().default("pending"),
  
  // Customer info (for reference)
  customerEmail: varchar("customerEmail", { length: 320 }),
  customerName: text("customerName"),
  
  // Metadata
  metadata: text("metadata"), // JSON string for additional data
  
  // Timestamps
  createdAt: timestamp("createdAt").defaultNow().notNull(),
  updatedAt: timestamp("updatedAt").defaultNow().onUpdateNow().notNull(),
  completedAt: timestamp("completedAt"),
});

export type Payment = typeof payments.$inferSelect;
export type InsertPayment = typeof payments.$inferInsert;
