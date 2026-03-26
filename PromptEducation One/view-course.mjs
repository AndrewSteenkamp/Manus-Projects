import { getCourseBySlug, getPromptsByCourseId } from './server/db.js';

async function viewCourse() {
  const course = await getCourseBySlug('apps-build');
  console.log('Course:', JSON.stringify(course, null, 2));
  
  const prompts = await getPromptsByCourseId(course.id);
  console.log('\nTotal Prompts:', prompts.length);
  console.log('\nFirst 3 Prompts:');
  prompts.slice(0, 3).forEach((p, i) => {
    console.log(`\n${i + 1}. ${p.title}`);
    console.log(`   Question: ${p.question.substring(0, 150)}...`);
  });
  
  process.exit(0);
}

viewCourse();
