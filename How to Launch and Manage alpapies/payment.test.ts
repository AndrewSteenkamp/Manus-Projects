import { describe, expect, it } from "vitest";
import { appRouter } from "./routers";
import type { TrpcContext } from "./_core/context";

type AuthenticatedUser = NonNullable<TrpcContext["user"]>;

function createAuthContext(): { ctx: TrpcContext } {
  const user: AuthenticatedUser = {
    id: 1,
    openId: "sample-user",
    email: "sample@example.com",
    name: "Sample User",
    loginMethod: "manus",
    role: "user",
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

describe("payment procedures", () => {
  it("payment router is defined and accessible", () => {
    const { ctx } = createAuthContext();
    const caller = appRouter.createCaller(ctx);

    expect(caller.payment).toBeDefined();
    expect(caller.payment.createPayment).toBeDefined();
    expect(caller.payment.getPaymentByOrderId).toBeDefined();
  });

  it("validates payment processor enum", async () => {
    const { ctx } = createAuthContext();
    const caller = appRouter.createCaller(ctx);

    // Test that invalid processor is rejected
    await expect(
      caller.payment.createPayment({
        orderId: 1,
        processor: "invalid" as any,
        amount: 99.99,
        currency: "USD",
      })
    ).rejects.toThrow();
  });
});

describe("payment.getPaymentByOrderId", () => {
  it("returns undefined for non-existent order", async () => {
    const { ctx } = createAuthContext();
    const caller = appRouter.createCaller(ctx);

    const payment = await caller.payment.getPaymentByOrderId({
      orderId: 999999,
    });

    expect(payment).toBeUndefined();
  });
});
