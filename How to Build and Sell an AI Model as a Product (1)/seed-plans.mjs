#!/usr/bin/env node
import { drizzle } from "drizzle-orm/mysql2";
import { subscriptionPlans } from "./drizzle/schema.js";
import dotenv from "dotenv";

dotenv.config();

const db = drizzle(process.env.DATABASE_URL);

const plans = [
  {
    name: "Starter",
    description: "Perfect for individual traders getting started with JSE analysis",
    priceRands: "499.00",
    billingCycle: "monthly",
    features: JSON.stringify([
      "Real-time JSE stock prices",
      "ECM confidence scores",
      "Track up to 10 stocks",
      "5 price alerts",
      "Basic sector analysis",
      "Email support"
    ]),
    maxStocks: 10,
    maxAlerts: 5,
    advancedAnalytics: false,
    apiAccess: false,
    prioritySupport: false,
    active: true,
  },
  {
    name: "Professional",
    description: "Advanced tools for serious traders and analysts",
    priceRands: "999.00",
    billingCycle: "monthly",
    features: JSON.stringify([
      "Everything in Starter",
      "Track up to 50 stocks",
      "20 price alerts",
      "Advanced ECM analytics",
      "Historical data access",
      "Sector deep-dive reports",
      "Priority email support"
    ]),
    maxStocks: 50,
    maxAlerts: 20,
    advancedAnalytics: true,
    apiAccess: false,
    prioritySupport: true,
    active: true,
  },
  {
    name: "Enterprise",
    description: "Complete solution for institutional traders and fund managers",
    priceRands: "2499.00",
    billingCycle: "monthly",
    features: JSON.stringify([
      "Everything in Professional",
      "Unlimited stock tracking",
      "Unlimited price alerts",
      "API access for integration",
      "Custom ECM models",
      "White-label options",
      "Dedicated account manager",
      "24/7 priority support"
    ]),
    maxStocks: 999999,
    maxAlerts: 999999,
    advancedAnalytics: true,
    apiAccess: true,
    prioritySupport: true,
    active: true,
  },
];

async function seed() {
  console.log("Seeding subscription plans...");
  
  try {
    for (const plan of plans) {
      await db.insert(subscriptionPlans).values(plan);
      console.log(`✓ Created plan: ${plan.name} - R${plan.priceRands}`);
    }
    
    console.log("\n✅ All subscription plans seeded successfully!");
  } catch (error) {
    console.error("❌ Error seeding plans:", error);
    process.exit(1);
  }
  
  process.exit(0);
}

seed();
