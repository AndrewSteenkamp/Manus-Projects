import { z } from "zod";
import { TRPCError } from "@trpc/server";
import { COOKIE_NAME } from "@shared/const";
import { getSessionCookieOptions } from "./_core/cookies";
import { systemRouter } from "./_core/systemRouter";
import { publicProcedure, protectedProcedure, router } from "./_core/trpc";
import * as db from "./db";

// ============================================================================
// HELPER PROCEDURES
// ============================================================================

// Admin-only procedure
const adminProcedure = protectedProcedure.use(({ ctx, next }) => {
  if (ctx.user.role !== 'admin') {
    throw new TRPCError({ code: 'FORBIDDEN', message: 'Admin access required' });
  }
  return next({ ctx });
});

// Provider-only procedure
const providerProcedure = protectedProcedure.use(({ ctx, next }) => {
  if (ctx.user.role !== 'provider') {
    throw new TRPCError({ code: 'FORBIDDEN', message: 'Provider access required' });
  }
  return next({ ctx });
});

// Customer-only procedure
const customerProcedure = protectedProcedure.use(({ ctx, next }) => {
  if (ctx.user.role !== 'customer') {
    throw new TRPCError({ code: 'FORBIDDEN', message: 'Customer access required' });
  }
  return next({ ctx });
});

// ============================================================================
// MAIN ROUTER
// ============================================================================

export const appRouter = router({
  system: systemRouter,
  
  // ============================================================================
  // AUTH ROUTER
  // ============================================================================
  auth: router({
    me: publicProcedure.query(opts => opts.ctx.user),
    
    logout: publicProcedure.mutation(({ ctx }) => {
      const cookieOptions = getSessionCookieOptions(ctx.req);
      ctx.res.clearCookie(COOKIE_NAME, { ...cookieOptions, maxAge: -1 });
      return { success: true } as const;
    }),
    
    // Switch user role (for testing or role upgrade)
    switchRole: protectedProcedure
      .input(z.object({
        role: z.enum(["customer", "provider", "admin"]),
      }))
      .mutation(async ({ ctx, input }) => {
        await db.updateUserRole(ctx.user.id, input.role);
        return { success: true };
      }),
  }),

  // ============================================================================
  // USER PROFILE ROUTER
  // ============================================================================
  profile: router({
    // Get current user's full profile
    get: protectedProcedure.query(async ({ ctx }) => {
      const user = await db.getUserById(ctx.user.id);
      
      if (ctx.user.role === 'provider') {
        const providerProfile = await db.getProviderProfileByUserId(ctx.user.id);
        const services = await db.getProviderServices(ctx.user.id);
        const portfolio = await db.getProviderPortfolio(ctx.user.id);
        
        return {
          user,
          providerProfile,
          services,
          portfolio,
        };
      }
      
      return { user };
    }),
    
    // Update basic user info
    updateBasicInfo: protectedProcedure
      .input(z.object({
        name: z.string().optional(),
        email: z.string().email().optional(),
      }))
      .mutation(async ({ ctx, input }) => {
        // Note: In production, you'd update the users table here
        // For now, this is a placeholder since user info comes from OAuth
        return { success: true };
      }),
  }),

  // ============================================================================
  // PROVIDER ROUTER
  // ============================================================================
  provider: router({
    // Create provider profile (when customer upgrades to provider)
    createProfile: protectedProcedure
      .input(z.object({
        bio: z.string().optional(),
        phone: z.string(),
        address: z.string(),
        city: z.string(),
        province: z.string().optional(),
        postalCode: z.string().optional(),
        qualifications: z.string().optional(), // JSON string
      }))
      .mutation(async ({ ctx, input }) => {
        // Check if profile already exists
        const existing = await db.getProviderProfileByUserId(ctx.user.id);
        if (existing) {
          throw new TRPCError({ code: 'BAD_REQUEST', message: 'Provider profile already exists' });
        }
        
        // Create profile
        await db.createProviderProfile({
          userId: ctx.user.id,
          ...input,
        });
        
        // Update user role to provider
        await db.updateUserRole(ctx.user.id, 'provider');
        
        return { success: true };
      }),
    
    // Update provider profile
    updateProfile: providerProcedure
      .input(z.object({
        bio: z.string().optional(),
        phone: z.string().optional(),
        address: z.string().optional(),
        city: z.string().optional(),
        province: z.string().optional(),
        postalCode: z.string().optional(),
      }))
      .mutation(async ({ ctx, input }) => {
        await db.updateProviderProfile(ctx.user.id, input);
        return { success: true };
      }),
    
    // Get provider profile by ID (public)
    getById: publicProcedure
      .input(z.object({ providerId: z.number() }))
      .query(async ({ input }) => {
        const user = await db.getUserById(input.providerId);
        const profile = await db.getProviderProfileByUserId(input.providerId);
        const services = await db.getProviderServices(input.providerId);
        const portfolio = await db.getProviderPortfolio(input.providerId);
        const reviews = await db.getProviderReviews(input.providerId);
        
        return {
          user,
          profile,
          services,
          portfolio,
          reviews,
        };
      }),
    
    // Add service category
    addService: providerProcedure
      .input(z.object({ categoryId: z.number() }))
      .mutation(async ({ ctx, input }) => {
        const profile = await db.getProviderProfileByUserId(ctx.user.id);
        if (!profile) {
          throw new TRPCError({ code: 'NOT_FOUND', message: 'Provider profile not found' });
        }
        
        await db.addProviderService(profile.id, input.categoryId);
        return { success: true };
      }),
    
    // Remove service category
    removeService: providerProcedure
      .input(z.object({ categoryId: z.number() }))
      .mutation(async ({ ctx, input }) => {
        const profile = await db.getProviderProfileByUserId(ctx.user.id);
        if (!profile) {
          throw new TRPCError({ code: 'NOT_FOUND', message: 'Provider profile not found' });
        }
        
        await db.removeProviderService(profile.id, input.categoryId);
        return { success: true };
      }),
    
    // Add portfolio item
    addPortfolioItem: providerProcedure
      .input(z.object({
        title: z.string().optional(),
        description: z.string().optional(),
        imageUrl: z.string(),
        categoryId: z.number().optional(),
      }))
      .mutation(async ({ ctx, input }) => {
        const profile = await db.getProviderProfileByUserId(ctx.user.id);
        if (!profile) {
          throw new TRPCError({ code: 'NOT_FOUND', message: 'Provider profile not found' });
        }
        
        await db.addPortfolioItem({
          providerId: profile.id,
          ...input,
        });
        return { success: true };
      }),
    
    // Delete portfolio item
    deletePortfolioItem: providerProcedure
      .input(z.object({ itemId: z.number() }))
      .mutation(async ({ ctx, input }) => {
        const profile = await db.getProviderProfileByUserId(ctx.user.id);
        if (!profile) {
          throw new TRPCError({ code: 'NOT_FOUND', message: 'Provider profile not found' });
        }
        
        await db.deletePortfolioItem(input.itemId, profile.id);
        return { success: true };
      }),
  }),

  // ============================================================================
  // SERVICE CATEGORIES ROUTER
  // ============================================================================
  categories: router({
    // Get all active categories
    getAll: publicProcedure.query(async () => {
      return await db.getAllServiceCategories();
    }),
    
    // Get category by ID
    getById: publicProcedure
      .input(z.object({ categoryId: z.number() }))
      .query(async ({ input }) => {
        return await db.getServiceCategoryById(input.categoryId);
      }),
  }),

  // ============================================================================
  // SERVICE REQUESTS ROUTER
  // ============================================================================
  requests: router({
    // Create service request (customer only)
    create: customerProcedure
      .input(z.object({
        categoryId: z.number(),
        title: z.string().min(5),
        description: z.string().min(20),
        address: z.string(),
        city: z.string(),
        province: z.string().optional(),
        postalCode: z.string().optional(),
        latitude: z.string().optional(),
        longitude: z.string().optional(),
        photos: z.string().optional(), // JSON string
        preferredDate: z.date().optional(),
        urgency: z.enum(["low", "medium", "high"]).default("medium"),
      }))
      .mutation(async ({ ctx, input }) => {
        await db.createServiceRequest({
          customerId: ctx.user.id,
          ...input,
        });
        return { success: true };
      }),
    
    // Get customer's own requests
    getMy: customerProcedure.query(async ({ ctx }) => {
      return await db.getCustomerServiceRequests(ctx.user.id);
    }),
    
    // Get all open requests (for providers)
    getOpen: providerProcedure.query(async () => {
      return await db.getOpenServiceRequests();
    }),
    
    // Get request by ID with quotes
    getById: protectedProcedure
      .input(z.object({ requestId: z.number() }))
      .query(async ({ input }) => {
        const request = await db.getServiceRequestById(input.requestId);
        const quotes = await db.getQuotesByRequestId(input.requestId);
        
        return { request, quotes };
      }),
  }),

  // ============================================================================
  // QUOTES ROUTER
  // ============================================================================
  quotes: router({
    // Submit quote (provider only)
    submit: providerProcedure
      .input(z.object({
        requestId: z.number(),
        amount: z.number().min(0), // Amount in cents
        description: z.string().min(20),
        estimatedDuration: z.string().optional(),
        materialsIncluded: z.boolean().default(false),
        materialsCost: z.number().default(0),
        availableFrom: z.date().optional(),
        availableTo: z.date().optional(),
      }))
      .mutation(async ({ ctx, input }) => {
        await db.createQuote({
          providerId: ctx.user.id,
          ...input,
        });
        return { success: true };
      }),
    
    // Get provider's quotes
    getMy: providerProcedure.query(async ({ ctx }) => {
      return await db.getProviderQuotes(ctx.user.id);
    }),
    
    // Accept quote (customer only)
    accept: customerProcedure
      .input(z.object({ quoteId: z.number() }))
      .mutation(async ({ ctx, input }) => {
        const quote = await db.getQuoteById(input.quoteId);
        if (!quote) {
          throw new TRPCError({ code: 'NOT_FOUND', message: 'Quote not found' });
        }
        
        // Get provider profile to determine commission rate
        const providerProfile = await db.getProviderProfileByUserId(quote.providerId);
        if (!providerProfile) {
          throw new TRPCError({ code: 'NOT_FOUND', message: 'Provider profile not found' });
        }
        
        // Calculate commission based on tier
        let commissionRate = 2000; // 20% for probationary
        if (providerProfile.tier === 'verified') commissionRate = 1800; // 18%
        if (providerProfile.tier === 'premium') commissionRate = 1500; // 15%
        
        const commissionAmount = Math.round((quote.amount * commissionRate) / 10000);
        const providerPayout = quote.amount - commissionAmount;
        
        // Create booking
        await db.createBooking({
          requestId: quote.requestId,
          quoteId: input.quoteId,
          customerId: ctx.user.id,
          providerId: quote.providerId,
          amount: quote.amount,
          commissionRate,
          commissionAmount,
          providerPayout,
          status: 'pending',
        });
        
        // Update quote status
        await db.updateQuoteStatus(input.quoteId, 'accepted');
        
        // Update request status
        await db.updateServiceRequestStatus(quote.requestId, 'accepted');
        
        return { success: true };
      }),
    
    // Withdraw quote (provider only)
    withdraw: providerProcedure
      .input(z.object({ quoteId: z.number() }))
      .mutation(async ({ ctx, input }) => {
        const quote = await db.getQuoteById(input.quoteId);
        if (!quote || quote.providerId !== ctx.user.id) {
          throw new TRPCError({ code: 'FORBIDDEN' });
        }
        
        await db.updateQuoteStatus(input.quoteId, 'withdrawn');
        return { success: true };
      }),
  }),

  // ============================================================================
  // BOOKINGS ROUTER
  // ============================================================================
  bookings: router({
    // Get customer's bookings
    getMyCustomer: customerProcedure.query(async ({ ctx }) => {
      return await db.getCustomerBookings(ctx.user.id);
    }),
    
    // Get provider's bookings
    getMyProvider: providerProcedure.query(async ({ ctx }) => {
      return await db.getProviderBookings(ctx.user.id);
    }),
    
    // Get booking by ID
    getById: protectedProcedure
      .input(z.object({ bookingId: z.number() }))
      .query(async ({ ctx, input }) => {
        const booking = await db.getBookingById(input.bookingId);
        if (!booking) {
          throw new TRPCError({ code: 'NOT_FOUND' });
        }
        
        // Check access
        if (booking.customerId !== ctx.user.id && booking.providerId !== ctx.user.id && ctx.user.role !== 'admin') {
          throw new TRPCError({ code: 'FORBIDDEN' });
        }
        
        const messages = await db.getBookingMessages(input.bookingId);
        return { booking, messages };
      }),
    
    // Update booking status
    updateStatus: protectedProcedure
      .input(z.object({
        bookingId: z.number(),
        status: z.enum(["pending", "confirmed", "in_progress", "completed", "cancelled"]),
      }))
      .mutation(async ({ ctx, input }) => {
        const booking = await db.getBookingById(input.bookingId);
        if (!booking) {
          throw new TRPCError({ code: 'NOT_FOUND' });
        }
        
        // Check permissions
        const isCustomer = booking.customerId === ctx.user.id;
        const isProvider = booking.providerId === ctx.user.id;
        
        if (!isCustomer && !isProvider && ctx.user.role !== 'admin') {
          throw new TRPCError({ code: 'FORBIDDEN' });
        }
        
        await db.updateBookingStatus(input.bookingId, input.status);
        
        // If completed, release payment from escrow
        if (input.status === 'completed') {
          const payment = await db.getPaymentByBookingId(input.bookingId);
          if (payment) {
            await db.releasePaymentFromEscrow(payment.id);
          }
        }
        
        return { success: true };
      }),
  }),

  // ============================================================================
  // MESSAGES ROUTER
  // ============================================================================
  messages: router({
    // Send message
    send: protectedProcedure
      .input(z.object({
        bookingId: z.number(),
        content: z.string().min(1),
        attachments: z.string().optional(), // JSON string
      }))
      .mutation(async ({ ctx, input }) => {
        const booking = await db.getBookingById(input.bookingId);
        if (!booking) {
          throw new TRPCError({ code: 'NOT_FOUND' });
        }
        
        // Determine receiver
        const receiverId = booking.customerId === ctx.user.id ? booking.providerId : booking.customerId;
        
        await db.createMessage({
          bookingId: input.bookingId,
          senderId: ctx.user.id,
          receiverId,
          content: input.content,
          attachments: input.attachments,
        });
        
        return { success: true };
      }),
    
    // Get messages for a booking
    getByBooking: protectedProcedure
      .input(z.object({ bookingId: z.number() }))
      .query(async ({ ctx, input }) => {
        const booking = await db.getBookingById(input.bookingId);
        if (!booking) {
          throw new TRPCError({ code: 'NOT_FOUND' });
        }
        
        // Check access
        if (booking.customerId !== ctx.user.id && booking.providerId !== ctx.user.id) {
          throw new TRPCError({ code: 'FORBIDDEN' });
        }
        
        return await db.getBookingMessages(input.bookingId);
      }),
    
    // Mark message as read
    markRead: protectedProcedure
      .input(z.object({ messageId: z.number() }))
      .mutation(async ({ input }) => {
        await db.markMessageAsRead(input.messageId);
        return { success: true };
      }),
  }),

  // ============================================================================
  // REVIEWS ROUTER
  // ============================================================================
  reviews: router({
    // Submit review (customer only, after booking completed)
    submit: customerProcedure
      .input(z.object({
        bookingId: z.number(),
        rating: z.number().min(1).max(5),
        title: z.string().optional(),
        comment: z.string().optional(),
      }))
      .mutation(async ({ ctx, input }) => {
        const booking = await db.getBookingById(input.bookingId);
        if (!booking) {
          throw new TRPCError({ code: 'NOT_FOUND' });
        }
        
        if (booking.customerId !== ctx.user.id) {
          throw new TRPCError({ code: 'FORBIDDEN' });
        }
        
        if (booking.status !== 'completed') {
          throw new TRPCError({ code: 'BAD_REQUEST', message: 'Can only review completed bookings' });
        }
        
        // Check if review already exists
        const existing = await db.getReviewByBookingId(input.bookingId);
        if (existing) {
          throw new TRPCError({ code: 'BAD_REQUEST', message: 'Review already submitted' });
        }
        
        await db.createReview({
          bookingId: input.bookingId,
          customerId: ctx.user.id,
          providerId: booking.providerId,
          rating: input.rating,
          title: input.title,
          comment: input.comment,
        });
        
        return { success: true };
      }),
    
    // Get provider reviews
    getByProvider: publicProcedure
      .input(z.object({ providerId: z.number() }))
      .query(async ({ input }) => {
        return await db.getProviderReviews(input.providerId);
      }),
  }),

  // ============================================================================
  // ADMIN ROUTER
  // ============================================================================
  admin: router({
    // Get pending provider applications
    getPendingProviders: adminProcedure.query(async () => {
      return await db.getPendingProviderApplications();
    }),
    
    // Approve provider
    approveProvider: adminProcedure
      .input(z.object({ providerId: z.number() }))
      .mutation(async ({ input }) => {
        await db.updateProviderProfile(input.providerId, {
          verificationStatus: 'approved',
          verifiedAt: new Date(),
        });
        return { success: true };
      }),
    
    // Reject provider
    rejectProvider: adminProcedure
      .input(z.object({ providerId: z.number(), reason: z.string() }))
      .mutation(async ({ input }) => {
        await db.updateProviderProfile(input.providerId, {
          verificationStatus: 'rejected',
        });
        return { success: true };
      }),
    
    // Update provider tier
    updateProviderTier: adminProcedure
      .input(z.object({
        providerId: z.number(),
        tier: z.enum(["probationary", "verified", "premium"]),
      }))
      .mutation(async ({ ctx, input }) => {
        await db.updateProviderTier(input.providerId, input.tier);
        
        // Add admin note
        await db.createAdminNote({
          providerId: input.providerId,
          adminId: ctx.user.id,
          note: `Tier updated to ${input.tier}`,
          noteType: 'tier_change',
        });
        
        return { success: true };
      }),
    
    // Add admin note
    addNote: adminProcedure
      .input(z.object({
        providerId: z.number(),
        note: z.string(),
        noteType: z.enum(["general", "background_check", "qualification", "tier_change"]),
      }))
      .mutation(async ({ ctx, input }) => {
        await db.createAdminNote({
          providerId: input.providerId,
          adminId: ctx.user.id,
          note: input.note,
          noteType: input.noteType,
        });
        return { success: true };
      }),
    
    // Get provider admin notes
    getProviderNotes: adminProcedure
      .input(z.object({ providerId: z.number() }))
      .query(async ({ input }) => {
        return await db.getProviderAdminNotes(input.providerId);
      }),
  }),
});

export type AppRouter = typeof appRouter;
