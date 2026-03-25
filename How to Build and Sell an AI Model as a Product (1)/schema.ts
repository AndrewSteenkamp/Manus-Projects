import { int, mysqlEnum, mysqlTable, text, timestamp, varchar, decimal, boolean } from "drizzle-orm/mysql-core";

/**
 * Core user table backing auth flow.
 */
export const users = mysqlTable("users", {
  id: int("id").autoincrement().primaryKey(),
  openId: varchar("openId", { length: 64 }).notNull().unique(),
  name: text("name"),
  email: varchar("email", { length: 320 }),
  loginMethod: varchar("loginMethod", { length: 64 }),
  role: mysqlEnum("role", ["user", "admin"]).default("user").notNull(),
  createdAt: timestamp("createdAt").defaultNow().notNull(),
  updatedAt: timestamp("updatedAt").defaultNow().onUpdateNow().notNull(),
  lastSignedIn: timestamp("lastSignedIn").defaultNow().notNull(),
});

export type User = typeof users.$inferSelect;
export type InsertUser = typeof users.$inferInsert;

/**
 * Subscription plans for Siener AI (R499, R999, R2499)
 */
export const subscriptionPlans = mysqlTable("subscription_plans", {
  id: int("id").autoincrement().primaryKey(),
  name: varchar("name", { length: 100 }).notNull(),
  description: text("description"),
  priceRands: decimal("priceRands", { precision: 10, scale: 2 }).notNull(),
  billingCycle: mysqlEnum("billingCycle", ["monthly", "yearly"]).default("monthly").notNull(),
  features: text("features").notNull(), // JSON string of features array
  maxStocks: int("maxStocks").default(10).notNull(),
  maxAlerts: int("maxAlerts").default(5).notNull(),
  advancedAnalytics: boolean("advancedAnalytics").default(false).notNull(),
  apiAccess: boolean("apiAccess").default(false).notNull(),
  prioritySupport: boolean("prioritySupport").default(false).notNull(),
  active: boolean("active").default(true).notNull(),
  createdAt: timestamp("createdAt").defaultNow().notNull(),
  updatedAt: timestamp("updatedAt").defaultNow().onUpdateNow().notNull(),
});

export type SubscriptionPlan = typeof subscriptionPlans.$inferSelect;
export type InsertSubscriptionPlan = typeof subscriptionPlans.$inferInsert;

/**
 * User subscriptions tracking
 */
export const userSubscriptions = mysqlTable("user_subscriptions", {
  id: int("id").autoincrement().primaryKey(),
  userId: int("userId").notNull(),
  planId: int("planId").notNull(),
  status: mysqlEnum("status", ["active", "expired", "cancelled", "pending"]).default("pending").notNull(),
  startDate: timestamp("startDate").notNull(),
  endDate: timestamp("endDate").notNull(),
  autoRenew: boolean("autoRenew").default(true).notNull(),
  yocoPaymentId: varchar("yocoPaymentId", { length: 255 }),
  createdAt: timestamp("createdAt").defaultNow().notNull(),
  updatedAt: timestamp("updatedAt").defaultNow().onUpdateNow().notNull(),
});

export type UserSubscription = typeof userSubscriptions.$inferSelect;
export type InsertUserSubscription = typeof userSubscriptions.$inferInsert;

/**
 * Payment transactions for Yoco integration
 */
export const paymentTransactions = mysqlTable("payment_transactions", {
  id: int("id").autoincrement().primaryKey(),
  userId: int("userId").notNull(),
  subscriptionId: int("subscriptionId"),
  yocoPaymentId: varchar("yocoPaymentId", { length: 255 }).notNull(),
  amountRands: decimal("amountRands", { precision: 10, scale: 2 }).notNull(),
  currency: varchar("currency", { length: 3 }).default("ZAR").notNull(),
  status: mysqlEnum("status", ["pending", "completed", "failed", "refunded"]).default("pending").notNull(),
  paymentMethod: varchar("paymentMethod", { length: 50 }),
  transactionDate: timestamp("transactionDate").defaultNow().notNull(),
  metadata: text("metadata"), // JSON string for additional Yoco data
  createdAt: timestamp("createdAt").defaultNow().notNull(),
  updatedAt: timestamp("updatedAt").defaultNow().onUpdateNow().notNull(),
});

export type PaymentTransaction = typeof paymentTransactions.$inferSelect;
export type InsertPaymentTransaction = typeof paymentTransactions.$inferInsert;

/**
 * JSE stock watchlist for users
 */
export const stockWatchlist = mysqlTable("stock_watchlist", {
  id: int("id").autoincrement().primaryKey(),
  userId: int("userId").notNull(),
  stockSymbol: varchar("stockSymbol", { length: 20 }).notNull(),
  stockName: varchar("stockName", { length: 200 }),
  notes: text("notes"),
  addedAt: timestamp("addedAt").defaultNow().notNull(),
});

export type StockWatchlist = typeof stockWatchlist.$inferSelect;
export type InsertStockWatchlist = typeof stockWatchlist.$inferInsert;

/**
 * Market data cache for performance optimization
 */
export const marketDataCache = mysqlTable("market_data_cache", {
  id: int("id").autoincrement().primaryKey(),
  stockSymbol: varchar("stockSymbol", { length: 20 }).notNull().unique(),
  currentPrice: decimal("currentPrice", { precision: 15, scale: 4 }),
  priceChange: decimal("priceChange", { precision: 15, scale: 4 }),
  priceChangePercent: decimal("priceChangePercent", { precision: 10, scale: 2 }),
  volume: varchar("volume", { length: 50 }),
  marketCap: varchar("marketCap", { length: 50 }),
  sector: varchar("sector", { length: 100 }),
  ecmConfidence: decimal("ecmConfidence", { precision: 5, scale: 2 }),
  marketDirection: mysqlEnum("marketDirection", ["bullish", "bearish", "neutral"]),
  supportLevel: decimal("supportLevel", { precision: 15, scale: 4 }),
  resistanceLevel: decimal("resistanceLevel", { precision: 15, scale: 4 }),
  lastUpdated: timestamp("lastUpdated").defaultNow().onUpdateNow().notNull(),
  createdAt: timestamp("createdAt").defaultNow().notNull(),
});

export type MarketDataCache = typeof marketDataCache.$inferSelect;
export type InsertMarketDataCache = typeof marketDataCache.$inferInsert;

/**
 * Marketing content generated by autonomous agent
 */
export const marketingContent = mysqlTable("marketing_content", {
  id: int("id").autoincrement().primaryKey(),
  contentType: mysqlEnum("contentType", ["social_post", "blog", "email", "ad_copy"]).notNull(),
  platform: varchar("platform", { length: 50 }), // twitter, facebook, linkedin, etc.
  title: varchar("title", { length: 500 }),
  content: text("content").notNull(),
  imageUrl: varchar("imageUrl", { length: 500 }),
  status: mysqlEnum("status", ["draft", "scheduled", "published", "archived"]).default("draft").notNull(),
  scheduledFor: timestamp("scheduledFor"),
  publishedAt: timestamp("publishedAt"),
  engagement: text("engagement"), // JSON string with likes, shares, comments
  generatedBy: varchar("generatedBy", { length: 100 }).default("autonomous_agent").notNull(),
  createdAt: timestamp("createdAt").defaultNow().notNull(),
  updatedAt: timestamp("updatedAt").defaultNow().onUpdateNow().notNull(),
});

export type MarketingContent = typeof marketingContent.$inferSelect;
export type InsertMarketingContent = typeof marketingContent.$inferInsert;

/**
 * Marketing campaigns tracking
 */
export const marketingCampaigns = mysqlTable("marketing_campaigns", {
  id: int("id").autoincrement().primaryKey(),
  name: varchar("name", { length: 200 }).notNull(),
  description: text("description"),
  campaignType: mysqlEnum("campaignType", ["awareness", "acquisition", "retention", "conversion"]).notNull(),
  status: mysqlEnum("status", ["planning", "active", "paused", "completed"]).default("planning").notNull(),
  budget: decimal("budget", { precision: 10, scale: 2 }),
  spent: decimal("spent", { precision: 10, scale: 2 }).default("0.00"),
  startDate: timestamp("startDate"),
  endDate: timestamp("endDate"),
  targetAudience: text("targetAudience"),
  metrics: text("metrics"), // JSON string with impressions, clicks, conversions
  createdAt: timestamp("createdAt").defaultNow().notNull(),
  updatedAt: timestamp("updatedAt").defaultNow().onUpdateNow().notNull(),
});

export type MarketingCampaign = typeof marketingCampaigns.$inferSelect;
export type InsertMarketingCampaign = typeof marketingCampaigns.$inferInsert;

/**
 * Weekly newsletters sent to subscribers
 */
export const newsletters = mysqlTable("newsletters", {
  id: int("id").autoincrement().primaryKey(),
  userId: int("userId").notNull(),
  subject: varchar("subject", { length: 255 }).notNull(),
  content: text("content").notNull(), // HTML content
  sentAt: timestamp("sentAt").defaultNow().notNull(),
  opened: boolean("opened").default(false).notNull(),
  openedAt: timestamp("openedAt"),
});

export type Newsletter = typeof newsletters.$inferSelect;
export type InsertNewsletter = typeof newsletters.$inferInsert;
