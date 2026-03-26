import { bulkCreateAchievements, getAllAchievements } from './server/db.js';

const achievements = [
  // Milestone achievements
  {
    name: "First Steps",
    slug: "first-steps",
    description: "Complete your first lesson",
    icon: "footprints",
    category: "milestone",
    xpReward: 10,
    requirement: JSON.stringify({ type: "lessons_completed", count: 1 }),
  },
  {
    name: "Getting Started",
    slug: "getting-started",
    description: "Complete your first course",
    icon: "graduation-cap",
    category: "milestone",
    xpReward: 50,
    requirement: JSON.stringify({ type: "courses_completed", count: 1 }),
  },
  {
    name: "Knowledge Seeker",
    slug: "knowledge-seeker",
    description: "Complete 5 courses",
    icon: "book-open",
    category: "milestone",
    xpReward: 200,
    requirement: JSON.stringify({ type: "courses_completed", count: 5 }),
  },
  {
    name: "Master Learner",
    slug: "master-learner",
    description: "Complete 10 courses",
    icon: "award",
    category: "milestone",
    xpReward: 500,
    requirement: JSON.stringify({ type: "courses_completed", count: 10 }),
  },
  {
    name: "Prompt Expert",
    slug: "prompt-expert",
    description: "Complete 25 courses",
    icon: "trophy",
    category: "milestone",
    xpReward: 1000,
    requirement: JSON.stringify({ type: "courses_completed", count: 25 }),
  },
  
  // Streak achievements
  {
    name: "Consistent Learner",
    slug: "consistent-learner",
    description: "Maintain a 3-day learning streak",
    icon: "flame",
    category: "streak",
    xpReward: 30,
    requirement: JSON.stringify({ type: "streak", days: 3 }),
  },
  {
    name: "Week Warrior",
    slug: "week-warrior",
    description: "Maintain a 7-day learning streak",
    icon: "zap",
    category: "streak",
    xpReward: 100,
    requirement: JSON.stringify({ type: "streak", days: 7 }),
  },
  {
    name: "Dedication Master",
    slug: "dedication-master",
    description: "Maintain a 30-day learning streak",
    icon: "star",
    category: "streak",
    xpReward: 500,
    requirement: JSON.stringify({ type: "streak", days: 30 }),
  },
  
  // Mastery achievements
  {
    name: "SaaS Specialist",
    slug: "saas-specialist",
    description: "Complete all SaaS courses",
    icon: "briefcase",
    category: "mastery",
    xpReward: 300,
    requirement: JSON.stringify({ type: "category_mastery", category: "SaaS" }),
  },
  {
    name: "Marketing Maven",
    slug: "marketing-maven",
    description: "Complete all Marketing courses",
    icon: "megaphone",
    category: "mastery",
    xpReward: 300,
    requirement: JSON.stringify({ type: "category_mastery", category: "Marketing" }),
  },
  {
    name: "Business Strategist",
    slug: "business-strategist",
    description: "Complete all Business Strategy courses",
    icon: "trending-up",
    category: "mastery",
    xpReward: 300,
    requirement: JSON.stringify({ type: "category_mastery", category: "Business Strategy" }),
  },
  
  // Special achievements
  {
    name: "Early Adopter",
    slug: "early-adopter",
    description: "Join AI Prompts Academy",
    icon: "rocket",
    category: "special",
    xpReward: 25,
    requirement: JSON.stringify({ type: "signup", auto: true }),
  },
  {
    name: "Speed Learner",
    slug: "speed-learner",
    description: "Complete a course in under 2 hours",
    icon: "clock",
    category: "special",
    xpReward: 100,
    requirement: JSON.stringify({ type: "course_speed", hours: 2 }),
  },
  {
    name: "Night Owl",
    slug: "night-owl",
    description: "Complete 10 lessons after 10 PM",
    icon: "moon",
    category: "special",
    xpReward: 50,
    requirement: JSON.stringify({ type: "time_of_day", after: 22, count: 10 }),
  },
  {
    name: "Early Bird",
    slug: "early-bird",
    description: "Complete 10 lessons before 8 AM",
    icon: "sunrise",
    category: "special",
    xpReward: 50,
    requirement: JSON.stringify({ type: "time_of_day", before: 8, count: 10 }),
  },
];

async function seedAchievements() {
  console.log('🎯 Seeding achievements...\n');
  
  // Check if achievements already exist
  const existing = await getAllAchievements();
  if (existing.length > 0) {
    console.log(`✅ Achievements already seeded (${existing.length} found)`);
    return;
  }
  
  try {
    await bulkCreateAchievements(achievements);
    console.log(`✅ Successfully seeded ${achievements.length} achievements!\n`);
    
    console.log('Achievement Categories:');
    console.log(`  - Milestone: ${achievements.filter(a => a.category === 'milestone').length}`);
    console.log(`  - Streak: ${achievements.filter(a => a.category === 'streak').length}`);
    console.log(`  - Mastery: ${achievements.filter(a => a.category === 'mastery').length}`);
    console.log(`  - Special: ${achievements.filter(a => a.category === 'special').length}`);
  } catch (error) {
    console.error('❌ Error seeding achievements:', error);
    process.exit(1);
  }
  
  process.exit(0);
}

seedAchievements();
