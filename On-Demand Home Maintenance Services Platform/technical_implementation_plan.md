# Technical Implementation Plan

## South African Home Services Marketplace - MVP Development

---

## Table of Contents

1. [Technical Architecture Overview](#technical-architecture-overview)
2. [Technology Stack Specification](#technology-stack-specification)
3. [Database Schema Design](#database-schema-design)
4. [API Endpoints Specification](#api-endpoints-specification)
5. [Payment Integration Guide](#payment-integration-guide)
6. [Development Sprint Plan](#development-sprint-plan)
7. [Deployment and Infrastructure](#deployment-and-infrastructure)
8. [Security and Compliance](#security-and-compliance)
9. [Testing Strategy](#testing-strategy)
10. [Post-Launch Monitoring](#post-launch-monitoring)

---

## 1. Technical Architecture Overview

### 1.1 System Architecture

The platform follows a modern **three-tier architecture** with clear separation of concerns:

```
┌─────────────────────────────────────────────────────────────┐
│                     PRESENTATION LAYER                       │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │   Web App    │  │  Mobile PWA  │  │  Admin Panel │      │
│  │  (Next.js)   │  │  (Next.js)   │  │  (Next.js)   │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                      APPLICATION LAYER                       │
│  ┌──────────────────────────────────────────────────────┐   │
│  │           RESTful API (Node.js/Express)              │   │
│  │  ┌────────────┐  ┌────────────┐  ┌────────────┐    │   │
│  │  │   Auth     │  │  Booking   │  │  Payment   │    │   │
│  │  │  Service   │  │  Service   │  │  Service   │    │   │
│  │  └────────────┘  └────────────┘  └────────────┘    │   │
│  └──────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                        DATA LAYER                            │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │  PostgreSQL  │  │  S3 Storage  │  │    Redis     │      │
│  │  (Primary)   │  │   (Files)    │  │   (Cache)    │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
└─────────────────────────────────────────────────────────────┘
                            │
                            ▼
┌─────────────────────────────────────────────────────────────┐
│                    EXTERNAL SERVICES                         │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐      │
│  │   PayFast    │  │    Twilio    │  │   SendGrid   │      │
│  │  (Payment)   │  │    (SMS)     │  │   (Email)    │      │
│  └──────────────┘  └──────────────┘  └──────────────┘      │
└─────────────────────────────────────────────────────────────┘
```

### 1.2 Key Architectural Decisions

**Decision 1: Monolithic vs. Microservices**
- **Choice:** Monolithic architecture for MVP
- **Rationale:** Faster development, simpler deployment, adequate for initial scale (<10,000 users)
- **Future:** Migrate to microservices when reaching 50,000+ users

**Decision 2: Server-Side Rendering (SSR) vs. Client-Side Rendering (CSR)**
- **Choice:** Hybrid approach with Next.js (SSR for public pages, CSR for dashboards)
- **Rationale:** SEO benefits for landing pages, fast interactivity for user dashboards

**Decision 3: Relational vs. NoSQL Database**
- **Choice:** PostgreSQL (relational)
- **Rationale:** Complex relationships (users, bookings, reviews), ACID compliance for transactions

**Decision 4: Real-time Communication**
- **Choice:** WebSockets (Socket.io) for in-app messaging
- **Rationale:** Real-time updates for job status, quotes, and messages

**Decision 5: Mobile Strategy**
- **Choice:** Progressive Web App (PWA) initially, native apps later
- **Rationale:** Cost-effective, single codebase, works across iOS/Android, installable

---

## 2. Technology Stack Specification

### 2.1 Frontend Stack

| Component | Technology | Version | Purpose |
|-----------|-----------|---------|---------|
| **Framework** | Next.js | 14.x | React framework with SSR, routing, and optimization |
| **UI Library** | React | 18.x | Component-based UI development |
| **Styling** | Tailwind CSS | 3.x | Utility-first CSS framework |
| **State Management** | Zustand | 4.x | Lightweight state management |
| **Forms** | React Hook Form | 7.x | Form validation and handling |
| **HTTP Client** | Axios | 1.x | API requests with interceptors |
| **Real-time** | Socket.io Client | 4.x | WebSocket communication |
| **Date Handling** | date-fns | 2.x | Date formatting and manipulation |
| **Icons** | Lucide React | Latest | Icon library |
| **Maps** | Leaflet | 1.x | Interactive maps for service areas |

### 2.2 Backend Stack

| Component | Technology | Version | Purpose |
|-----------|-----------|---------|---------|
| **Runtime** | Node.js | 20.x LTS | JavaScript runtime |
| **Framework** | Express.js | 4.x | Web application framework |
| **Database ORM** | Prisma | 5.x | Type-safe database client |
| **Authentication** | Passport.js | 0.7.x | Authentication middleware |
| **JWT** | jsonwebtoken | 9.x | Token-based authentication |
| **Validation** | Joi | 17.x | Request validation |
| **File Upload** | Multer | 1.x | Multipart form data handling |
| **Email** | Nodemailer | 6.x | Email sending |
| **SMS** | Twilio SDK | 4.x | SMS notifications |
| **Payment** | PayFast SDK | Custom | Payment processing |
| **Real-time** | Socket.io | 4.x | WebSocket server |
| **Cron Jobs** | node-cron | 3.x | Scheduled tasks |
| **Logging** | Winston | 3.x | Application logging |

### 2.3 Database and Storage

| Component | Technology | Purpose |
|-----------|-----------|---------|
| **Primary Database** | PostgreSQL 15+ | User data, bookings, transactions |
| **Cache** | Redis 7+ | Session storage, rate limiting |
| **File Storage** | S3-compatible (Cloudflare R2 / AWS S3) | Profile photos, job images, documents |
| **Search** | PostgreSQL Full-Text Search | Provider and job search (upgrade to Elasticsearch later) |

### 2.4 DevOps and Infrastructure

| Component | Technology | Purpose |
|-----------|-----------|---------|
| **Hosting (Frontend)** | Vercel | Next.js deployment with CDN |
| **Hosting (Backend)** | Railway / Render | Node.js API hosting |
| **Database Hosting** | Railway / Supabase | Managed PostgreSQL |
| **CI/CD** | GitHub Actions | Automated testing and deployment |
| **Monitoring** | Sentry | Error tracking and monitoring |
| **Analytics** | Google Analytics 4 | User behavior tracking |
| **Uptime Monitoring** | UptimeRobot | Service availability monitoring |

### 2.5 Development Tools

| Tool | Purpose |
|------|---------|
| **Version Control** | Git + GitHub |
| **Package Manager** | pnpm (faster than npm/yarn) |
| **Code Editor** | VS Code (recommended) |
| **API Testing** | Postman / Thunder Client |
| **Database GUI** | Prisma Studio / TablePlus |
| **Design** | Figma (for UI mockups) |

### 2.6 Cost Breakdown (Monthly, MVP Phase)

| Service | Free Tier | Paid (if needed) | Notes |
|---------|-----------|------------------|-------|
| **Vercel (Frontend)** | ✅ Unlimited | $20/month (Pro) | Free tier sufficient for MVP |
| **Railway (Backend + DB)** | $5 credit | $10-20/month | Pay-as-you-go |
| **Cloudflare R2 (Storage)** | 10GB free | $0.015/GB | ~$2/month for MVP |
| **SendGrid (Email)** | 100/day free | $15/month (40K emails) | Free tier sufficient initially |
| **Twilio (SMS)** | Trial credit | ~$0.08/SMS | ~$50/month for notifications |
| **PayFast** | No fee | 2.9% + R2 per transaction | Transaction-based |
| **Sentry (Monitoring)** | 5K events/month | $26/month | Free tier sufficient |
| **Domain** | - | R200/year (~$11) | One-time annual cost |
| **SSL Certificate** | ✅ Free (Let's Encrypt) | - | Included with hosting |
| **Total (Initial)** | **~$0-20/month** | **~$50-100/month at scale** | Well within R10K budget |

---

## 3. Database Schema Design

### 3.1 Entity Relationship Diagram

```
┌─────────────┐         ┌─────────────────┐         ┌─────────────────┐
│    users    │────────▶│ customer_profiles│         │provider_profiles│◀────┐
│             │         │                 │         │                 │     │
│ - id        │         │ - user_id (FK)  │         │ - user_id (FK)  │     │
│ - email     │         │ - name          │         │ - business_name │     │
│ - password  │         │ - phone         │         │ - services[]    │     │
│ - role      │         │ - address       │         │ - rating        │     │
│ - created_at│         └─────────────────┘         │ - verified      │     │
└─────────────┘                                     └─────────────────┘     │
      │                                                     │                │
      │                                                     │                │
      ▼                                                     ▼                │
┌─────────────────┐                               ┌─────────────────┐      │
│service_requests │                               │     quotes      │      │
│                 │                               │                 │      │
│ - id            │                               │ - id            │      │
│ - customer_id   │◀──────────────────────────────│ - request_id    │      │
│ - service_type  │                               │ - provider_id   │──────┘
│ - description   │                               │ - amount        │
│ - location      │                               │ - details       │
│ - status        │                               │ - status        │
│ - created_at    │                               │ - created_at    │
└─────────────────┘                               └─────────────────┘
      │                                                     │
      │                                                     │
      ▼                                                     ▼
┌─────────────────┐                               ┌─────────────────┐
│    bookings     │◀──────────────────────────────│  transactions   │
│                 │                               │                 │
│ - id            │                               │ - id            │
│ - request_id    │                               │ - booking_id    │
│ - quote_id      │                               │ - amount        │
│ - provider_id   │                               │ - commission    │
│ - customer_id   │                               │ - payout        │
│ - scheduled_date│                               │ - status        │
│ - status        │                               │ - payfast_id    │
│ - payment_status│                               │ - created_at    │
└─────────────────┘                               └─────────────────┘
      │
      │
      ▼
┌─────────────────┐
│     reviews     │
│                 │
│ - id            │
│ - booking_id    │
│ - customer_id   │
│ - provider_id   │
│ - rating        │
│ - comment       │
│ - created_at    │
└─────────────────┘
```

### 3.2 Core Tables Schema

#### users
```sql
CREATE TABLE users (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  email VARCHAR(255) UNIQUE NOT NULL,
  password_hash VARCHAR(255) NOT NULL,
  role VARCHAR(20) NOT NULL CHECK (role IN ('customer', 'provider', 'admin')),
  email_verified BOOLEAN DEFAULT FALSE,
  phone VARCHAR(20),
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_role ON users(role);
```

#### customer_profiles
```sql
CREATE TABLE customer_profiles (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID UNIQUE NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  first_name VARCHAR(100) NOT NULL,
  last_name VARCHAR(100) NOT NULL,
  phone VARCHAR(20),
  address TEXT,
  city VARCHAR(100),
  postal_code VARCHAR(10),
  latitude DECIMAL(10, 8),
  longitude DECIMAL(11, 8),
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_customer_user_id ON customer_profiles(user_id);
```

#### provider_profiles
```sql
CREATE TABLE provider_profiles (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID UNIQUE NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  business_name VARCHAR(255),
  bio TEXT,
  services TEXT[] NOT NULL, -- Array: ['plumbing', 'electrical']
  service_areas TEXT[] NOT NULL, -- Array: ['Southern Suburbs', 'City Bowl']
  years_experience INTEGER,
  verification_status VARCHAR(20) DEFAULT 'pending' CHECK (verification_status IN ('pending', 'probationary', 'verified', 'premium', 'suspended')),
  verification_date TIMESTAMP,
  rating DECIMAL(3, 2) DEFAULT 0.00,
  total_jobs INTEGER DEFAULT 0,
  total_reviews INTEGER DEFAULT 0,
  commission_rate DECIMAL(5, 2) DEFAULT 20.00, -- 20%
  profile_photo_url TEXT,
  portfolio_urls TEXT[], -- Array of image URLs
  insurance_provider VARCHAR(255),
  insurance_policy_number VARCHAR(100),
  insurance_expiry DATE,
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_provider_user_id ON provider_profiles(user_id);
CREATE INDEX idx_provider_services ON provider_profiles USING GIN(services);
CREATE INDEX idx_provider_verification ON provider_profiles(verification_status);
CREATE INDEX idx_provider_rating ON provider_profiles(rating DESC);
```

#### service_requests
```sql
CREATE TABLE service_requests (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  customer_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  service_type VARCHAR(50) NOT NULL, -- 'plumbing', 'electrical', etc.
  title VARCHAR(255) NOT NULL,
  description TEXT NOT NULL,
  location_address TEXT NOT NULL,
  location_city VARCHAR(100),
  location_latitude DECIMAL(10, 8),
  location_longitude DECIMAL(11, 8),
  preferred_date DATE,
  preferred_time VARCHAR(20), -- 'morning', 'afternoon', 'evening'
  urgency VARCHAR(20) DEFAULT 'normal' CHECK (urgency IN ('low', 'normal', 'urgent', 'emergency')),
  budget_min DECIMAL(10, 2),
  budget_max DECIMAL(10, 2),
  status VARCHAR(20) DEFAULT 'open' CHECK (status IN ('open', 'quoted', 'booked', 'completed', 'cancelled')),
  image_urls TEXT[], -- Array of job photos
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_requests_customer ON service_requests(customer_id);
CREATE INDEX idx_requests_service_type ON service_requests(service_type);
CREATE INDEX idx_requests_status ON service_requests(status);
CREATE INDEX idx_requests_created ON service_requests(created_at DESC);
```

#### quotes
```sql
CREATE TABLE quotes (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  request_id UUID NOT NULL REFERENCES service_requests(id) ON DELETE CASCADE,
  provider_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  amount DECIMAL(10, 2) NOT NULL,
  details TEXT,
  estimated_duration VARCHAR(100), -- '2-3 hours'
  availability TEXT, -- 'Available tomorrow morning'
  status VARCHAR(20) DEFAULT 'pending' CHECK (status IN ('pending', 'accepted', 'rejected', 'expired')),
  valid_until TIMESTAMP,
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_quotes_request ON quotes(request_id);
CREATE INDEX idx_quotes_provider ON quotes(provider_id);
CREATE INDEX idx_quotes_status ON quotes(status);
```

#### bookings
```sql
CREATE TABLE bookings (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  request_id UUID NOT NULL REFERENCES service_requests(id) ON DELETE CASCADE,
  quote_id UUID NOT NULL REFERENCES quotes(id) ON DELETE CASCADE,
  customer_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  provider_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  scheduled_date DATE NOT NULL,
  scheduled_time VARCHAR(20),
  amount DECIMAL(10, 2) NOT NULL,
  commission_rate DECIMAL(5, 2) NOT NULL,
  commission_amount DECIMAL(10, 2) NOT NULL,
  provider_payout DECIMAL(10, 2) NOT NULL,
  status VARCHAR(20) DEFAULT 'confirmed' CHECK (status IN ('confirmed', 'in_progress', 'completed', 'cancelled', 'disputed')),
  payment_status VARCHAR(20) DEFAULT 'pending' CHECK (payment_status IN ('pending', 'paid', 'held', 'released', 'refunded')),
  completion_date TIMESTAMP,
  cancellation_reason TEXT,
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_bookings_customer ON bookings(customer_id);
CREATE INDEX idx_bookings_provider ON bookings(provider_id);
CREATE INDEX idx_bookings_status ON bookings(status);
CREATE INDEX idx_bookings_payment ON bookings(payment_status);
CREATE INDEX idx_bookings_scheduled ON bookings(scheduled_date);
```

#### transactions
```sql
CREATE TABLE transactions (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  booking_id UUID NOT NULL REFERENCES bookings(id) ON DELETE CASCADE,
  customer_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  provider_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  amount DECIMAL(10, 2) NOT NULL,
  commission_amount DECIMAL(10, 2) NOT NULL,
  provider_payout DECIMAL(10, 2) NOT NULL,
  payment_method VARCHAR(50), -- 'card', 'eft', 'instant_eft'
  payfast_payment_id VARCHAR(255),
  payfast_status VARCHAR(50),
  status VARCHAR(20) DEFAULT 'pending' CHECK (status IN ('pending', 'completed', 'failed', 'refunded')),
  paid_at TIMESTAMP,
  payout_at TIMESTAMP,
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_transactions_booking ON transactions(booking_id);
CREATE INDEX idx_transactions_customer ON transactions(customer_id);
CREATE INDEX idx_transactions_provider ON transactions(provider_id);
CREATE INDEX idx_transactions_status ON transactions(status);
```

#### reviews
```sql
CREATE TABLE reviews (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  booking_id UUID UNIQUE NOT NULL REFERENCES bookings(id) ON DELETE CASCADE,
  customer_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  provider_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  rating INTEGER NOT NULL CHECK (rating >= 1 AND rating <= 5),
  comment TEXT,
  response TEXT, -- Provider can respond to review
  response_at TIMESTAMP,
  created_at TIMESTAMP DEFAULT NOW(),
  updated_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_reviews_provider ON reviews(provider_id);
CREATE INDEX idx_reviews_customer ON reviews(customer_id);
CREATE INDEX idx_reviews_rating ON reviews(rating DESC);
CREATE INDEX idx_reviews_created ON reviews(created_at DESC);
```

#### messages
```sql
CREATE TABLE messages (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  booking_id UUID NOT NULL REFERENCES bookings(id) ON DELETE CASCADE,
  sender_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  recipient_id UUID NOT NULL REFERENCES users(id) ON DELETE CASCADE,
  content TEXT NOT NULL,
  read BOOLEAN DEFAULT FALSE,
  created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_messages_booking ON messages(booking_id);
CREATE INDEX idx_messages_sender ON messages(sender_id);
CREATE INDEX idx_messages_recipient ON messages(recipient_id);
CREATE INDEX idx_messages_created ON messages(created_at DESC);
```

### 3.3 Prisma Schema Example

```prisma
// prisma/schema.prisma

generator client {
  provider = "prisma-client-js"
}

datasource db {
  provider = "postgresql"
  url      = env("DATABASE_URL")
}

model User {
  id            String   @id @default(uuid())
  email         String   @unique
  passwordHash  String   @map("password_hash")
  role          Role
  emailVerified Boolean  @default(false) @map("email_verified")
  phone         String?
  createdAt     DateTime @default(now()) @map("created_at")
  updatedAt     DateTime @updatedAt @map("updated_at")

  customerProfile CustomerProfile?
  providerProfile ProviderProfile?
  serviceRequests ServiceRequest[]
  quotes          Quote[]
  bookingsAsCustomer Booking[] @relation("CustomerBookings")
  bookingsAsProvider Booking[] @relation("ProviderBookings")
  reviewsGiven    Review[] @relation("CustomerReviews")
  reviewsReceived Review[] @relation("ProviderReviews")
  messagesSent    Message[] @relation("SentMessages")
  messagesReceived Message[] @relation("ReceivedMessages")

  @@map("users")
}

enum Role {
  customer
  provider
  admin
}

model CustomerProfile {
  id         String   @id @default(uuid())
  userId     String   @unique @map("user_id")
  firstName  String   @map("first_name")
  lastName   String   @map("last_name")
  phone      String?
  address    String?
  city       String?
  postalCode String?  @map("postal_code")
  latitude   Decimal? @db.Decimal(10, 8)
  longitude  Decimal? @db.Decimal(11, 8)
  createdAt  DateTime @default(now()) @map("created_at")
  updatedAt  DateTime @updatedAt @map("updated_at")

  user User @relation(fields: [userId], references: [id], onDelete: Cascade)

  @@map("customer_profiles")
}

model ProviderProfile {
  id                 String   @id @default(uuid())
  userId             String   @unique @map("user_id")
  businessName       String?  @map("business_name")
  bio                String?
  services           String[]
  serviceAreas       String[] @map("service_areas")
  yearsExperience    Int?     @map("years_experience")
  verificationStatus VerificationStatus @default(pending) @map("verification_status")
  verificationDate   DateTime? @map("verification_date")
  rating             Decimal  @default(0.00) @db.Decimal(3, 2)
  totalJobs          Int      @default(0) @map("total_jobs")
  totalReviews       Int      @default(0) @map("total_reviews")
  commissionRate     Decimal  @default(20.00) @db.Decimal(5, 2) @map("commission_rate")
  profilePhotoUrl    String?  @map("profile_photo_url")
  portfolioUrls      String[] @map("portfolio_urls")
  insuranceProvider  String?  @map("insurance_provider")
  insurancePolicyNumber String? @map("insurance_policy_number")
  insuranceExpiry    DateTime? @map("insurance_expiry") @db.Date
  createdAt          DateTime @default(now()) @map("created_at")
  updatedAt          DateTime @updatedAt @map("updated_at")

  user User @relation(fields: [userId], references: [id], onDelete: Cascade)

  @@map("provider_profiles")
}

enum VerificationStatus {
  pending
  probationary
  verified
  premium
  suspended
}

// ... (continue with other models)
```

---

## 4. API Endpoints Specification

### 4.1 Authentication Endpoints

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| POST | `/api/auth/register` | Register new user (customer or provider) | No |
| POST | `/api/auth/login` | Login and receive JWT token | No |
| POST | `/api/auth/logout` | Logout and invalidate token | Yes |
| POST | `/api/auth/forgot-password` | Request password reset email | No |
| POST | `/api/auth/reset-password` | Reset password with token | No |
| GET | `/api/auth/me` | Get current user profile | Yes |
| PUT | `/api/auth/me` | Update current user profile | Yes |

### 4.2 Customer Endpoints

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/api/customers/profile` | Get customer profile | Yes (Customer) |
| PUT | `/api/customers/profile` | Update customer profile | Yes (Customer) |
| GET | `/api/customers/bookings` | Get customer's bookings | Yes (Customer) |
| GET | `/api/customers/bookings/:id` | Get specific booking details | Yes (Customer) |
| POST | `/api/customers/reviews` | Submit review for completed job | Yes (Customer) |

### 4.3 Provider Endpoints

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/api/providers` | Search/browse providers | No |
| GET | `/api/providers/:id` | Get provider profile | No |
| GET | `/api/providers/me` | Get own provider profile | Yes (Provider) |
| PUT | `/api/providers/me` | Update provider profile | Yes (Provider) |
| GET | `/api/providers/me/bookings` | Get provider's bookings | Yes (Provider) |
| GET | `/api/providers/me/earnings` | Get earnings dashboard | Yes (Provider) |
| GET | `/api/providers/me/reviews` | Get provider's reviews | Yes (Provider) |

### 4.4 Service Request Endpoints

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| POST | `/api/requests` | Create new service request | Yes (Customer) |
| GET | `/api/requests` | Get service requests (filtered by provider services) | Yes (Provider) |
| GET | `/api/requests/:id` | Get specific request details | Yes |
| PUT | `/api/requests/:id` | Update service request | Yes (Customer) |
| DELETE | `/api/requests/:id` | Cancel service request | Yes (Customer) |

### 4.5 Quote Endpoints

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| POST | `/api/quotes` | Submit quote for service request | Yes (Provider) |
| GET | `/api/quotes/request/:requestId` | Get all quotes for a request | Yes (Customer) |
| GET | `/api/quotes/:id` | Get specific quote details | Yes |
| PUT | `/api/quotes/:id/accept` | Accept a quote (creates booking) | Yes (Customer) |
| PUT | `/api/quotes/:id/reject` | Reject a quote | Yes (Customer) |

### 4.6 Booking Endpoints

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/api/bookings/:id` | Get booking details | Yes |
| PUT | `/api/bookings/:id/start` | Mark job as started | Yes (Provider) |
| PUT | `/api/bookings/:id/complete` | Mark job as completed | Yes (Provider) |
| PUT | `/api/bookings/:id/cancel` | Cancel booking | Yes |
| POST | `/api/bookings/:id/dispute` | File dispute | Yes |

### 4.7 Payment Endpoints

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| POST | `/api/payments/initiate` | Initiate payment (redirect to PayFast) | Yes (Customer) |
| POST | `/api/payments/webhook` | PayFast webhook (payment confirmation) | No (Verified) |
| GET | `/api/payments/:id/status` | Check payment status | Yes |

### 4.8 Messaging Endpoints

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/api/messages/booking/:bookingId` | Get messages for a booking | Yes |
| POST | `/api/messages` | Send message | Yes |
| PUT | `/api/messages/:id/read` | Mark message as read | Yes |

### 4.9 Admin Endpoints

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/api/admin/providers/pending` | Get providers pending verification | Yes (Admin) |
| PUT | `/api/admin/providers/:id/verify` | Approve provider | Yes (Admin) |
| PUT | `/api/admin/providers/:id/reject` | Reject provider | Yes (Admin) |
| GET | `/api/admin/disputes` | Get all disputes | Yes (Admin) |
| PUT | `/api/admin/disputes/:id/resolve` | Resolve dispute | Yes (Admin) |
| GET | `/api/admin/analytics` | Get platform analytics | Yes (Admin) |

### 4.10 Example API Request/Response

**POST `/api/requests` - Create Service Request**

Request:
```json
{
  "serviceType": "plumbing",
  "title": "Leaking kitchen tap",
  "description": "The kitchen tap has been leaking for 2 days. Water drips constantly even when fully closed.",
  "locationAddress": "123 Main Road, Claremont, Cape Town",
  "locationCity": "Cape Town",
  "preferredDate": "2025-11-28",
  "preferredTime": "morning",
  "urgency": "normal",
  "budgetMin": 500,
  "budgetMax": 1000,
  "imageUrls": ["https://storage.example.com/job-photos/abc123.jpg"]
}
```

Response (201 Created):
```json
{
  "success": true,
  "data": {
    "id": "req_abc123xyz",
    "customerId": "user_customer123",
    "serviceType": "plumbing",
    "title": "Leaking kitchen tap",
    "description": "The kitchen tap has been leaking for 2 days...",
    "locationAddress": "123 Main Road, Claremont, Cape Town",
    "status": "open",
    "createdAt": "2025-11-25T10:30:00Z"
  }
}
```

---

## 5. Payment Integration Guide

### 5.1 PayFast Integration Overview

PayFast is South Africa's leading payment gateway, supporting:
- Credit/debit cards (Visa, Mastercard)
- Instant EFT (bank transfers)
- SnapScan, Zapper (mobile wallets)

**Integration Type:** Server-to-server with payment redirect

### 5.2 PayFast Setup Steps

**Step 1: Create PayFast Account**
1. Register at https://www.payfast.co.za/
2. Complete business verification
3. Obtain Merchant ID and Merchant Key
4. Set up passphrase for security

**Step 2: Configure Webhook**
- Set ITN (Instant Transaction Notification) URL: `https://yourdomain.com/api/payments/webhook`
- Enable ITN in PayFast dashboard
- Test with sandbox environment first

**Step 3: Install PayFast SDK**
```bash
npm install payfast-node
```

### 5.3 Payment Flow

```
Customer                Platform              PayFast              Provider
   │                       │                     │                    │
   │  1. Accept Quote      │                     │                    │
   ├──────────────────────>│                     │                    │
   │                       │                     │                    │
   │                       │  2. Create Booking  │                    │
   │                       │     (status: pending)│                   │
   │                       │                     │                    │
   │  3. Redirect to       │                     │                    │
   │     PayFast           │                     │                    │
   │<──────────────────────│                     │                    │
   │                       │                     │                    │
   │  4. Complete Payment  │                     │                    │
   ├───────────────────────┼────────────────────>│                    │
   │                       │                     │                    │
   │                       │  5. ITN Webhook     │                    │
   │                       │<────────────────────│                    │
   │                       │                     │                    │
   │                       │  6. Update Booking  │                    │
   │                       │     (status: paid)  │                    │
   │                       │                     │                    │
   │  7. Confirmation      │                     │                    │
   │<──────────────────────│                     │                    │
   │                       │                     │                    │
   │                       │  8. Notify Provider │                    │
   │                       ├────────────────────────────────────────>│
   │                       │                     │                    │
   │                       │  (Job Completed)    │                    │
   │                       │                     │                    │
   │                       │  9. Release Payment │                    │
   │                       │     (minus commission)                   │
   │                       ├────────────────────────────────────────>│
```

### 5.4 Payment Implementation Code

**Create Payment (Backend)**

```javascript
// routes/payments.js
const payfast = require('payfast-node');

const payfastConfig = {
  merchantId: process.env.PAYFAST_MERCHANT_ID,
  merchantKey: process.env.PAYFAST_MERCHANT_KEY,
  passphrase: process.env.PAYFAST_PASSPHRASE,
  sandbox: process.env.NODE_ENV !== 'production'
};

router.post('/initiate', authenticateUser, async (req, res) => {
  const { bookingId } = req.body;
  
  // Get booking details
  const booking = await prisma.booking.findUnique({
    where: { id: bookingId },
    include: { customer: true, provider: true }
  });
  
  if (!booking || booking.customerId !== req.user.id) {
    return res.status(403).json({ error: 'Unauthorized' });
  }
  
  // Create PayFast payment data
  const paymentData = {
    merchant_id: payfastConfig.merchantId,
    merchant_key: payfastConfig.merchantKey,
    return_url: `${process.env.APP_URL}/bookings/${bookingId}/payment-success`,
    cancel_url: `${process.env.APP_URL}/bookings/${bookingId}/payment-cancelled`,
    notify_url: `${process.env.API_URL}/api/payments/webhook`,
    
    // Transaction details
    m_payment_id: booking.id,
    amount: booking.amount.toFixed(2),
    item_name: `Home Service: ${booking.serviceType}`,
    item_description: `Booking #${booking.id.substring(0, 8)}`,
    
    // Customer details
    name_first: booking.customer.firstName,
    name_last: booking.customer.lastName,
    email_address: booking.customer.email,
    
    // Custom fields
    custom_str1: booking.providerId,
    custom_str2: booking.serviceType
  };
  
  // Generate signature
  const signature = payfast.generateSignature(paymentData, payfastConfig.passphrase);
  paymentData.signature = signature;
  
  // Create transaction record
  await prisma.transaction.create({
    data: {
      bookingId: booking.id,
      customerId: booking.customerId,
      providerId: booking.providerId,
      amount: booking.amount,
      commissionAmount: booking.commissionAmount,
      providerPayout: booking.providerPayout,
      status: 'pending'
    }
  });
  
  // Return PayFast URL
  const payfastUrl = payfastConfig.sandbox 
    ? 'https://sandbox.payfast.co.za/eng/process'
    : 'https://www.payfast.co.za/eng/process';
  
  res.json({
    success: true,
    paymentUrl: payfastUrl,
    paymentData
  });
});
```

**Handle Webhook (Backend)**

```javascript
// routes/payments.js
router.post('/webhook', async (req, res) => {
  const payfastData = req.body;
  
  // Verify signature
  const signature = payfast.generateSignature(payfastData, payfastConfig.passphrase);
  
  if (signature !== payfastData.signature) {
    console.error('Invalid PayFast signature');
    return res.status(400).send('Invalid signature');
  }
  
  // Verify payment status
  if (payfastData.payment_status !== 'COMPLETE') {
    console.log('Payment not complete:', payfastData.payment_status);
    return res.status(200).send('Payment not complete');
  }
  
  const bookingId = payfastData.m_payment_id;
  
  // Update booking and transaction
  await prisma.$transaction([
    prisma.booking.update({
      where: { id: bookingId },
      data: { 
        paymentStatus: 'paid',
        status: 'confirmed'
      }
    }),
    prisma.transaction.update({
      where: { bookingId },
      data: {
        status: 'completed',
        payfastPaymentId: payfastData.pf_payment_id,
        payfastStatus: payfastData.payment_status,
        paidAt: new Date()
      }
    })
  ]);
  
  // Send notifications
  await sendProviderNotification(bookingId, 'New booking confirmed!');
  await sendCustomerEmail(bookingId, 'Payment successful');
  
  res.status(200).send('OK');
});
```

### 5.5 Commission Calculation

```javascript
// utils/commission.js
function calculateCommission(amount, providerTier) {
  const commissionRates = {
    probationary: 0.20, // 20%
    verified: 0.18,     // 18%
    premium: 0.15       // 15%
  };
  
  const rate = commissionRates[providerTier] || 0.20;
  const commissionAmount = amount * rate;
  const providerPayout = amount - commissionAmount;
  
  return {
    amount,
    commissionRate: rate,
    commissionAmount: Math.round(commissionAmount * 100) / 100,
    providerPayout: Math.round(providerPayout * 100) / 100
  };
}

// Example usage
const booking = {
  amount: 800,
  providerTier: 'verified'
};

const payment = calculateCommission(booking.amount, booking.providerTier);
// {
//   amount: 800,
//   commissionRate: 0.18,
//   commissionAmount: 144,
//   providerPayout: 656
// }
```

### 5.6 Payout to Providers

**Manual Payout (Initial MVP):**
- Admin reviews completed jobs weekly
- Exports provider payouts from dashboard
- Processes bank transfers manually via FNB business banking

**Automated Payout (Future Enhancement):**
- Integrate with PayFast Payouts API
- Automatic transfer to provider bank accounts
- 48-hour payout cycle after job completion

---

## 6. Development Sprint Plan

### 6.1 Sprint Overview (8-Week Plan)

| Sprint | Duration | Focus | Deliverables |
|--------|----------|-------|--------------|
| **Sprint 1** | Week 1-2 | Foundation & Auth | User registration, login, database setup |
| **Sprint 2** | Week 3-4 | Core Features | Service requests, provider profiles, quotes |
| **Sprint 3** | Week 5-6 | Transactions | Booking system, PayFast integration, payments |
| **Sprint 4** | Week 7-8 | Quality & Launch | Reviews, messaging, admin dashboard, testing |

### 6.2 Sprint 1: Foundation & Authentication (Week 1-2)

**Week 1: Setup & Infrastructure**

Day 1-2: Project Setup
- [ ] Initialize Next.js project with TypeScript
- [ ] Set up Tailwind CSS and UI components
- [ ] Configure ESLint and Prettier
- [ ] Set up Git repository and GitHub
- [ ] Configure environment variables

Day 3-4: Database Setup
- [ ] Set up PostgreSQL database (Railway/Supabase)
- [ ] Define Prisma schema
- [ ] Run initial migrations
- [ ] Seed database with test data
- [ ] Set up Prisma Studio for database management

Day 5: Backend API Setup
- [ ] Initialize Express.js server
- [ ] Configure middleware (CORS, body-parser, helmet)
- [ ] Set up error handling
- [ ] Configure logging (Winston)
- [ ] Create API route structure

**Week 2: Authentication System**

Day 1-2: User Registration
- [ ] Create registration API endpoint
- [ ] Implement password hashing (bcrypt)
- [ ] Add email validation
- [ ] Create registration UI (customer and provider)
- [ ] Add form validation (React Hook Form + Joi)

Day 3-4: User Login
- [ ] Create login API endpoint
- [ ] Implement JWT token generation
- [ ] Add refresh token mechanism
- [ ] Create login UI
- [ ] Implement protected routes

Day 5: Profile Management
- [ ] Create profile API endpoints (GET, PUT)
- [ ] Build customer profile UI
- [ ] Build provider profile UI
- [ ] Add profile photo upload (S3)

**Sprint 1 Deliverables:**
- ✅ Working authentication system (register, login, logout)
- ✅ Customer and provider profile pages
- ✅ Database schema and migrations
- ✅ Basic UI components and layout

### 6.3 Sprint 2: Core Features (Week 3-4)

**Week 3: Service Requests**

Day 1-2: Create Service Request
- [ ] Build service request form UI
- [ ] Add image upload for job photos
- [ ] Create service request API endpoint
- [ ] Implement location selection (map or address input)
- [ ] Add service category selection

Day 3-4: Browse Service Requests (Provider View)
- [ ] Create service request listing API (filtered by provider services)
- [ ] Build provider dashboard with available jobs
- [ ] Add search and filter functionality
- [ ] Implement pagination
- [ ] Add job detail view

Day 5: Manage Service Requests (Customer View)
- [ ] Create customer dashboard with their requests
- [ ] Add edit/cancel request functionality
- [ ] Show request status (open, quoted, booked)
- [ ] Display received quotes

**Week 4: Provider Profiles & Quotes**

Day 1-2: Provider Search and Profiles
- [ ] Create provider search API (by service, location, rating)
- [ ] Build provider listing page
- [ ] Create provider profile page (public view)
- [ ] Add portfolio gallery
- [ ] Display reviews and ratings

Day 3-4: Quote System
- [ ] Create quote submission API
- [ ] Build quote form for providers
- [ ] Display quotes to customers (comparison view)
- [ ] Add quote acceptance/rejection
- [ ] Send notifications on new quotes

Day 5: Provider Dashboard
- [ ] Build provider dashboard (jobs, earnings, profile)
- [ ] Display submitted quotes and their status
- [ ] Show upcoming bookings
- [ ] Add earnings summary

**Sprint 2 Deliverables:**
- ✅ Customers can post service requests
- ✅ Providers can browse and quote on jobs
- ✅ Customers can compare and accept quotes
- ✅ Provider search and profile pages

### 6.4 Sprint 3: Transactions & Payments (Week 5-6)

**Week 5: Booking System**

Day 1-2: Create Booking
- [ ] Build booking creation logic (when quote accepted)
- [ ] Create booking API endpoints
- [ ] Calculate commission and provider payout
- [ ] Send booking confirmation emails
- [ ] Add booking to customer and provider dashboards

Day 3-4: Booking Management
- [ ] Build booking detail page
- [ ] Add job status updates (confirmed, in_progress, completed)
- [ ] Implement cancellation flow
- [ ] Add cancellation policies and fees
- [ ] Send status update notifications

Day 5: Booking Calendar
- [ ] Create calendar view for providers
- [ ] Add availability management
- [ ] Implement booking conflict detection
- [ ] Build scheduling interface

**Week 6: Payment Integration**

Day 1-2: PayFast Setup
- [ ] Create PayFast merchant account
- [ ] Configure PayFast credentials
- [ ] Implement payment initiation
- [ ] Build payment redirect flow
- [ ] Add payment success/failure pages

Day 3-4: Payment Webhook
- [ ] Create webhook endpoint
- [ ] Implement signature verification
- [ ] Update booking and transaction status
- [ ] Handle payment failures
- [ ] Add payment retry mechanism

Day 5: Transaction Management
- [ ] Build transaction history page (customer)
- [ ] Build earnings dashboard (provider)
- [ ] Add payout tracking
- [ ] Create admin transaction reports
- [ ] Implement refund logic

**Sprint 3 Deliverables:**
- ✅ Complete booking flow (quote → booking → payment)
- ✅ PayFast payment integration
- ✅ Transaction tracking and management
- ✅ Provider earnings dashboard

### 6.5 Sprint 4: Quality & Launch Prep (Week 7-8)

**Week 7: Reviews & Messaging**

Day 1-2: Review System
- [ ] Create review submission API
- [ ] Build review form (post-job completion)
- [ ] Display reviews on provider profiles
- [ ] Calculate and update provider ratings
- [ ] Add review moderation (admin)

Day 3-4: In-App Messaging
- [ ] Set up Socket.io for real-time messaging
- [ ] Create messaging API endpoints
- [ ] Build chat interface (booking-specific)
- [ ] Add message notifications
- [ ] Implement read receipts

Day 5: Notifications
- [ ] Set up email notifications (SendGrid/Nodemailer)
- [ ] Set up SMS notifications (Twilio)
- [ ] Create notification templates
- [ ] Add notification preferences
- [ ] Implement push notifications (PWA)

**Week 8: Admin Dashboard & Testing**

Day 1-2: Admin Dashboard
- [ ] Build admin login and authentication
- [ ] Create provider vetting dashboard
- [ ] Add dispute management interface
- [ ] Build analytics dashboard (GMV, users, jobs)
- [ ] Add user management tools

Day 3-4: Testing & Bug Fixes
- [ ] Write unit tests for critical functions
- [ ] Perform end-to-end testing
- [ ] Test payment flow thoroughly
- [ ] Cross-browser testing
- [ ] Mobile responsiveness testing
- [ ] Fix identified bugs

Day 5: Launch Preparation
- [ ] Set up production environment
- [ ] Configure domain and SSL
- [ ] Set up monitoring (Sentry, UptimeRobot)
- [ ] Create backup and recovery plan
- [ ] Prepare launch announcement
- [ ] Final security audit

**Sprint 4 Deliverables:**
- ✅ Review and rating system
- ✅ Real-time messaging
- ✅ Admin dashboard for vetting and management
- ✅ Comprehensive testing and bug fixes
- ✅ Production-ready platform

---

## 7. Deployment and Infrastructure

### 7.1 Hosting Architecture

**Frontend (Next.js):**
- **Platform:** Vercel
- **Deployment:** Automatic via GitHub integration
- **CDN:** Vercel Edge Network (global)
- **Environment:** Production, Staging

**Backend (Node.js API):**
- **Platform:** Railway or Render
- **Deployment:** Automatic via GitHub integration
- **Scaling:** Auto-scaling based on traffic
- **Environment:** Production, Staging

**Database (PostgreSQL):**
- **Platform:** Railway PostgreSQL or Supabase
- **Backups:** Daily automated backups
- **Replication:** Read replicas for scaling (future)

**File Storage (S3-compatible):**
- **Platform:** Cloudflare R2 or AWS S3
- **CDN:** Cloudflare CDN
- **Access:** Signed URLs for security

### 7.2 Environment Variables

**Frontend (.env.local):**
```bash
NEXT_PUBLIC_API_URL=https://api.yourdomain.com
NEXT_PUBLIC_APP_URL=https://yourdomain.com
NEXT_PUBLIC_GOOGLE_MAPS_API_KEY=your_google_maps_key
NEXT_PUBLIC_SOCKET_URL=wss://api.yourdomain.com
```

**Backend (.env):**
```bash
# Database
DATABASE_URL=postgresql://user:password@host:5432/database

# Authentication
JWT_SECRET=your_jwt_secret_key
JWT_REFRESH_SECRET=your_jwt_refresh_secret
JWT_EXPIRES_IN=1d
JWT_REFRESH_EXPIRES_IN=7d

# PayFast
PAYFAST_MERCHANT_ID=your_merchant_id
PAYFAST_MERCHANT_KEY=your_merchant_key
PAYFAST_PASSPHRASE=your_passphrase
PAYFAST_SANDBOX=false

# Email (SendGrid)
SENDGRID_API_KEY=your_sendgrid_key
FROM_EMAIL=noreply@yourdomain.com

# SMS (Twilio)
TWILIO_ACCOUNT_SID=your_twilio_sid
TWILIO_AUTH_TOKEN=your_twilio_token
TWILIO_PHONE_NUMBER=+27123456789

# Storage (S3/R2)
S3_ENDPOINT=https://your-bucket.r2.cloudflarestorage.com
S3_ACCESS_KEY_ID=your_access_key
S3_SECRET_ACCESS_KEY=your_secret_key
S3_BUCKET_NAME=your_bucket_name
S3_REGION=auto

# App URLs
APP_URL=https://yourdomain.com
API_URL=https://api.yourdomain.com

# Monitoring
SENTRY_DSN=your_sentry_dsn

# Other
NODE_ENV=production
PORT=3001
```

### 7.3 Deployment Checklist

**Pre-Deployment:**
- [ ] All tests passing
- [ ] Environment variables configured
- [ ] Database migrations run
- [ ] SSL certificates configured
- [ ] Domain DNS configured
- [ ] PayFast merchant account verified
- [ ] Email/SMS services configured

**Deployment Steps:**
1. Push code to `main` branch
2. Automatic deployment triggered (Vercel + Railway)
3. Run database migrations on production
4. Verify deployment health checks
5. Test critical user flows (registration, booking, payment)
6. Monitor error logs (Sentry)

**Post-Deployment:**
- [ ] Verify website is accessible
- [ ] Test user registration and login
- [ ] Test payment flow (small test transaction)
- [ ] Check email and SMS notifications
- [ ] Monitor server logs for errors
- [ ] Set up uptime monitoring alerts

### 7.4 Continuous Integration/Deployment (CI/CD)

**GitHub Actions Workflow:**

```yaml
# .github/workflows/deploy.yml
name: Deploy to Production

on:
  push:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-node@v3
        with:
          node-version: '20'
      - run: npm install
      - run: npm run test
      - run: npm run lint

  deploy-frontend:
    needs: test
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Deploy to Vercel
        uses: amondnet/vercel-action@v20
        with:
          vercel-token: ${{ secrets.VERCEL_TOKEN }}
          vercel-org-id: ${{ secrets.VERCEL_ORG_ID }}
          vercel-project-id: ${{ secrets.VERCEL_PROJECT_ID }}
          vercel-args: '--prod'

  deploy-backend:
    needs: test
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Deploy to Railway
        uses: bervProject/railway-deploy@main
        with:
          railway_token: ${{ secrets.RAILWAY_TOKEN }}
          service: api
```

---

## 8. Security and Compliance

### 8.1 Security Best Practices

**Authentication & Authorization:**
- Use bcrypt for password hashing (salt rounds: 12)
- Implement JWT with short expiration (1 day)
- Use refresh tokens for extended sessions
- Implement role-based access control (RBAC)
- Add rate limiting on auth endpoints (5 attempts per 15 min)

**Data Protection:**
- Encrypt sensitive data at rest (database encryption)
- Use HTTPS for all communications (SSL/TLS)
- Implement CORS with whitelist
- Sanitize all user inputs (prevent XSS, SQL injection)
- Use parameterized queries (Prisma ORM)

**Payment Security:**
- Never store credit card details
- Use PayFast's PCI-compliant payment gateway
- Verify webhook signatures
- Implement idempotency for payment operations
- Log all payment transactions

**File Upload Security:**
- Validate file types (images only: jpg, png, webp)
- Limit file size (max 5MB per image)
- Scan uploads for malware (ClamAV or similar)
- Use signed URLs for private files
- Store files in S3 with proper ACLs

### 8.2 POPIA Compliance (Protection of Personal Information Act)

**Data Collection:**
- Collect only necessary personal information
- Obtain explicit consent for data processing
- Provide clear privacy policy
- Allow users to access their data
- Implement data deletion requests

**Data Storage:**
- Store data securely (encrypted)
- Limit access to authorized personnel only
- Implement audit logs for data access
- Regular security audits

**Data Sharing:**
- Do not share personal data with third parties without consent
- Background check providers: explicit consent required
- Payment processors: only necessary transaction data

**User Rights:**
- Right to access personal data
- Right to correct inaccurate data
- Right to delete data (account deletion)
- Right to data portability

### 8.3 Terms of Service and Policies

**Required Legal Documents:**
1. **Terms of Service** - User agreement for platform usage
2. **Privacy Policy** - How personal data is collected and used (POPIA compliant)
3. **Provider Agreement** - Independent contractor terms
4. **Refund Policy** - Conditions for refunds and disputes
5. **Cookie Policy** - Disclosure of cookie usage

**Consult a South African lawyer to draft these documents.**

---

## 9. Testing Strategy

### 9.1 Testing Pyramid

```
                    ▲
                   ╱ ╲
                  ╱   ╲
                 ╱ E2E ╲          (10% - Critical user flows)
                ╱───────╲
               ╱         ╲
              ╱Integration╲       (30% - API endpoints, DB)
             ╱─────────────╲
            ╱               ╲
           ╱  Unit Tests     ╲    (60% - Functions, utilities)
          ╱___________________╲
```

### 9.2 Unit Testing

**Tools:** Jest, React Testing Library

**What to Test:**
- Utility functions (commission calculation, date formatting)
- React components (forms, buttons, cards)
- API route handlers
- Database models and queries

**Example Unit Test:**

```javascript
// utils/commission.test.js
const { calculateCommission } = require('./commission');

describe('Commission Calculation', () => {
  test('calculates 20% commission for probationary provider', () => {
    const result = calculateCommission(1000, 'probationary');
    expect(result.commissionAmount).toBe(200);
    expect(result.providerPayout).toBe(800);
  });

  test('calculates 18% commission for verified provider', () => {
    const result = calculateCommission(1000, 'verified');
    expect(result.commissionAmount).toBe(180);
    expect(result.providerPayout).toBe(820);
  });

  test('calculates 15% commission for premium provider', () => {
    const result = calculateCommission(1000, 'premium');
    expect(result.commissionAmount).toBe(150);
    expect(result.providerPayout).toBe(850);
  });
});
```

### 9.3 Integration Testing

**Tools:** Supertest (API testing), Prisma Test Environment

**What to Test:**
- API endpoints (request/response)
- Database operations (CRUD)
- Authentication flows
- Payment webhook handling

**Example Integration Test:**

```javascript
// routes/auth.test.js
const request = require('supertest');
const app = require('../app');

describe('POST /api/auth/register', () => {
  test('registers a new customer successfully', async () => {
    const response = await request(app)
      .post('/api/auth/register')
      .send({
        email: 'test@example.com',
        password: 'SecurePass123!',
        role: 'customer',
        firstName: 'John',
        lastName: 'Doe'
      });

    expect(response.status).toBe(201);
    expect(response.body.success).toBe(true);
    expect(response.body.data.email).toBe('test@example.com');
    expect(response.body.data.token).toBeDefined();
  });

  test('returns error for duplicate email', async () => {
    // Register first user
    await request(app).post('/api/auth/register').send({
      email: 'duplicate@example.com',
      password: 'SecurePass123!',
      role: 'customer'
    });

    // Try to register again with same email
    const response = await request(app)
      .post('/api/auth/register')
      .send({
        email: 'duplicate@example.com',
        password: 'AnotherPass456!',
        role: 'customer'
      });

    expect(response.status).toBe(400);
    expect(response.body.error).toContain('already exists');
  });
});
```

### 9.4 End-to-End Testing

**Tools:** Playwright or Cypress

**Critical User Flows to Test:**
1. Customer registration → post service request → receive quote → accept quote → pay → complete job → leave review
2. Provider registration → browse jobs → submit quote → quote accepted → complete job → receive payment
3. Admin login → review provider application → approve provider

**Example E2E Test:**

```javascript
// e2e/customer-booking-flow.spec.js
const { test, expect } = require('@playwright/test');

test('customer can book a service from start to finish', async ({ page }) => {
  // 1. Register as customer
  await page.goto('https://yourdomain.com/register');
  await page.fill('input[name="email"]', 'customer@example.com');
  await page.fill('input[name="password"]', 'SecurePass123!');
  await page.selectOption('select[name="role"]', 'customer');
  await page.click('button[type="submit"]');
  await expect(page).toHaveURL(/\/dashboard/);

  // 2. Post service request
  await page.click('text=Request a Service');
  await page.selectOption('select[name="serviceType"]', 'plumbing');
  await page.fill('input[name="title"]', 'Leaking tap');
  await page.fill('textarea[name="description"]', 'Kitchen tap is leaking');
  await page.fill('input[name="location"]', '123 Main Rd, Cape Town');
  await page.click('button:has-text("Submit Request")');
  await expect(page.locator('text=Request submitted')).toBeVisible();

  // 3. Wait for quote (simulate provider submitting quote)
  // ... (in real test, you'd have a provider account submit a quote)

  // 4. Accept quote
  await page.click('text=View Quotes');
  await page.click('button:has-text("Accept Quote")');
  await expect(page).toHaveURL(/\/payment/);

  // 5. Complete payment (redirect to PayFast sandbox)
  // ... (test payment flow)

  // 6. Verify booking confirmed
  await expect(page.locator('text=Booking Confirmed')).toBeVisible();
});
```

### 9.5 Manual Testing Checklist

**Before Launch:**
- [ ] Test on Chrome, Firefox, Safari, Edge
- [ ] Test on mobile devices (iOS, Android)
- [ ] Test all user roles (customer, provider, admin)
- [ ] Test payment flow with real PayFast sandbox
- [ ] Test email and SMS notifications
- [ ] Test file uploads (profile photos, job images)
- [ ] Test edge cases (invalid inputs, network errors)
- [ ] Test accessibility (keyboard navigation, screen readers)
- [ ] Test performance (page load times, API response times)

---

## 10. Post-Launch Monitoring

### 10.1 Monitoring Tools

**Error Tracking: Sentry**
- Real-time error notifications
- Stack traces and context
- Performance monitoring
- User feedback collection

**Uptime Monitoring: UptimeRobot**
- 5-minute interval checks
- Email/SMS alerts on downtime
- Status page for transparency

**Analytics: Google Analytics 4**
- User behavior tracking
- Conversion funnel analysis
- Traffic sources
- User demographics

**Application Performance: New Relic or Datadog (optional)**
- API response times
- Database query performance
- Server resource usage

### 10.2 Key Metrics to Monitor

**Technical Metrics:**
- API response time (target: <500ms)
- Error rate (target: <1%)
- Uptime (target: 99.9%)
- Database query time (target: <100ms)
- Page load time (target: <3s)

**Business Metrics:**
- Daily/monthly active users
- Conversion rate (visitor → registration → booking)
- Customer acquisition cost (CAC)
- Gross merchandise value (GMV)
- Platform revenue (commissions)
- Customer retention rate
- Provider utilization rate

**Quality Metrics:**
- Average customer rating
- Average provider rating
- Dispute rate
- Job completion rate
- Payment success rate

### 10.3 Alerting Strategy

**Critical Alerts (Immediate Action):**
- Website down (uptime < 99%)
- Payment processing failure
- Database connection errors
- High error rate (>5% of requests)

**Warning Alerts (Review Within 24 Hours):**
- Slow API response times (>1s)
- High dispute rate (>5%)
- Low provider response rate (<50%)
- Payment webhook delays

**Informational Alerts (Weekly Review):**
- New user registrations
- Weekly GMV summary
- Provider performance reports
- Customer satisfaction scores

### 10.4 Incident Response Plan

**Step 1: Detection**
- Automated monitoring alerts
- User reports via support channels
- Manual checks during critical periods

**Step 2: Assessment**
- Determine severity (critical, high, medium, low)
- Identify affected users and services
- Estimate impact on business

**Step 3: Response**
- Critical: Immediate action, all hands on deck
- High: Respond within 1 hour
- Medium: Respond within 4 hours
- Low: Respond within 24 hours

**Step 4: Communication**
- Notify affected users (email, in-app notification)
- Update status page
- Provide estimated resolution time

**Step 5: Resolution**
- Fix the issue
- Deploy hotfix if necessary
- Verify fix in production
- Monitor for recurrence

**Step 6: Post-Mortem**
- Document what happened
- Identify root cause
- Implement preventive measures
- Update runbooks and documentation

---

## Appendix A: Sample Code Snippets

### A.1 Authentication Middleware

```javascript
// middleware/auth.js
const jwt = require('jsonwebtoken');
const { PrismaClient } = require('@prisma/client');
const prisma = new PrismaClient();

async function authenticateUser(req, res, next) {
  try {
    // Get token from header
    const authHeader = req.headers.authorization;
    if (!authHeader || !authHeader.startsWith('Bearer ')) {
      return res.status(401).json({ error: 'No token provided' });
    }

    const token = authHeader.substring(7);

    // Verify token
    const decoded = jwt.verify(token, process.env.JWT_SECRET);

    // Get user from database
    const user = await prisma.user.findUnique({
      where: { id: decoded.userId },
      include: {
        customerProfile: true,
        providerProfile: true
      }
    });

    if (!user) {
      return res.status(401).json({ error: 'User not found' });
    }

    // Attach user to request
    req.user = user;
    next();
  } catch (error) {
    if (error.name === 'JsonWebTokenError') {
      return res.status(401).json({ error: 'Invalid token' });
    }
    if (error.name === 'TokenExpiredError') {
      return res.status(401).json({ error: 'Token expired' });
    }
    return res.status(500).json({ error: 'Authentication failed' });
  }
}

function requireRole(role) {
  return (req, res, next) => {
    if (req.user.role !== role) {
      return res.status(403).json({ error: 'Insufficient permissions' });
    }
    next();
  };
}

module.exports = { authenticateUser, requireRole };
```

### A.2 Email Notification Template

```javascript
// services/email.js
const nodemailer = require('nodemailer');

const transporter = nodemailer.createTransporter({
  host: 'smtp.sendgrid.net',
  port: 587,
  auth: {
    user: 'apikey',
    pass: process.env.SENDGRID_API_KEY
  }
});

async function sendBookingConfirmation(booking) {
  const customer = booking.customer;
  const provider = booking.provider;

  const emailHtml = `
    <!DOCTYPE html>
    <html>
    <head>
      <style>
        body { font-family: Arial, sans-serif; line-height: 1.6; }
        .container { max-width: 600px; margin: 0 auto; padding: 20px; }
        .header { background: #2563eb; color: white; padding: 20px; text-align: center; }
        .content { padding: 20px; background: #f9fafb; }
        .button { display: inline-block; padding: 12px 24px; background: #2563eb; color: white; text-decoration: none; border-radius: 6px; }
        .footer { text-align: center; padding: 20px; color: #6b7280; font-size: 14px; }
      </style>
    </head>
    <body>
      <div class="container">
        <div class="header">
          <h1>Booking Confirmed!</h1>
        </div>
        <div class="content">
          <p>Hi ${customer.firstName},</p>
          <p>Your booking has been confirmed. Here are the details:</p>
          
          <h3>Service Details:</h3>
          <ul>
            <li><strong>Service:</strong> ${booking.serviceType}</li>
            <li><strong>Provider:</strong> ${provider.businessName || provider.firstName}</li>
            <li><strong>Date:</strong> ${booking.scheduledDate}</li>
            <li><strong>Time:</strong> ${booking.scheduledTime}</li>
            <li><strong>Amount:</strong> R${booking.amount}</li>
          </ul>

          <p>Your provider will contact you shortly to confirm the details.</p>

          <p style="text-align: center; margin-top: 30px;">
            <a href="${process.env.APP_URL}/bookings/${booking.id}" class="button">View Booking</a>
          </p>
        </div>
        <div class="footer">
          <p>Need help? Contact us at support@yourdomain.com</p>
          <p>&copy; 2025 SA Home Services. All rights reserved.</p>
        </div>
      </div>
    </body>
    </html>
  `;

  await transporter.sendMail({
    from: process.env.FROM_EMAIL,
    to: customer.email,
    subject: 'Booking Confirmed - SA Home Services',
    html: emailHtml
  });
}

module.exports = { sendBookingConfirmation };
```

---

## Appendix B: Database Optimization

### B.1 Indexing Strategy

```sql
-- Performance-critical indexes

-- Users table
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_role ON users(role);

-- Provider profiles (search and filtering)
CREATE INDEX idx_provider_services ON provider_profiles USING GIN(services);
CREATE INDEX idx_provider_service_areas ON provider_profiles USING GIN(service_areas);
CREATE INDEX idx_provider_rating ON provider_profiles(rating DESC);
CREATE INDEX idx_provider_verification ON provider_profiles(verification_status);

-- Service requests (provider job browsing)
CREATE INDEX idx_requests_service_type ON service_requests(service_type);
CREATE INDEX idx_requests_status ON service_requests(status);
CREATE INDEX idx_requests_created ON service_requests(created_at DESC);
CREATE INDEX idx_requests_location ON service_requests(location_city, service_type);

-- Bookings (dashboard queries)
CREATE INDEX idx_bookings_customer ON bookings(customer_id, created_at DESC);
CREATE INDEX idx_bookings_provider ON bookings(provider_id, created_at DESC);
CREATE INDEX idx_bookings_status ON bookings(status);
CREATE INDEX idx_bookings_scheduled ON bookings(scheduled_date);

-- Reviews (provider profile)
CREATE INDEX idx_reviews_provider ON reviews(provider_id, created_at DESC);
CREATE INDEX idx_reviews_rating ON reviews(rating DESC);

-- Full-text search (future enhancement)
CREATE INDEX idx_requests_search ON service_requests USING GIN(to_tsvector('english', title || ' ' || description));
```

### B.2 Query Optimization Examples

**Inefficient Query:**
```javascript
// Loads all bookings into memory, then filters
const bookings = await prisma.booking.findMany({
  include: {
    customer: true,
    provider: true,
    request: true
  }
});
const activeBookings = bookings.filter(b => b.status === 'confirmed');
```

**Optimized Query:**
```javascript
// Filters at database level, only loads necessary data
const activeBookings = await prisma.booking.findMany({
  where: { status: 'confirmed' },
  select: {
    id: true,
    scheduledDate: true,
    amount: true,
    customer: {
      select: { firstName: true, lastName: true, phone: true }
    },
    provider: {
      select: { businessName: true, phone: true }
    },
    request: {
      select: { title: true, serviceType: true }
    }
  }
});
```

---

*Implementation Plan Version: 1.0*  
*Last Updated: November 25, 2025*  
*For Development Team Use*
