import { eq, and, desc, gte } from "drizzle-orm";
import { drizzle } from "drizzle-orm/mysql2";
import { 
  InsertUser, 
  users,
  subscriptionPlans,
  userSubscriptions,
  paymentTransactions,
  stockWatchlist,
  marketDataCache,
  marketingContent,
  marketingCampaigns,
  InsertSubscriptionPlan,
  InsertUserSubscription,
  InsertPaymentTransaction,
  InsertStockWatchlist,
  InsertMarketDataCache,
  InsertMarketingContent,
  InsertMarketingCampaign,
  newsletters,
  InsertNewsletter,
} from "../drizzle/schema";
import { ENV } from './_core/env';

let _db: ReturnType<typeof drizzle> | null = null;

export async function getDb() {
  if (!_db && process.env.DATABASE_URL) {
    try {
      _db = drizzle(process.env.DATABASE_URL);
    } catch (error) {
      console.warn("[Database] Failed to connect:", error);
      _db = null;
    }
  }
  return _db;
}

// ============= USER MANAGEMENT =============

export async function upsertUser(user: InsertUser): Promise<void> {
  if (!user.openId) {
    throw new Error("User openId is required for upsert");
  }

  const db = await getDb();
  if (!db) {
    console.warn("[Database] Cannot upsert user: database not available");
    return;
  }

  try {
    const values: InsertUser = {
      openId: user.openId,
    };
    const updateSet: Record<string, unknown> = {};

    const textFields = ["name", "email", "loginMethod"] as const;
    type TextField = (typeof textFields)[number];

    const assignNullable = (field: TextField) => {
      const value = user[field];
      if (value === undefined) return;
      const normalized = value ?? null;
      values[field] = normalized;
      updateSet[field] = normalized;
    };

    textFields.forEach(assignNullable);

    if (user.lastSignedIn !== undefined) {
      values.lastSignedIn = user.lastSignedIn;
      updateSet.lastSignedIn = user.lastSignedIn;
    }
    if (user.role !== undefined) {
      values.role = user.role;
      updateSet.role = user.role;
    } else if (user.openId === ENV.ownerOpenId) {
      values.role = 'admin';
      updateSet.role = 'admin';
    }

    if (!values.lastSignedIn) {
      values.lastSignedIn = new Date();
    }

    if (Object.keys(updateSet).length === 0) {
      updateSet.lastSignedIn = new Date();
    }

    await db.insert(users).values(values).onDuplicateKeyUpdate({
      set: updateSet,
    });
  } catch (error) {
    console.error("[Database] Failed to upsert user:", error);
    throw error;
  }
}

export async function getUserByOpenId(openId: string) {
  const db = await getDb();
  if (!db) {
    console.warn("[Database] Cannot get user: database not available");
    return undefined;
  }

  const result = await db.select().from(users).where(eq(users.openId, openId)).limit(1);
  return result.length > 0 ? result[0] : undefined;
}

export async function getUserById(id: number) {
  const db = await getDb();
  if (!db) return undefined;

  const result = await db.select().from(users).where(eq(users.id, id)).limit(1);
  return result.length > 0 ? result[0] : undefined;
}

// ============= SUBSCRIPTION PLANS =============

export async function getAllSubscriptionPlans() {
  const db = await getDb();
  if (!db) return [];

  return db.select().from(subscriptionPlans).where(eq(subscriptionPlans.active, true)).orderBy(subscriptionPlans.priceRands);
}

export async function getSubscriptionPlanById(id: number) {
  const db = await getDb();
  if (!db) return undefined;

  const result = await db.select().from(subscriptionPlans).where(eq(subscriptionPlans.id, id)).limit(1);
  return result.length > 0 ? result[0] : undefined;
}

export async function createSubscriptionPlan(plan: InsertSubscriptionPlan) {
  const db = await getDb();
  if (!db) throw new Error("Database not available");

  const result = await db.insert(subscriptionPlans).values(plan);
  return result;
}

// ============= USER SUBSCRIPTIONS =============

export async function getUserActiveSubscription(userId: number) {
  const db = await getDb();
  if (!db) return undefined;

  const now = new Date();
  const result = await db
    .select()
    .from(userSubscriptions)
    .where(
      and(
        eq(userSubscriptions.userId, userId),
        eq(userSubscriptions.status, "active"),
        gte(userSubscriptions.endDate, now)
      )
    )
    .orderBy(desc(userSubscriptions.endDate))
    .limit(1);

  return result.length > 0 ? result[0] : undefined;
}

export async function getUserSubscriptionHistory(userId: number) {
  const db = await getDb();
  if (!db) return [];

  return db
    .select()
    .from(userSubscriptions)
    .where(eq(userSubscriptions.userId, userId))
    .orderBy(desc(userSubscriptions.createdAt));
}

export async function createUserSubscription(subscription: InsertUserSubscription) {
  const db = await getDb();
  if (!db) throw new Error("Database not available");

  const result = await db.insert(userSubscriptions).values(subscription);
  const insertId = Number(result[0].insertId);
  
  // Fetch and return the created subscription
  const created = await db.select().from(userSubscriptions).where(eq(userSubscriptions.id, insertId));
  return created[0];
}

export async function updateSubscriptionStatus(id: number, status: "active" | "expired" | "cancelled" | "pending") {
  const db = await getDb();
  if (!db) throw new Error("Database not available");

  await db.update(userSubscriptions).set({ status, updatedAt: new Date() }).where(eq(userSubscriptions.id, id));
}

// ============= PAYMENT TRANSACTIONS =============

export async function createPaymentTransaction(transaction: InsertPaymentTransaction) {
  const db = await getDb();
  if (!db) throw new Error("Database not available");

  const result = await db.insert(paymentTransactions).values(transaction);
  return result;
}

export async function getPaymentTransactionByYocoId(yocoPaymentId: string) {
  const db = await getDb();
  if (!db) return undefined;

  const result = await db.select().from(paymentTransactions).where(eq(paymentTransactions.yocoPaymentId, yocoPaymentId)).limit(1);
  return result.length > 0 ? result[0] : undefined;
}

export async function getUserPaymentHistory(userId: number) {
  const db = await getDb();
  if (!db) return [];

  return db
    .select()
    .from(paymentTransactions)
    .where(eq(paymentTransactions.userId, userId))
    .orderBy(desc(paymentTransactions.transactionDate));
}

export async function updatePaymentStatus(id: number, status: "pending" | "completed" | "failed" | "refunded") {
  const db = await getDb();
  if (!db) throw new Error("Database not available");

  await db.update(paymentTransactions).set({ status, updatedAt: new Date() }).where(eq(paymentTransactions.id, id));
}

// ============= STOCK WATCHLIST =============

export async function getUserWatchlist(userId: number) {
  const db = await getDb();
  if (!db) return [];

  return db.select().from(stockWatchlist).where(eq(stockWatchlist.userId, userId)).orderBy(desc(stockWatchlist.addedAt));
}

export async function addToWatchlist(item: InsertStockWatchlist) {
  const db = await getDb();
  if (!db) throw new Error("Database not available");

  const result = await db.insert(stockWatchlist).values(item);
  return result;
}

export async function removeFromWatchlist(id: number) {
  const db = await getDb();
  if (!db) throw new Error("Database not available");

  await db.delete(stockWatchlist).where(eq(stockWatchlist.id, id));
}

// ============= MARKET DATA CACHE =============

export async function getMarketDataCache(stockSymbol: string) {
  const db = await getDb();
  if (!db) return undefined;

  const result = await db.select().from(marketDataCache).where(eq(marketDataCache.stockSymbol, stockSymbol)).limit(1);
  return result.length > 0 ? result[0] : undefined;
}

export async function getAllMarketDataCache() {
  const db = await getDb();
  if (!db) return [];

  return db.select().from(marketDataCache).orderBy(marketDataCache.stockSymbol);
}

export async function upsertMarketDataCache(data: InsertMarketDataCache) {
  const db = await getDb();
  if (!db) throw new Error("Database not available");

  await db
    .insert(marketDataCache)
    .values(data)
    .onDuplicateKeyUpdate({
      set: {
        currentPrice: data.currentPrice,
        priceChange: data.priceChange,
        priceChangePercent: data.priceChangePercent,
        volume: data.volume,
        marketCap: data.marketCap,
        sector: data.sector,
        ecmConfidence: data.ecmConfidence,
        marketDirection: data.marketDirection,
        supportLevel: data.supportLevel,
        resistanceLevel: data.resistanceLevel,
        lastUpdated: new Date(),
      },
    });
}

// ============= NEWSLETTERS =============

export async function getActiveSubscribers() {
  const db = await getDb();
  if (!db) return [];

  try {
    const activeUsers = await db
      .select({
        id: users.id,
        email: users.email,
        name: users.name,
      })
      .from(users)
      .innerJoin(userSubscriptions, eq(users.id, userSubscriptions.userId))
      .where(eq(userSubscriptions.status, "active"));
    
    return activeUsers.filter((u) => u.email);
  } catch (error) {
    console.error("[Database] Error getting active subscribers:", error);
    return [];
  }
}

export async function saveNewsletterRecord(data: {
  userId: number;
  subject: string;
  content: string;
  sentAt: Date;
}) {
  const db = await getDb();
  if (!db) return;

  try {
    await db.insert(newsletters).values(data);
  } catch (error) {
    console.error("[Database] Error saving newsletter:", error);
    throw error;
  }
}

export async function getUserNewsletters(userId: number) {
  const db = await getDb();
  if (!db) return [];

  try {
    return await db
      .select()
      .from(newsletters)
      .where(eq(newsletters.userId, userId))
      .orderBy(desc(newsletters.sentAt));
  } catch (error) {
    console.error("[Database] Error getting user newsletters:", error);
    return [];
  }
}

// ============= MARKETING CONTENT =============

export async function createMarketingContent(content: InsertMarketingContent) {
  const db = await getDb();
  if (!db) throw new Error("Database not available");

  const result = await db.insert(marketingContent).values(content);
  return result;
}

export async function getScheduledMarketingContent() {
  const db = await getDb();
  if (!db) return [];

  const now = new Date();
  return db
    .select()
    .from(marketingContent)
    .where(
      and(
        eq(marketingContent.status, "scheduled"),
        gte(marketingContent.scheduledFor!, now)
      )
    )
    .orderBy(marketingContent.scheduledFor);
}

export async function getAllMarketingContent() {
  const db = await getDb();
  if (!db) return [];

  return db.select().from(marketingContent).orderBy(desc(marketingContent.createdAt));
}

export async function updateMarketingContentStatus(id: number, status: "draft" | "scheduled" | "published" | "archived", publishedAt?: Date) {
  const db = await getDb();
  if (!db) throw new Error("Database not available");

  const updateData: any = { status, updatedAt: new Date() };
  if (publishedAt) {
    updateData.publishedAt = publishedAt;
  }

  await db.update(marketingContent).set(updateData).where(eq(marketingContent.id, id));
}

// ============= MARKETING CAMPAIGNS =============

export async function createMarketingCampaign(campaign: InsertMarketingCampaign) {
  const db = await getDb();
  if (!db) throw new Error("Database not available");

  const result = await db.insert(marketingCampaigns).values(campaign);
  return result;
}

export async function getAllMarketingCampaigns() {
  const db = await getDb();
  if (!db) return [];

  return db.select().from(marketingCampaigns).orderBy(desc(marketingCampaigns.createdAt));
}

export async function getActiveCampaigns() {
  const db = await getDb();
  if (!db) return [];

  return db.select().from(marketingCampaigns).where(eq(marketingCampaigns.status, "active")).orderBy(desc(marketingCampaigns.startDate));
}

export async function updateCampaignMetrics(id: number, metrics: string, spent: string) {
  const db = await getDb();
  if (!db) throw new Error("Database not available");

  await db.update(marketingCampaigns).set({ metrics, spent, updatedAt: new Date() }).where(eq(marketingCampaigns.id, id));
}
