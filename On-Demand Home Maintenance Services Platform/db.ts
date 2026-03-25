import { eq, and, desc, sql } from "drizzle-orm";
import { drizzle } from "drizzle-orm/mysql2";
import { 
  InsertUser, 
  users, 
  providerProfiles,
  serviceCategories,
  providerServices,
  portfolioItems,
  serviceRequests,
  quotes,
  bookings,
  payments,
  reviews,
  messages,
  adminNotes,
  InsertProviderProfile,
  InsertServiceRequest,
  InsertQuote,
  InsertBooking,
  InsertPayment,
  InsertReview,
  InsertMessage,
  InsertAdminNote,
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

// ============================================================================
// USER MANAGEMENT
// ============================================================================

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
    
    // Handle role assignment
    if (user.role !== undefined) {
      values.role = user.role;
      updateSet.role = user.role;
    } else if (user.openId === ENV.ownerOpenId) {
      values.role = 'admin';
      updateSet.role = 'admin';
    } else {
      values.role = 'customer'; // Default role
      updateSet.role = 'customer';
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

export async function getUserById(userId: number) {
  const db = await getDb();
  if (!db) return undefined;

  const result = await db.select().from(users).where(eq(users.id, userId)).limit(1);
  return result.length > 0 ? result[0] : undefined;
}

export async function updateUserRole(userId: number, role: "customer" | "provider" | "admin") {
  const db = await getDb();
  if (!db) return false;

  await db.update(users).set({ role }).where(eq(users.id, userId));
  return true;
}

// ============================================================================
// PROVIDER PROFILE MANAGEMENT
// ============================================================================

export async function createProviderProfile(profile: InsertProviderProfile) {
  const db = await getDb();
  if (!db) throw new Error("Database not available");

  const result = await db.insert(providerProfiles).values(profile);
  return result;
}

export async function getProviderProfileByUserId(userId: number) {
  const db = await getDb();
  if (!db) return undefined;

  const result = await db.select().from(providerProfiles).where(eq(providerProfiles.userId, userId)).limit(1);
  return result.length > 0 ? result[0] : undefined;
}

export async function updateProviderProfile(userId: number, updates: Partial<InsertProviderProfile>) {
  const db = await getDb();
  if (!db) return false;

  await db.update(providerProfiles).set(updates).where(eq(providerProfiles.userId, userId));
  return true;
}

export async function getProviderProfileById(profileId: number) {
  const db = await getDb();
  if (!db) return undefined;

  const result = await db.select().from(providerProfiles).where(eq(providerProfiles.id, profileId)).limit(1);
  return result.length > 0 ? result[0] : undefined;
}

// Get all pending provider applications for admin review
export async function getPendingProviderApplications() {
  const db = await getDb();
  if (!db) return [];

  const result = await db
    .select({
      profile: providerProfiles,
      user: users,
    })
    .from(providerProfiles)
    .leftJoin(users, eq(providerProfiles.userId, users.id))
    .where(eq(providerProfiles.verificationStatus, "pending"))
    .orderBy(desc(providerProfiles.createdAt));

  return result;
}

// Update provider tier based on performance
export async function updateProviderTier(userId: number, tier: "probationary" | "verified" | "premium") {
  const db = await getDb();
  if (!db) return false;

  await db.update(providerProfiles).set({ tier }).where(eq(providerProfiles.userId, userId));
  return true;
}

// ============================================================================
// SERVICE CATEGORIES
// ============================================================================

export async function getAllServiceCategories() {
  const db = await getDb();
  if (!db) return [];

  const result = await db.select().from(serviceCategories).where(eq(serviceCategories.active, true));
  return result;
}

export async function getServiceCategoryById(categoryId: number) {
  const db = await getDb();
  if (!db) return undefined;

  const result = await db.select().from(serviceCategories).where(eq(serviceCategories.id, categoryId)).limit(1);
  return result.length > 0 ? result[0] : undefined;
}

// ============================================================================
// PROVIDER SERVICES (Categories offered by provider)
// ============================================================================

export async function addProviderService(providerId: number, categoryId: number) {
  const db = await getDb();
  if (!db) throw new Error("Database not available");

  await db.insert(providerServices).values({ providerId, categoryId });
}

export async function getProviderServices(providerId: number) {
  const db = await getDb();
  if (!db) return [];

  const result = await db
    .select({
      service: providerServices,
      category: serviceCategories,
    })
    .from(providerServices)
    .leftJoin(serviceCategories, eq(providerServices.categoryId, serviceCategories.id))
    .where(eq(providerServices.providerId, providerId));

  return result;
}

export async function removeProviderService(providerId: number, categoryId: number) {
  const db = await getDb();
  if (!db) return false;

  await db.delete(providerServices).where(
    and(
      eq(providerServices.providerId, providerId),
      eq(providerServices.categoryId, categoryId)
    )
  );
  return true;
}

// ============================================================================
// PORTFOLIO ITEMS
// ============================================================================

export async function addPortfolioItem(item: { providerId: number; title?: string; description?: string; imageUrl: string; categoryId?: number }) {
  const db = await getDb();
  if (!db) throw new Error("Database not available");

  const result = await db.insert(portfolioItems).values(item);
  return result;
}

export async function getProviderPortfolio(providerId: number) {
  const db = await getDb();
  if (!db) return [];

  const result = await db.select().from(portfolioItems).where(eq(portfolioItems.providerId, providerId)).orderBy(desc(portfolioItems.createdAt));
  return result;
}

export async function deletePortfolioItem(itemId: number, providerId: number) {
  const db = await getDb();
  if (!db) return false;

  await db.delete(portfolioItems).where(
    and(
      eq(portfolioItems.id, itemId),
      eq(portfolioItems.providerId, providerId)
    )
  );
  return true;
}

// ============================================================================
// SERVICE REQUESTS
// ============================================================================

export async function createServiceRequest(request: InsertServiceRequest) {
  const db = await getDb();
  if (!db) throw new Error("Database not available");

  const result = await db.insert(serviceRequests).values(request);
  return result;
}

export async function getServiceRequestById(requestId: number) {
  const db = await getDb();
  if (!db) return undefined;

  const result = await db.select().from(serviceRequests).where(eq(serviceRequests.id, requestId)).limit(1);
  return result.length > 0 ? result[0] : undefined;
}

export async function getCustomerServiceRequests(customerId: number) {
  const db = await getDb();
  if (!db) return [];

  const result = await db
    .select()
    .from(serviceRequests)
    .where(eq(serviceRequests.customerId, customerId))
    .orderBy(desc(serviceRequests.createdAt));

  return result;
}

export async function getOpenServiceRequests() {
  const db = await getDb();
  if (!db) return [];

  const result = await db
    .select()
    .from(serviceRequests)
    .where(eq(serviceRequests.status, "open"))
    .orderBy(desc(serviceRequests.createdAt));

  return result;
}

export async function updateServiceRequestStatus(requestId: number, status: "open" | "quoted" | "accepted" | "closed") {
  const db = await getDb();
  if (!db) return false;

  await db.update(serviceRequests).set({ status }).where(eq(serviceRequests.id, requestId));
  return true;
}

// ============================================================================
// QUOTES
// ============================================================================

export async function createQuote(quote: InsertQuote) {
  const db = await getDb();
  if (!db) throw new Error("Database not available");

  const result = await db.insert(quotes).values(quote);
  return result;
}

export async function getQuotesByRequestId(requestId: number) {
  const db = await getDb();
  if (!db) return [];

  const result = await db
    .select({
      quote: quotes,
      provider: providerProfiles,
      user: users,
    })
    .from(quotes)
    .leftJoin(providerProfiles, eq(quotes.providerId, providerProfiles.userId))
    .leftJoin(users, eq(quotes.providerId, users.id))
    .where(eq(quotes.requestId, requestId))
    .orderBy(quotes.amount);

  return result;
}

export async function getProviderQuotes(providerId: number) {
  const db = await getDb();
  if (!db) return [];

  const result = await db
    .select()
    .from(quotes)
    .where(eq(quotes.providerId, providerId))
    .orderBy(desc(quotes.createdAt));

  return result;
}

export async function updateQuoteStatus(quoteId: number, status: "pending" | "accepted" | "rejected" | "withdrawn") {
  const db = await getDb();
  if (!db) return false;

  await db.update(quotes).set({ status }).where(eq(quotes.id, quoteId));
  return true;
}

export async function getQuoteById(quoteId: number) {
  const db = await getDb();
  if (!db) return undefined;

  const result = await db.select().from(quotes).where(eq(quotes.id, quoteId)).limit(1);
  return result.length > 0 ? result[0] : undefined;
}

// ============================================================================
// BOOKINGS
// ============================================================================

export async function createBooking(booking: InsertBooking) {
  const db = await getDb();
  if (!db) throw new Error("Database not available");

  const result = await db.insert(bookings).values(booking);
  return result;
}

export async function getBookingById(bookingId: number) {
  const db = await getDb();
  if (!db) return undefined;

  const result = await db.select().from(bookings).where(eq(bookings.id, bookingId)).limit(1);
  return result.length > 0 ? result[0] : undefined;
}

export async function getCustomerBookings(customerId: number) {
  const db = await getDb();
  if (!db) return [];

  const result = await db
    .select()
    .from(bookings)
    .where(eq(bookings.customerId, customerId))
    .orderBy(desc(bookings.createdAt));

  return result;
}

export async function getProviderBookings(providerId: number) {
  const db = await getDb();
  if (!db) return [];

  const result = await db
    .select()
    .from(bookings)
    .where(eq(bookings.providerId, providerId))
    .orderBy(desc(bookings.createdAt));

  return result;
}

export async function updateBookingStatus(
  bookingId: number, 
  status: "pending" | "confirmed" | "in_progress" | "completed" | "cancelled"
) {
  const db = await getDb();
  if (!db) return false;

  const updates: any = { status };
  
  // Set appropriate timestamp based on status
  if (status === "confirmed") updates.confirmedAt = new Date();
  if (status === "in_progress") updates.startedAt = new Date();
  if (status === "completed") updates.completedAt = new Date();
  if (status === "cancelled") updates.cancelledAt = new Date();

  await db.update(bookings).set(updates).where(eq(bookings.id, bookingId));
  return true;
}

// ============================================================================
// PAYMENTS
// ============================================================================

export async function createPayment(payment: InsertPayment) {
  const db = await getDb();
  if (!db) throw new Error("Database not available");

  const result = await db.insert(payments).values(payment);
  return result;
}

export async function getPaymentByBookingId(bookingId: number) {
  const db = await getDb();
  if (!db) return undefined;

  const result = await db.select().from(payments).where(eq(payments.bookingId, bookingId)).limit(1);
  return result.length > 0 ? result[0] : undefined;
}

export async function updatePaymentStatus(
  paymentId: number,
  status: "pending" | "processing" | "completed" | "failed" | "refunded"
) {
  const db = await getDb();
  if (!db) return false;

  await db.update(payments).set({ status }).where(eq(payments.id, paymentId));
  return true;
}

export async function releasePaymentFromEscrow(paymentId: number) {
  const db = await getDb();
  if (!db) return false;

  await db.update(payments).set({ 
    heldInEscrow: false, 
    releasedAt: new Date() 
  }).where(eq(payments.id, paymentId));
  return true;
}

// ============================================================================
// REVIEWS
// ============================================================================

export async function createReview(review: InsertReview) {
  const db = await getDb();
  if (!db) throw new Error("Database not available");

  const result = await db.insert(reviews).values(review);
  
  // Update provider's average rating
  await updateProviderRating(review.providerId);
  
  return result;
}

export async function getProviderReviews(providerId: number) {
  const db = await getDb();
  if (!db) return [];

  const result = await db
    .select()
    .from(reviews)
    .where(eq(reviews.providerId, providerId))
    .orderBy(desc(reviews.createdAt));

  return result;
}

export async function getReviewByBookingId(bookingId: number) {
  const db = await getDb();
  if (!db) return undefined;

  const result = await db.select().from(reviews).where(eq(reviews.bookingId, bookingId)).limit(1);
  return result.length > 0 ? result[0] : undefined;
}

async function updateProviderRating(providerId: number) {
  const db = await getDb();
  if (!db) return;

  const result = await db
    .select({
      avgRating: sql<number>`AVG(${reviews.rating})`,
      totalJobs: sql<number>`COUNT(*)`,
    })
    .from(reviews)
    .where(eq(reviews.providerId, providerId));

  if (result.length > 0 && result[0]) {
    const avgRating = Math.round((result[0].avgRating || 0) * 100); // Store as integer (e.g., 450 = 4.50)
    const totalJobs = result[0].totalJobs || 0;

    await db.update(providerProfiles).set({
      averageRating: avgRating,
      totalJobs: totalJobs,
    }).where(eq(providerProfiles.userId, providerId));
  }
}

// ============================================================================
// MESSAGES
// ============================================================================

export async function createMessage(message: InsertMessage) {
  const db = await getDb();
  if (!db) throw new Error("Database not available");

  const result = await db.insert(messages).values(message);
  return result;
}

export async function getBookingMessages(bookingId: number) {
  const db = await getDb();
  if (!db) return [];

  const result = await db
    .select()
    .from(messages)
    .where(eq(messages.bookingId, bookingId))
    .orderBy(messages.createdAt);

  return result;
}

export async function markMessageAsRead(messageId: number) {
  const db = await getDb();
  if (!db) return false;

  await db.update(messages).set({ 
    isRead: true, 
    readAt: new Date() 
  }).where(eq(messages.id, messageId));
  return true;
}

// ============================================================================
// ADMIN NOTES
// ============================================================================

export async function createAdminNote(note: InsertAdminNote) {
  const db = await getDb();
  if (!db) throw new Error("Database not available");

  const result = await db.insert(adminNotes).values(note);
  return result;
}

export async function getProviderAdminNotes(providerId: number) {
  const db = await getDb();
  if (!db) return [];

  const result = await db
    .select()
    .from(adminNotes)
    .where(eq(adminNotes.providerId, providerId))
    .orderBy(desc(adminNotes.createdAt));

  return result;
}
