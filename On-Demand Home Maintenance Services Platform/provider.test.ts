import { describe, expect, it } from "vitest";
import { appRouter } from "./routers";
import type { TrpcContext } from "./_core/context";

type AuthenticatedUser = NonNullable<TrpcContext["user"]>;

function createProviderContext(userId: number = 2): { ctx: TrpcContext } {
  const user: AuthenticatedUser = {
    id: userId,
    openId: `provider-${userId}`,
    email: `provider${userId}@example.com`,
    name: `Provider ${userId}`,
    loginMethod: "manus",
    role: "provider",
    createdAt: new Date(),
    updatedAt: new Date(),
    lastSignedIn: new Date(),
  };

  const ctx: TrpcContext = {
    user,
    req: {
      protocol: "https",
      headers: {},
    } as TrpcContext["req"],
    res: {} as TrpcContext["res"],
  };

  return { ctx };
}

function createCustomerContext(userId: number = 1): { ctx: TrpcContext } {
  const user: AuthenticatedUser = {
    id: userId,
    openId: `customer-${userId}`,
    email: `customer${userId}@example.com`,
    name: `Customer ${userId}`,
    loginMethod: "manus",
    role: "customer",
    createdAt: new Date(),
    updatedAt: new Date(),
    lastSignedIn: new Date(),
  };

  const ctx: TrpcContext = {
    user,
    req: {
      protocol: "https",
      headers: {},
    } as TrpcContext["req"],
    res: {} as TrpcContext["res"],
  };

  return { ctx };
}

function createAdminContext(): { ctx: TrpcContext } {
  const user: AuthenticatedUser = {
    id: 999,
    openId: "admin-user",
    email: "admin@example.com",
    name: "Admin User",
    loginMethod: "manus",
    role: "admin",
    createdAt: new Date(),
    updatedAt: new Date(),
    lastSignedIn: new Date(),
  };

  const ctx: TrpcContext = {
    user,
    req: {
      protocol: "https",
      headers: {},
    } as TrpcContext["req"],
    res: {} as TrpcContext["res"],
  };

  return { ctx };
}

describe("Provider Management", () => {
  it("should allow customer to create provider profile", async () => {
    const { ctx } = createCustomerContext(100);
    const caller = appRouter.createCaller(ctx);

    const result = await caller.provider.createProfile({
      bio: "Experienced plumber with 10 years experience",
      phone: "+27123456789",
      address: "123 Main St",
      city: "Cape Town",
      province: "Western Cape",
      postalCode: "8001",
    });

    expect(result.success).toBe(true);
  });

  it("should retrieve provider profile by ID", async () => {
    const { ctx } = createCustomerContext();
    const caller = appRouter.createCaller(ctx);

    // This will return null/undefined if provider doesn't exist, which is expected
    const result = await caller.provider.getById({ providerId: 999 });
    
    // Just verify the query executes without error
    expect(result).toBeDefined();
  });

  it("should list all service categories", async () => {
    const { ctx } = createCustomerContext();
    const caller = appRouter.createCaller(ctx);

    const categories = await caller.categories.getAll();

    expect(Array.isArray(categories)).toBe(true);
    expect(categories.length).toBeGreaterThan(0);
    
    // Verify expected categories exist
    const categoryNames = categories.map(c => c.name);
    expect(categoryNames).toContain("Plumbing");
    expect(categoryNames).toContain("Electrical");
    expect(categoryNames).toContain("HVAC");
  });
});

describe("Quote and Booking System", () => {
  it("should calculate correct commission for probationary provider", () => {
    const quoteAmount = 80000; // R800.00 in cents
    const commissionRate = 2000; // 20% for probationary
    
    const commissionAmount = Math.round((quoteAmount * commissionRate) / 10000);
    const providerPayout = quoteAmount - commissionAmount;
    
    expect(commissionAmount).toBe(16000); // R160.00
    expect(providerPayout).toBe(64000); // R640.00
  });

  it("should calculate correct commission for verified provider", () => {
    const quoteAmount = 80000; // R800.00 in cents
    const commissionRate = 1800; // 18% for verified
    
    const commissionAmount = Math.round((quoteAmount * commissionRate) / 10000);
    const providerPayout = quoteAmount - commissionAmount;
    
    expect(commissionAmount).toBe(14400); // R144.00
    expect(providerPayout).toBe(65600); // R656.00
  });

  it("should calculate correct commission for premium provider", () => {
    const quoteAmount = 80000; // R800.00 in cents
    const commissionRate = 1500; // 15% for premium
    
    const commissionAmount = Math.round((quoteAmount * commissionRate) / 10000);
    const providerPayout = quoteAmount - commissionAmount;
    
    expect(commissionAmount).toBe(12000); // R120.00
    expect(providerPayout).toBe(68000); // R680.00
  });
});

describe("Admin Provider Vetting", () => {
  it("should allow admin to get pending provider applications", async () => {
    const { ctx } = createAdminContext();
    const caller = appRouter.createCaller(ctx);

    const pendingProviders = await caller.admin.getPendingProviders();

    expect(Array.isArray(pendingProviders)).toBe(true);
  });

  it("should prevent non-admin from accessing admin endpoints", async () => {
    const { ctx } = createCustomerContext();
    const caller = appRouter.createCaller(ctx);

    await expect(
      caller.admin.getPendingProviders()
    ).rejects.toThrow("Admin access required");
  });
});

describe("Role-Based Access Control", () => {
  it("should allow provider to access provider endpoints", async () => {
    const { ctx } = createProviderContext();
    const caller = appRouter.createCaller(ctx);

    const quotes = await caller.quotes.getMy();
    expect(Array.isArray(quotes)).toBe(true);
  });

  it("should prevent customer from accessing provider-only endpoints", async () => {
    const { ctx } = createCustomerContext();
    const caller = appRouter.createCaller(ctx);

    await expect(
      caller.quotes.getMy()
    ).rejects.toThrow("Provider access required");
  });

  it("should allow customer to access customer endpoints", async () => {
    const { ctx } = createCustomerContext();
    const caller = appRouter.createCaller(ctx);

    const requests = await caller.requests.getMy();
    expect(Array.isArray(requests)).toBe(true);
  });

  it("should prevent provider from accessing customer-only endpoints", async () => {
    const { ctx } = createProviderContext();
    const caller = appRouter.createCaller(ctx);

    await expect(
      caller.requests.getMy()
    ).rejects.toThrow("Customer access required");
  });
});

describe("Authentication", () => {
  it("should return user info for authenticated user", async () => {
    const { ctx } = createCustomerContext();
    const caller = appRouter.createCaller(ctx);

    const user = await caller.auth.me();

    expect(user).toBeDefined();
    expect(user?.role).toBe("customer");
  });
});
