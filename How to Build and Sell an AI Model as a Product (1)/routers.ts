import { z } from "zod";
import { COOKIE_NAME } from "@shared/const";
import { getSessionCookieOptions } from "./_core/cookies";
import { systemRouter } from "./_core/systemRouter";
import { publicProcedure, protectedProcedure, router } from "./_core/trpc";
import * as db from "./db";
import { getMarketOverview, fetchStockQuote, getStockHistory, JSE_STOCKS } from "./marketData";
import { 
  createYocoPayment, 
  calculateSubscriptionPrice, 
  generatePaymentMetadata,
  processYocoWebhook
} from "./yocoPayments.js";
import { generateWeeklyNewsletter, getUserNewsletters } from "./newsletter";

export const appRouter = router({
  system: systemRouter,
  
  auth: router({
    me: publicProcedure.query(opts => opts.ctx.user),
    logout: publicProcedure.mutation(({ ctx }) => {
      const cookieOptions = getSessionCookieOptions(ctx.req);
      ctx.res.clearCookie(COOKIE_NAME, { ...cookieOptions, maxAge: -1 });
      return { success: true } as const;
    }),
  }),

  // ============= NEWSLETTERS =============
  newsletters: router({
    list: protectedProcedure.query(async ({ ctx }) => {
      return await getUserNewsletters(ctx.user.id);
    }),

    generate: protectedProcedure.mutation(async ({ ctx }) => {
      const newsletter = await generateWeeklyNewsletter();
      // Save to current user
      await db.saveNewsletterRecord({
        userId: ctx.user.id,
        subject: newsletter.subject,
        content: newsletter.htmlContent,
        sentAt: newsletter.generatedAt,
      });
      return { success: true, subject: newsletter.subject };
    }),
  }),

  // ============= MARKET DATA =============
  market: router({
    overview: publicProcedure.query(async () => {
      const overview = await getMarketOverview();
      
      // Cache the data in database
      for (const quote of overview.quotes) {
        await db.upsertMarketDataCache({
          stockSymbol: quote.symbol,
          currentPrice: quote.currentPrice.toString(),
          priceChange: quote.priceChange.toString(),
          priceChangePercent: quote.priceChangePercent.toString(),
          volume: quote.volume,
          marketCap: quote.marketCap,
          sector: quote.sector,
          ecmConfidence: overview.ecm.confidence.toString(),
          marketDirection: overview.ecm.direction,
          supportLevel: overview.ecm.supportLevel.toString(),
          resistanceLevel: overview.ecm.resistanceLevel.toString(),
        });
      }
      
      return overview;
    }),

    stockQuote: publicProcedure
      .input(z.object({ symbol: z.string() }))
      .query(async ({ input }) => {
        return await fetchStockQuote(input.symbol);
      }),

    stockHistory: publicProcedure
      .input(z.object({ 
        symbol: z.string(),
        range: z.enum(["1d", "5d", "1mo", "3mo", "6mo", "1y"]).default("1mo")
      }))
      .query(async ({ input }) => {
        return await getStockHistory(input.symbol, input.range);
      }),

    jseStocks: publicProcedure.query(() => {
      return JSE_STOCKS;
    }),

    cachedData: publicProcedure.query(async () => {
      return await db.getAllMarketDataCache();
    }),
  }),

  // ============= SUBSCRIPTION PLANS =============
  plans: router({
    list: publicProcedure.query(async () => {
      return await db.getAllSubscriptionPlans();
    }),

    get: publicProcedure
      .input(z.object({ id: z.number() }))
      .query(async ({ input }) => {
        return await db.getSubscriptionPlanById(input.id);
      }),
  }),

  // ============= USER SUBSCRIPTIONS =============
  subscriptions: router({
    current: protectedProcedure.query(async ({ ctx }) => {
      return await db.getUserActiveSubscription(ctx.user.id);
    }),

    history: protectedProcedure.query(async ({ ctx }) => {
      return await db.getUserSubscriptionHistory(ctx.user.id);
    }),

    create: protectedProcedure
      .input(z.object({
        planId: z.number(),
        origin: z.string(),
      }))
      .mutation(async ({ input, ctx }) => {
        const plan = await db.getSubscriptionPlanById(input.planId);
        if (!plan) {
          throw new Error("Subscription plan not found");
        }

        // Get Yoco API key from environment
        const yocoApiKey = process.env.YOCO_SECRET_KEY;
        if (!yocoApiKey) {
          throw new Error("Yoco API key not configured");
        }

        // Create Yoco payment
        const amountCents = calculateSubscriptionPrice(parseFloat(plan.priceRands));
        const metadata = generatePaymentMetadata(ctx.user.id, plan.id, plan.name);

        const payment = await createYocoPayment(
          {
            amount: amountCents,
            currency: "ZAR",
            description: `Siener AI - ${plan.name} Subscription`,
            metadata,
            successUrl: `${input.origin}/subscription/success`,
            cancelUrl: `${input.origin}/subscription/cancel`,
            failureUrl: `${input.origin}/subscription/failure`,
          },
          yocoApiKey
        );

        if (!payment) {
          throw new Error("Failed to create payment");
        }

        // Create pending subscription
        const startDate = new Date();
        const endDate = new Date();
        endDate.setMonth(endDate.getMonth() + 1); // 1 month subscription

        await db.createUserSubscription({
          userId: ctx.user.id,
          planId: plan.id,
          status: "pending",
          startDate,
          endDate,
          yocoPaymentId: payment.id,
        });

        // Create payment transaction record
        await db.createPaymentTransaction({
          userId: ctx.user.id,
          yocoPaymentId: payment.id,
          amountRands: plan.priceRands,
          currency: "ZAR",
          status: "pending",
          metadata: JSON.stringify(metadata),
        });

        return {
          success: true,
          paymentId: payment.id,
          redirectUrl: payment.redirectUrl,
        };
      }),

    cancel: protectedProcedure
      .input(z.object({ subscriptionId: z.number() }))
      .mutation(async ({ input, ctx }) => {
        const subscription = await db.getUserActiveSubscription(ctx.user.id);
        
        if (!subscription || subscription.id !== input.subscriptionId) {
          throw new Error("Subscription not found or not active");
        }

        await db.updateSubscriptionStatus(input.subscriptionId, "cancelled");
        
        return { success: true };
      }),
  }),

  // ============= PAYMENTS =============
  payments: router({
    history: protectedProcedure.query(async ({ ctx }) => {
      return await db.getUserPaymentHistory(ctx.user.id);
    }),

    createPayment: protectedProcedure
      .input(z.object({
        planId: z.number(),
        amount: z.number(),
      }))
      .mutation(async ({ input, ctx }) => {
        // Create subscription first
        const now = new Date();
        const endDate = new Date(now);
        endDate.setMonth(endDate.getMonth() + 1); // 1 month subscription
        
        const subscription = await db.createUserSubscription({
          userId: ctx.user.id,
          planId: input.planId,
          status: "pending",
          startDate: now,
          endDate: endDate,
        });

        // TODO: Integrate Yoco payment gateway
        // For now, redirect to dashboard after creating subscription
        const checkoutUrl = `/dashboard?subscribed=true`;

        return { checkoutUrl, subscriptionId: subscription.id };
      }),

    webhook: publicProcedure
      .input(z.object({
        payload: z.any(),
        signature: z.string(),
      }))
      .mutation(async ({ input }) => {
        // Process Yoco webhook
        const result = processYocoWebhook(input.payload);
        
        // Update payment transaction
        const transaction = await db.getPaymentTransactionByYocoId(result.paymentId);
        if (transaction) {
          await db.updatePaymentStatus(transaction.id, result.status);
          
          // If payment completed, activate subscription
          if (result.status === "completed" && transaction.subscriptionId) {
            await db.updateSubscriptionStatus(transaction.subscriptionId, "active");
          }
        }

        return { success: true };
      }),
  }),

  // ============= WATCHLIST =============
  watchlist: router({
    list: protectedProcedure.query(async ({ ctx }) => {
      return await db.getUserWatchlist(ctx.user.id);
    }),

    add: protectedProcedure
      .input(z.object({
        stockSymbol: z.string(),
        stockName: z.string(),
        notes: z.string().optional(),
      }))
      .mutation(async ({ input, ctx }) => {
        await db.addToWatchlist({
          userId: ctx.user.id,
          stockSymbol: input.stockSymbol,
          stockName: input.stockName,
          notes: input.notes,
        });
        return { success: true };
      }),

    remove: protectedProcedure
      .input(z.object({ id: z.number() }))
      .mutation(async ({ input }) => {
        await db.removeFromWatchlist(input.id);
        return { success: true };
      }),
  }),

  // ============= MARKETING (for autonomous agent) =============
  marketing: router({
    content: router({
      list: publicProcedure.query(async () => {
        return await db.getAllMarketingContent();
      }),

      create: protectedProcedure
        .input(z.object({
          contentType: z.enum(["social_post", "blog", "email", "ad_copy"]),
          platform: z.string().optional(),
          title: z.string().optional(),
          content: z.string(),
          imageUrl: z.string().optional(),
          scheduledFor: z.date().optional(),
        }))
        .mutation(async ({ input }) => {
          await db.createMarketingContent({
            ...input,
            status: input.scheduledFor ? "scheduled" : "draft",
          });
          return { success: true };
        }),

      updateStatus: protectedProcedure
        .input(z.object({
          id: z.number(),
          status: z.enum(["draft", "scheduled", "published", "archived"]),
        }))
        .mutation(async ({ input }) => {
          await db.updateMarketingContentStatus(
            input.id, 
            input.status,
            input.status === "published" ? new Date() : undefined
          );
          return { success: true };
        }),
    }),

    campaigns: router({
      list: publicProcedure.query(async () => {
        return await db.getAllMarketingCampaigns();
      }),

      active: publicProcedure.query(async () => {
        return await db.getActiveCampaigns();
      }),

      create: protectedProcedure
        .input(z.object({
          name: z.string(),
          description: z.string().optional(),
          campaignType: z.enum(["awareness", "acquisition", "retention", "conversion"]),
          budget: z.string().optional(),
          startDate: z.date().optional(),
          endDate: z.date().optional(),
          targetAudience: z.string().optional(),
        }))
        .mutation(async ({ input }) => {
          await db.createMarketingCampaign({
            ...input,
            status: "planning",
          });
          return { success: true };
        }),
    }),
  }),
});

export type AppRouter = typeof appRouter;
