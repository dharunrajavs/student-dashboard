const express = require('express');
const cors = require('cors');
const { GoogleGenerativeAI } = require('@google/generative-ai');
require('dotenv').config();

const app = express();
const PORT = process.env.PORT || 5002;

// Check if API key exists (don't crash, just warn)
let genAI = null;
let model = null;
let useAI = false;

if (process.env.GEMINI_API_KEY) {
  try {
    genAI = new GoogleGenerativeAI(process.env.GEMINI_API_KEY);
    model = genAI.getGenerativeModel({ model: 'gemini-2.0-flash' });
    useAI = true;
    console.log('✓ Gemini AI initialized successfully');
  } catch (err) {
    console.warn('Warning: Could not initialize Gemini AI:', err.message);
    console.log('Using fallback responses instead');
  }
} else {
  console.warn('Warning: GEMINI_API_KEY not set - using fallback responses');
  console.log('Get your free API key from: https://aistudio.google.com/app/apikey');
}

// System prompt for academic mentor
const SYSTEM_PROMPT = `You are a helpful AI academic mentor named "AcademicAI Assistant". 
Your role is to help students with:
- Study plans and time management strategies
- Subject-wise guidance and explanations
- Exam preparation tips and techniques
- Career advice and guidance
- Motivation and emotional support

Be supportive, encouraging, and provide actionable advice. 
Keep responses helpful and concise (under 300 words).
Use bullet points and formatting when helpful.`;

// Middleware - Allow all origins in production
const allowedOrigins = process.env.NODE_ENV === 'production'
  ? [/\.vercel\.app$/, /\.onrender\.com$/, /localhost/]
  : ['http://localhost:3000', 'http://localhost:3001', 'http://localhost:3002', 'http://localhost:3003', 'http://localhost:3004', 'http://localhost:3005'];

app.use(cors({
  origin: function(origin, callback) {
    // Allow requests with no origin (mobile apps, curl, etc)
    if (!origin) return callback(null, true);
    
    if (process.env.NODE_ENV === 'production') {
      // Check against regex patterns in production
      const allowed = allowedOrigins.some(pattern => 
        pattern instanceof RegExp ? pattern.test(origin) : pattern === origin
      );
      if (allowed) return callback(null, true);
    } else {
      // Check exact match in development
      if (allowedOrigins.includes(origin)) return callback(null, true);
    }
    callback(null, true); // Allow all for now
  },
  methods: ['GET', 'POST'],
  allowedHeaders: ['Content-Type', 'Authorization']
}));
app.use(express.json());

// Health check endpoint
app.get('/health', (req, res) => {
  res.json({ 
    status: 'ok', 
    message: 'Server is running', 
    ai: useAI ? 'Google Gemini' : 'Fallback mode',
    aiEnabled: useAI
  });
});

// Intelligent fallback responses
function getFallbackResponse(message) {
  const msg = message.toLowerCase();
  
  if (msg.includes('exam') || msg.includes('test') || msg.includes('preparation')) {
    return `**Exam Preparation Strategy** 📚

**2 Weeks Before:**
- Complete syllabus coverage
- Make summary notes and flashcards
- Identify weak areas

**1 Week Before:**
- Solve previous year papers
- Practice numerical problems
- Revise important topics daily

**2 Days Before:**
- Quick revision only
- Don't start new topics
- Get proper rest

**Exam Day Tips:**
- Good sleep the night before
- Read questions carefully before answering
- Manage time wisely - don't spend too long on one question
- Review answers if time permits

You've got this! 💪`;
  }
  
  if (msg.includes('study') || msg.includes('plan') || msg.includes('schedule')) {
    return `**Personalized Study Plan** 📖

**Daily Schedule:**
- **Morning (6-8 AM):** Best for difficult subjects - fresh mind
- **Afternoon (2-4 PM):** Revision and practice problems
- **Evening (6-8 PM):** Light reading and making notes

**Study Techniques:**
1. **Pomodoro Technique:** 25 min study + 5 min break
2. **Active Recall:** Test yourself instead of re-reading
3. **Spaced Repetition:** Review topics at increasing intervals

**Tips:**
- Study hardest subjects when most alert
- Take short breaks every 45-50 minutes
- Get 7-8 hours of sleep
- Stay hydrated and eat well

Would you like guidance for a specific subject?`;
  }
  
  if (msg.includes('motivat') || msg.includes('stress') || msg.includes('anxious') || msg.includes('worried') || msg.includes('fail')) {
    return `**You've Got This!** 💪

Remember:
- **Failure is temporary** - Every successful person faced setbacks
- **Progress over perfection** - Small steps lead to big achievements
- **You're not alone** - Ask for help when needed

**To Manage Stress:**
1. Take deep breaths (4-7-8 technique)
2. Break tasks into smaller chunks
3. Celebrate small wins
4. Exercise or take a walk
5. Talk to friends or family

**Motivational Quote:**
*"The only way to do great work is to love what you do. If you haven't found it yet, keep looking."* - Steve Jobs

I believe in you! What specific challenge are you facing?`;
  }
  
  if (msg.includes('career') || msg.includes('job') || msg.includes('future') || msg.includes('profession')) {
    return `**Career Guidance** 🎯

**Steps to Choose Your Career Path:**
1. **Self-Assessment:** Identify your interests, strengths, and values
2. **Research:** Explore industries and roles that match
3. **Skills:** Develop both technical and soft skills
4. **Network:** Connect with professionals in your field of interest
5. **Experience:** Internships, projects, and volunteering

**In-Demand Fields (2026):**
- Artificial Intelligence & Machine Learning
- Data Science & Analytics
- Cybersecurity
- Cloud Computing
- Healthcare Technology
- Renewable Energy

**Action Items:**
- Build a strong LinkedIn profile
- Work on personal projects
- Get relevant certifications
- Practice for interviews

What field interests you the most?`;
  }
  
  if (msg.includes('math') || msg.includes('calculus') || msg.includes('algebra')) {
    return `**Mathematics Study Tips** 🔢

**Key Strategies:**
1. **Practice Daily:** Math requires consistent practice
2. **Understand Concepts:** Don't just memorize formulas
3. **Solve Step-by-Step:** Write out every step clearly
4. **Use Multiple Resources:** Videos, textbooks, practice problems

**Common Mistakes to Avoid:**
- Skipping the basics
- Not checking your work
- Memorizing without understanding
- Avoiding difficult problems

**Recommended Approach:**
1. Read theory and examples
2. Solve practice problems
3. Attempt previous year questions
4. Time yourself for exam simulation

What specific math topic do you need help with?`;
  }
  
  if (msg.includes('programming') || msg.includes('coding') || msg.includes('code') || msg.includes('software')) {
    return `**Programming Learning Guide** 💻

**For Beginners:**
1. Start with Python or JavaScript
2. Learn basics: variables, loops, conditionals
3. Build small projects
4. Practice on LeetCode/HackerRank

**Best Learning Path:**
- **Week 1-2:** Syntax and basics
- **Week 3-4:** Data structures
- **Week 5-6:** Algorithms
- **Week 7-8:** Projects

**Tips:**
- Code daily, even for 30 minutes
- Read other people's code
- Don't copy-paste - type it out
- Debug systematically
- Build projects you're interested in

**Free Resources:**
- freeCodeCamp
- The Odin Project
- CS50 (Harvard)
- Codecademy

What programming language are you learning?`;
  }
  
  if (msg.includes('english') || msg.includes('writing') || msg.includes('essay')) {
    return `**English & Writing Skills** ✍️

**Improve Your Writing:**
1. **Read Daily:** Newspapers, books, articles
2. **Expand Vocabulary:** Learn 5 new words daily
3. **Practice Writing:** Journals, essays, summaries
4. **Get Feedback:** Have others review your work

**Essay Structure:**
- **Introduction:** Hook + thesis statement
- **Body Paragraphs:** Topic sentence + evidence + analysis
- **Conclusion:** Restate thesis + final thoughts

**Grammar Tips:**
- Use active voice
- Keep sentences concise
- Proofread multiple times
- Read your writing aloud

**Resources:**
- Grammarly (writing assistant)
- Purdue OWL (writing guides)
- Daily reading habit

What type of writing are you working on?`;
  }
  
  // Default response for any other query
  return `**I'm here to help!** 🎓

I can assist you with:
- 📚 **Study Plans:** Personalized schedules and strategies
- 📝 **Exam Preparation:** Tips and techniques
- 💼 **Career Guidance:** Future planning and skills
- 💪 **Motivation:** Support when you're stressed
- 📖 **Subject Help:** Math, Science, Programming, English, etc.

**Quick Tips:**
- Be specific in your questions for better answers
- Ask about particular subjects or topics
- Share your goals so I can help you achieve them

What would you like help with today?`;
}

// Chat endpoint
app.post('/chat', async (req, res) => {
  try {
    const { message } = req.body;

    if (!message) {
      return res.status(400).json({ error: 'Message is required' });
    }

    // Try Gemini AI first (if available)
    if (useAI && model) {
      try {
        const chat = model.startChat({
          history: [
            {
              role: 'user',
              parts: [{ text: 'You are an AI academic mentor. Please acknowledge and follow these instructions: ' + SYSTEM_PROMPT }],
            },
            {
              role: 'model',
              parts: [{ text: 'I understand! I am AcademicAI Assistant, ready to help students with study plans, subject guidance, exam preparation, career advice, and motivation. How can I help you today?' }],
            },
          ],
        });

        const result = await chat.sendMessage(message);
        const reply = result.response.text();
        return res.json({ reply, source: 'gemini' });
      } catch (aiError) {
        console.log('Gemini API error, using fallback:', aiError.message);
        // Use intelligent fallback
        const reply = getFallbackResponse(message);
        return res.json({ reply, source: 'fallback' });
      }
    } else {
      // AI not available, use fallback directly
      const reply = getFallbackResponse(message);
      return res.json({ reply, source: 'fallback' });
    }
  } catch (error) {
    console.error('Chat Error:', error.message);
    res.status(500).json({ 
      error: 'Failed to process message',
      details: error.message 
    });
  }
});

// Start server
app.listen(PORT, () => {
  console.log(`Server running on http://localhost:${PORT}`);
  console.log(`AI Mode: ${useAI ? 'Google Gemini ✓' : 'Fallback Responses (no API key)'}`);
});
