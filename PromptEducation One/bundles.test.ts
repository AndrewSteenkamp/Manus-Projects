import { describe, expect, it } from "vitest";
import { appRouter } from "./routers";
import type { TrpcContext } from "./_core/context";

type AuthenticatedUser = NonNullable<TrpcContext["user"]>;

function createAdminContext(): { ctx: TrpcContext } {
  const user: AuthenticatedUser = {
    id: 1,
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
    res: {
      clearCookie: () => {},
    } as TrpcContext["res"],
  };

  return { ctx };
}

describe("bundles router", () => {
  it("should list all published bundles", async () => {
    const { ctx } = createAdminContext();
    const caller = appRouter.createCaller(ctx);

    const bundles = await caller.bundles.list();

    expect(Array.isArray(bundles)).toBe(true);
    expect(bundles.length).toBeGreaterThan(0);
    
    // Check that bundles have required fields
    if (bundles.length > 0) {
      const bundle = bundles[0];
      expect(bundle).toHaveProperty("id");
      expect(bundle).toHaveProperty("title");
      expect(bundle).toHaveProperty("slug");
      expect(bundle).toHaveProperty("price");
      expect(bundle).toHaveProperty("originalPrice");
      expect(bundle).toHaveProperty("discountPercent");
    }
  });

  it("should get bundle by slug", async () => {
    const { ctx } = createAdminContext();
    const caller = appRouter.createCaller(ctx);

    // First get all bundles to find a valid slug
    const bundles = await caller.bundles.list();
    
    if (bundles.length > 0) {
      const slug = bundles[0]!.slug;
      const bundle = await caller.bundles.getBySlug({ slug });

      expect(bundle).toBeDefined();
      expect(bundle.slug).toBe(slug);
    }
  });

  it("should get bundle courses", async () => {
    const { ctx } = createAdminContext();
    const caller = appRouter.createCaller(ctx);

    // First get all bundles
    const bundles = await caller.bundles.list();
    
    if (bundles.length > 0) {
      const bundleId = bundles[0]!.id;
      const courses = await caller.bundles.getBundleCourses({ bundleId });

      expect(Array.isArray(courses)).toBe(true);
      // Bundles should contain at least one course
      expect(courses.length).toBeGreaterThan(0);
      
      if (courses.length > 0) {
        const course = courses[0];
        expect(course).toHaveProperty("id");
        expect(course).toHaveProperty("title");
        expect(course).toHaveProperty("slug");
      }
    }
  });

  it("should calculate correct discount", async () => {
    const { ctx } = createAdminContext();
    const caller = appRouter.createCaller(ctx);

    const bundles = await caller.bundles.list();
    
    if (bundles.length > 0) {
      const bundle = bundles[0]!;
      
      // Verify discount calculation
      const expectedPrice = Math.round(
        bundle.originalPrice * (1 - bundle.discountPercent / 100)
      );
      
      expect(bundle.price).toBe(expectedPrice);
    }
  });
});
