import { int, mysqlEnum, mysqlTable, text, timestamp, varchar, boolean, decimal } from "drizzle-orm/mysql-core";
import { relations } from "drizzle-orm";

/**
 * Core user table backing auth flow.
 * Extended with provider-specific fields and three-tier role system.
 */
export const users = mysqlTable("users", {
  id: int("id").autoincrement().primaryKey(),
  openId: varchar("openId", { length: 64 }).notNull().unique(),
  name: text("name"),
  email: varchar("email", { length: 320 }),
  loginMethod: varchar("loginMethod", { length: 64 }),
  role: mysqlEnum("role", ["customer", "provider", "admin"]).default("customer").notNull(),
  createdAt: timestamp("createdAt").defaultNow().notNull(),
  updatedAt: timestamp("updatedAt").defaultNow().onUpdateNow().notNull(),
  lastSignedIn: timestamp("lastSignedIn").defaultNow().notNull(),
});

/**
 * Provider profiles with verification and tier information
 */
export const providerProfiles = mysqlTable("provider_profiles", {
  id: int("id").autoincrement().primaryKey(),
  userId: int("user_id").notNull(),
  bio: text("bio"),
  phone: varchar("phone", { length: 20 }),
  address: text("address"),
  city: varchar("city", { length: 100 }),
  province: varchar("province", { length: 100 }),
  postalCode: varchar("postal_code", { length: 10 }),
  
  // Verification status
  verificationStatus: mysqlEnum("verification_status", ["pending", "approved", "rejected"]).default("pending").notNull(),
  verifiedAt: timestamp("verified_at"),
  
  // Background checks
  backgroundCheckStatus: mysqlEnum("background_check_status", ["not_started", "in_progress", "completed", "failed"]).default("not_started").notNull(),
  backgroundCheckDate: timestamp("background_check_date"),
  backgroundCheckNotes: text("background_check_notes"),
  
  // Qualifications
  qualifications: text("qualifications"), // JSON array of qualification documents
  insuranceVerified: boolean("insurance_verified").default(false).notNull(),
  insuranceExpiryDate: timestamp("insurance_expiry_date"),
  
  // Provider tier system: Probationary (20%), Verified (18%), Premium (15%)
  tier: mysqlEnum("tier", ["probationary", "verified", "premium"]).default("probationary").notNull(),
  
  // Stats for tier calculation
  totalJobs: int("total_jobs").default(0).notNull(),
  averageRating: int("average_rating").default(0).notNull(), // Store as integer (e.g., 450 = 4.50 stars) to avoid decimal issues
  
  createdAt: timestamp("created_at").defaultNow().notNull(),
  updatedAt: timestamp("updated_at").defaultNow().onUpdateNow().notNull(),
});

/**
 * Service categories (plumbing, electrical, handyman, HVAC, solar, etc.)
 */
export const serviceCategories = mysqlTable("service_categories", {
  id: int("id").autoincrement().primaryKey(),
  name: varchar("name", { length: 100 }).notNull(),
  description: text("description"),
  icon: varchar("icon", { length: 50 }), // Icon name for UI
  active: boolean("active").default(true).notNull(),
  createdAt: timestamp("created_at").defaultNow().notNull(),
});

/**
 * Provider service offerings (many-to-many relationship)
 */
export const providerServices = mysqlTable("provider_services", {
  id: int("id").autoincrement().primaryKey(),
  providerId: int("provider_id").notNull(),
  categoryId: int("category_id").notNull(),
  createdAt: timestamp("created_at").defaultNow().notNull(),
});

/**
 * Provider portfolio items (photos of previous work)
 */
export const portfolioItems = mysqlTable("portfolio_items", {
  id: int("id").autoincrement().primaryKey(),
  providerId: int("provider_id").notNull(),
  title: varchar("title", { length: 200 }),
  description: text("description"),
  imageUrl: text("image_url").notNull(),
  categoryId: int("category_id"),
  createdAt: timestamp("created_at").defaultNow().notNull(),
});

/**
 * Service requests posted by customers
 */
export const serviceRequests = mysqlTable("service_requests", {
  id: int("id").autoincrement().primaryKey(),
  customerId: int("customer_id").notNull(),
  categoryId: int("category_id").notNull(),
  
  title: varchar("title", { length: 200 }).notNull(),
  description: text("description").notNull(),
  
  // Location details
  address: text("address").notNull(),
  city: varchar("city", { length: 100 }).notNull(),
  province: varchar("province", { length: 100 }),
  postalCode: varchar("postal_code", { length: 10 }),
  latitude: varchar("latitude", { length: 20 }),
  longitude: varchar("longitude", { length: 20 }),
  
  // Photos
  photos: text("photos"), // JSON array of photo URLs
  
  // Status
  status: mysqlEnum("status", ["open", "quoted", "accepted", "closed"]).default("open").notNull(),
  
  // Preferred timing
  preferredDate: timestamp("preferred_date"),
  urgency: mysqlEnum("urgency", ["low", "medium", "high"]).default("medium").notNull(),
  
  createdAt: timestamp("created_at").defaultNow().notNull(),
  updatedAt: timestamp("updated_at").defaultNow().onUpdateNow().notNull(),
});

/**
 * Quotes submitted by providers for service requests
 */
export const quotes = mysqlTable("quotes", {
  id: int("id").autoincrement().primaryKey(),
  requestId: int("request_id").notNull(),
  providerId: int("provider_id").notNull(),
  
  // Quote details
  amount: int("amount").notNull(), // Store in cents (e.g., R800.00 = 80000)
  description: text("description").notNull(),
  estimatedDuration: varchar("estimated_duration", { length: 100 }), // e.g., "2-3 hours"
  
  // Materials
  materialsIncluded: boolean("materials_included").default(false).notNull(),
  materialsCost: int("materials_cost").default(0).notNull(), // In cents
  
  // Availability
  availableFrom: timestamp("available_from"),
  availableTo: timestamp("available_to"),
  
  // Status
  status: mysqlEnum("status", ["pending", "accepted", "rejected", "withdrawn"]).default("pending").notNull(),
  
  createdAt: timestamp("created_at").defaultNow().notNull(),
  updatedAt: timestamp("updated_at").defaultNow().onUpdateNow().notNull(),
});

/**
 * Bookings created when a customer accepts a quote
 */
export const bookings = mysqlTable("bookings", {
  id: int("id").autoincrement().primaryKey(),
  requestId: int("request_id").notNull(),
  quoteId: int("quote_id").notNull(),
  customerId: int("customer_id").notNull(),
  providerId: int("provider_id").notNull(),
  
  // Booking details
  amount: int("amount").notNull(), // Total amount in cents
  commissionRate: int("commission_rate").notNull(), // Commission percentage * 100 (e.g., 1500 = 15%)
  commissionAmount: int("commission_amount").notNull(), // Commission in cents
  providerPayout: int("provider_payout").notNull(), // Amount provider receives in cents
  
  // Status workflow: pending → confirmed → in-progress → completed
  status: mysqlEnum("status", ["pending", "confirmed", "in_progress", "completed", "cancelled"]).default("pending").notNull(),
  
  // Timestamps for status changes
  confirmedAt: timestamp("confirmed_at"),
  startedAt: timestamp("started_at"),
  completedAt: timestamp("completed_at"),
  cancelledAt: timestamp("cancelled_at"),
  
  // Scheduled date
  scheduledDate: timestamp("scheduled_date"),
  
  createdAt: timestamp("created_at").defaultNow().notNull(),
  updatedAt: timestamp("updated_at").defaultNow().onUpdateNow().notNull(),
});

/**
 * Payments and transactions
 */
export const payments = mysqlTable("payments", {
  id: int("id").autoincrement().primaryKey(),
  bookingId: int("booking_id").notNull(),
  
  // Payment details
  amount: int("amount").notNull(), // In cents
  status: mysqlEnum("status", ["pending", "processing", "completed", "failed", "refunded"]).default("pending").notNull(),
  
  // PayFast details
  paymentId: varchar("payment_id", { length: 100 }), // PayFast payment ID
  paymentMethod: varchar("payment_method", { length: 50 }),
  
  // Escrow
  heldInEscrow: boolean("held_in_escrow").default(true).notNull(),
  releasedAt: timestamp("released_at"),
  
  // Metadata
  metadata: text("metadata"), // JSON for additional PayFast data
  
  createdAt: timestamp("created_at").defaultNow().notNull(),
  updatedAt: timestamp("updated_at").defaultNow().onUpdateNow().notNull(),
});

/**
 * Reviews and ratings for completed bookings
 */
export const reviews = mysqlTable("reviews", {
  id: int("id").autoincrement().primaryKey(),
  bookingId: int("booking_id").notNull(),
  customerId: int("customer_id").notNull(),
  providerId: int("provider_id").notNull(),
  
  // Rating (1-5 stars, stored as integer 1-5)
  rating: int("rating").notNull(),
  
  // Review content
  title: varchar("title", { length: 200 }),
  comment: text("comment"),
  
  // Provider response
  providerResponse: text("provider_response"),
  providerRespondedAt: timestamp("provider_responded_at"),
  
  // Moderation
  flagged: boolean("flagged").default(false).notNull(),
  flaggedReason: text("flagged_reason"),
  moderatedBy: int("moderated_by"),
  moderatedAt: timestamp("moderated_at"),
  
  createdAt: timestamp("created_at").defaultNow().notNull(),
  updatedAt: timestamp("updated_at").defaultNow().onUpdateNow().notNull(),
});

/**
 * In-app messages between customers and providers for specific bookings
 */
export const messages = mysqlTable("messages", {
  id: int("id").autoincrement().primaryKey(),
  bookingId: int("booking_id").notNull(),
  senderId: int("sender_id").notNull(),
  receiverId: int("receiver_id").notNull(),
  
  content: text("content").notNull(),
  
  // Read status
  isRead: boolean("is_read").default(false).notNull(),
  readAt: timestamp("read_at"),
  
  // Attachments
  attachments: text("attachments"), // JSON array of attachment URLs
  
  createdAt: timestamp("created_at").defaultNow().notNull(),
});

/**
 * Admin notes for provider vetting
 */
export const adminNotes = mysqlTable("admin_notes", {
  id: int("id").autoincrement().primaryKey(),
  providerId: int("provider_id").notNull(),
  adminId: int("admin_id").notNull(),
  
  note: text("note").notNull(),
  noteType: mysqlEnum("note_type", ["general", "background_check", "qualification", "tier_change"]).default("general").notNull(),
  
  createdAt: timestamp("created_at").defaultNow().notNull(),
});

// Type exports
export type User = typeof users.$inferSelect;
export type InsertUser = typeof users.$inferInsert;

export type ProviderProfile = typeof providerProfiles.$inferSelect;
export type InsertProviderProfile = typeof providerProfiles.$inferInsert;

export type ServiceCategory = typeof serviceCategories.$inferSelect;
export type InsertServiceCategory = typeof serviceCategories.$inferInsert;

export type ProviderService = typeof providerServices.$inferSelect;
export type InsertProviderService = typeof providerServices.$inferInsert;

export type PortfolioItem = typeof portfolioItems.$inferSelect;
export type InsertPortfolioItem = typeof portfolioItems.$inferInsert;

export type ServiceRequest = typeof serviceRequests.$inferSelect;
export type InsertServiceRequest = typeof serviceRequests.$inferInsert;

export type Quote = typeof quotes.$inferSelect;
export type InsertQuote = typeof quotes.$inferInsert;

export type Booking = typeof bookings.$inferSelect;
export type InsertBooking = typeof bookings.$inferInsert;

export type Payment = typeof payments.$inferSelect;
export type InsertPayment = typeof payments.$inferInsert;

export type Review = typeof reviews.$inferSelect;
export type InsertReview = typeof reviews.$inferInsert;

export type Message = typeof messages.$inferSelect;
export type InsertMessage = typeof messages.$inferInsert;

export type AdminNote = typeof adminNotes.$inferSelect;
export type InsertAdminNote = typeof adminNotes.$inferInsert;
