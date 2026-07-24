import React, { useState } from 'react';
import { 
  Bot, 
  FileText, 
  Brain, 
  Globe, 
  Calculator, 
  Terminal, 
  LayoutDashboard, 
  Cpu, 
  ShieldCheck, 
  Zap, 
  Layers, 
  Puzzle, 
  ChevronRight, 
  Mail, 
  CheckCircle2, 
  ArrowRight,
  Menu,
  X,
  Plus,
  Minus
} from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';

const rawAppUrl = import.meta.env.VITE_APP_URL || "https://ai-agent-frontend-120e.onrender.com";
const APP_URL = rawAppUrl.startsWith("http") ? rawAppUrl : `https://${rawAppUrl}`;
const API_URL = import.meta.env.VITE_API_URL || "https://ai-agent-backend-ev85.onrender.com";

// --- DATA DEFINITIONS ---

const TECH_LOGOS = [
  { name: 'OpenAI', icon: '🤖', desc: 'GPT-4o & Embeddings' },
  { name: 'LangChain', icon: '🦜', desc: 'Tool Orchestration' },
  { name: 'FastAPI', icon: '⚡', desc: 'Async High Performance' },
  { name: 'React', icon: '⚛️', desc: 'Interactive UI' },
  { name: 'ChromaDB', icon: '🌈', desc: 'Vector Search Engine' },
  { name: 'SQLite', icon: '🗄️', desc: 'ACID Persistence' },
  { name: 'TailwindCSS', icon: '🎨', desc: 'Modern Styling' },
];

const FEATURES = [
  {
    icon: Bot,
    title: '💬 AI Chat',
    desc: 'Context-aware conversational interface powered by state-of-the-art LLMs with full message persistence.',
    color: 'from-indigo-500 to-purple-500'
  },
  {
    icon: FileText,
    title: '📄 Document Intelligence',
    desc: 'Ingest PDF, TXT, DOCX, and CSV files effortlessly with automatic parsing and vector indexing.',
    color: 'from-purple-500 to-pink-500'
  },
  {
    icon: Brain,
    title: '🧠 Smart Memory',
    desc: 'Short-term and long-term memory buffer retaining recent chats, user preferences, and uploaded files.',
    color: 'from-pink-500 to-rose-500'
  },
  {
    icon: Globe,
    title: '🔎 Web Search',
    desc: 'Real-time web browsing capability for fetching live internet facts and external information.',
    color: 'from-cyan-500 to-blue-500'
  },
  {
    icon: Calculator,
    title: '🧮 Calculator',
    desc: 'Deterministic mathematical execution for complex equations without LLM hallucination.',
    color: 'from-blue-500 to-indigo-500'
  },
  {
    icon: Terminal,
    title: '🐍 Python Execution',
    desc: 'Dynamic code execution environment for data analysis, math computations, and custom scripts.',
    color: 'from-emerald-500 to-teal-500'
  },
  {
    icon: LayoutDashboard,
    title: '📊 Dashboard',
    desc: 'Comprehensive real-time analytics displaying chat counts, file metrics, and vector DB stats.',
    color: 'from-amber-500 to-orange-500'
  },
  {
    icon: Cpu,
    title: '⚡ Tool Orchestration',
    desc: 'Autonomous agent decision engine that selects, parameterizes, and runs tools dynamically.',
    color: 'from-violet-500 to-purple-600'
  },
];

const HOW_IT_WORKS = [
  { step: '01', title: 'User Input', desc: 'User submits a prompt or uploads a document into the interface.' },
  { step: '02', title: 'AI Agent Evaluation', desc: 'Agent evaluates intent and inspects available registered tools.' },
  { step: '03', title: 'Tool Selection', desc: 'Dynamically picks Web Search, Vector RAG, Python Runner, or Math Engine.' },
  { step: '04', title: 'Execution & Synthesis', desc: 'Executes the tool, gathers results, and synthesizes a smart response.' },
];

const WHY_CHOOSE = [
  {
    icon: Zap,
    title: 'Fast & Accurate',
    desc: 'Sub-second response retrieval with optimized vector indices and async API endpoints.'
  },
  {
    icon: ShieldCheck,
    title: 'Secure & Isolated',
    desc: 'Sanitized file uploads, safe SQL queries, and sandboxed code execution layers.'
  },
  {
    icon: Layers,
    title: 'Clean Architecture',
    desc: 'Strict separation of database, schemas, services, and routers for enterprise maintainability.'
  },
  {
    icon: Puzzle,
    title: 'Modular & Extensible',
    desc: 'Easily plug in custom tools, new vector stores, or alternative LLM providers in minutes.'
  },
];

const TECH_CATEGORIES = [
  { category: 'Frontend', items: ['React 18', 'TailwindCSS v4', 'Vite', 'Lucide Icons', 'Framer Motion'] },
  { category: 'Backend', items: ['FastAPI', 'Python 3.12', 'Uvicorn', 'Pydantic v2', 'REST APIs'] },
  { category: 'AI & Vectors', items: ['LangChain', 'OpenAI / Gemini', 'ChromaDB', 'Sentence-Transformers'] },
  { category: 'Database & Infra', items: ['SQLite', 'SQLAlchemy 2.0', 'Vercel / Render', 'PyPDF2 & Pandas'] },
];

const TESTIMONIALS = [
  {
    name: 'Alex Rivera',
    role: 'Lead AI Engineer @ TechFlow',
    avatar: 'https://images.unsplash.com/photo-1534528741775-53994a69daeb?w=150&auto=format&fit=crop&q=80',
    quote: 'The tool orchestration architecture is incredibly clean! Plugging in custom Python tools and ChromaDB vector search took less than an hour.'
  },
  {
    name: 'Sarah Chen',
    role: 'Full Stack Architect @ DataPulse',
    avatar: 'https://images.unsplash.com/photo-1507003211169-0a1dd7228f2d?w=150&auto=format&fit=crop&q=80',
    quote: 'FastAPI combined with Streamlit and ChromaDB makes document Q&A feel instant. The RAG retrieval precision is top tier.'
  },
  {
    name: 'Michael Vance',
    role: 'Product Lead @ Synthetix AI',
    avatar: 'https://images.unsplash.com/photo-1500648767791-00dcc994a43e?w=150&auto=format&fit=crop&q=80',
    quote: 'A masterpiece of modern AI system design. The UI is sleek and the backend architecture is enterprise-grade.'
  },
];

const FAQS = [
  {
    q: 'What is Tool Orchestration?',
    a: 'Tool Orchestration allows the AI Agent to autonomously decide when and how to call external utilities (like web search, python interpreter, database queries, or calculators) to solve complex user requests accurately.'
  },
  {
    q: 'How does Memory work?',
    a: 'The system uses a hybrid memory pipeline combining SQLite conversation history persistence with a lightweight JSON session memory buffer that tracks active document contexts and recent interactions.'
  },
  {
    q: 'Which file formats are supported?',
    a: 'You can upload PDF (.pdf), Plaintext (.txt), Microsoft Word (.docx), and CSV Data (.csv) files for automatic chunking and vector embedding.'
  },
  {
    q: 'Is the project open source & customizable?',
    a: 'Yes! The architecture is completely modular. You can plug in alternative vector databases (Pinecone, Qdrant) or swap LLM providers effortlessly.'
  },
  {
    q: 'Can I deploy it myself?',
    a: 'Absolutely. The FastAPI backend can be deployed to Render, AWS, or Docker containers, while the frontend deploys seamlessly to Vercel or Netlify.'
  },
];

export default function App() {
  const [mobileMenuOpen, setMobileMenuOpen] = useState(false);
  const [openFaq, setOpenFaq] = useState(null);

  const toggleFaq = (index) => {
    setOpenFaq(openFaq === index ? null : index);
  };

  return (
    <div className="min-h-screen bg-[#0F172A] text-slate-100 relative selection:bg-purple-500 selection:text-white">
      {/* Background Floating Blobs */}
      <div className="fixed inset-0 overflow-hidden pointer-events-none z-0">
        <div className="absolute -top-40 -left-40 w-96 h-96 bg-purple-600/20 rounded-full blur-[128px] animate-pulse" />
        <div className="absolute top-1/3 -right-40 w-96 h-96 bg-cyan-500/20 rounded-full blur-[128px] animate-pulse" />
        <div className="absolute -bottom-40 left-1/3 w-96 h-96 bg-indigo-600/20 rounded-full blur-[128px] animate-pulse" />
      </div>

      {/* ---------------- NAVIGATION ---------------- */}
      <nav className="fixed top-0 left-0 right-0 z-50 glass-nav py-4 px-6 md:px-12 transition-all">
        <div className="max-w-7xl mx-auto flex items-center justify-between">
          <div className="flex items-center space-x-3 cursor-pointer">
            <div className="w-10 h-10 rounded-xl bg-gradient-to-tr from-indigo-500 via-purple-500 to-cyan-400 p-[2px] shadow-lg glow-purple">
              <div className="w-full h-full bg-[#0F172A] rounded-[10px] flex items-center justify-center">
                <Bot className="w-6 h-6 text-cyan-400" />
              </div>
            </div>
            <span className="font-bold text-xl tracking-tight bg-gradient-to-r from-white via-slate-200 to-slate-400 bg-clip-text text-transparent">
              AI Agent <span className="text-cyan-400 text-xs font-semibold px-2 py-0.5 rounded-full bg-cyan-400/10 border border-cyan-400/20 ml-1">v1.0</span>
            </span>
          </div>

          <div className="hidden md:flex items-center space-x-8 text-sm font-medium text-slate-300">
            <a href="#features" className="hover:text-cyan-400 transition-colors">Features</a>
            <a href="#how-it-works" className="hover:text-cyan-400 transition-colors">How It Works</a>
            <a href="#tech-stack" className="hover:text-cyan-400 transition-colors">Tech Stack</a>
            <a href="#dashboard" className="hover:text-cyan-400 transition-colors">Dashboard</a>
            <a href="#faq" className="hover:text-cyan-400 transition-colors">FAQ</a>
          </div>

          <div className="hidden md:flex items-center space-x-4">
            <a 
              href={APP_URL} 
              target="_blank" 
              rel="noreferrer"
              className="px-5 py-2.5 rounded-xl bg-gradient-to-r from-indigo-600 via-purple-600 to-cyan-500 hover:opacity-90 font-medium text-sm transition-all shadow-lg hover:shadow-cyan-500/25 active:scale-95"
            >
              Launch App
            </a>
          </div>

          <button 
            className="md:hidden text-slate-300 hover:text-white"
            onClick={() => setMobileMenuOpen(!mobileMenuOpen)}
          >
            {mobileMenuOpen ? <X className="w-6 h-6" /> : <Menu className="w-6 h-6" />}
          </button>
        </div>

        {/* Mobile Menu */}
        {mobileMenuOpen && (
          <motion.div 
            initial={{ opacity: 0, y: -20 }}
            animate={{ opacity: 1, y: 0 }}
            className="md:hidden glass-card mt-4 p-6 rounded-2xl flex flex-col space-y-4 text-center"
          >
            <a href="#features" onClick={() => setMobileMenuOpen(false)}>Features</a>
            <a href="#how-it-works" onClick={() => setMobileMenuOpen(false)}>How It Works</a>
            <a href="#tech-stack" onClick={() => setMobileMenuOpen(false)}>Tech Stack</a>
            <a href="#dashboard" onClick={() => setMobileMenuOpen(false)}>Dashboard</a>
            <a href="#faq" onClick={() => setMobileMenuOpen(false)}>FAQ</a>
            <a 
              href={APP_URL} 
              className="px-5 py-2.5 rounded-xl bg-gradient-to-r from-indigo-600 to-cyan-500 text-white font-medium"
            >
              Launch App
            </a>
          </motion.div>
        )}
      </nav>

      {/* ---------------- 1. HERO SECTION ---------------- */}
      <section className="pt-36 pb-20 px-6 md:px-12 max-w-7xl mx-auto relative z-10">
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-12 items-center">
          <motion.div 
            initial={{ opacity: 0, x: -30 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ duration: 0.6 }}
            className="space-y-6 text-center lg:text-left"
          >
            <div className="inline-flex items-center space-x-2 px-3.5 py-1.5 rounded-full bg-purple-500/10 border border-purple-500/20 text-purple-300 text-xs font-semibold">
              <Zap className="w-3.5 h-3.5 text-cyan-400 animate-pulse" />
              <span>Next-Gen Tool Orchestration Agent</span>
            </div>

            <h1 className="text-4xl sm:text-5xl lg:text-6xl font-extrabold tracking-tight leading-tight">
              Your Intelligent AI Agent That <span className="text-gradient">Thinks, Searches,</span> & Acts.
            </h1>

            <p className="text-slate-300 text-lg md:text-xl font-normal leading-relaxed max-w-2xl mx-auto lg:mx-0">
              An AI-powered assistant capable of tool calling, document understanding, memory, and real-time automation.
            </p>

            <div className="flex flex-col sm:flex-row items-center justify-center lg:justify-start gap-4 pt-2">
              <a 
                href={APP_URL} 
                target="_blank"
                rel="noreferrer"
                className="w-full sm:w-auto px-8 py-4 rounded-xl bg-gradient-to-r from-indigo-600 via-purple-600 to-cyan-500 hover:opacity-90 font-semibold text-base transition-all shadow-xl hover:shadow-purple-500/30 flex items-center justify-center space-x-2 group"
              >
                <span>Get Started Free</span>
                <ArrowRight className="w-5 h-5 group-hover:translate-x-1 transition-transform" />
              </a>

              <a 
                href="#dashboard" 
                className="w-full sm:w-auto px-8 py-4 rounded-xl glass-card hover:bg-slate-800/80 font-semibold text-base text-slate-200 transition-all border border-slate-700 flex items-center justify-center"
              >
                View Live Demo
              </a>
            </div>

            <div className="pt-6 flex items-center justify-center lg:justify-start space-x-6 text-xs text-slate-400">
              <div className="flex items-center space-x-1.5">
                <CheckCircle2 className="w-4 h-4 text-emerald-400" />
                <span>Zero Latency RAG</span>
              </div>
              <div className="flex items-center space-x-1.5">
                <CheckCircle2 className="w-4 h-4 text-emerald-400" />
                <span>ChromaDB Vector Store</span>
              </div>
              <div className="flex items-center space-x-1.5">
                <CheckCircle2 className="w-4 h-4 text-emerald-400" />
                <span>FastAPI Async Core</span>
              </div>
            </div>
          </motion.div>

          {/* Animated Interactive Mockup */}
          <motion.div 
            initial={{ opacity: 0, scale: 0.9 }}
            animate={{ opacity: 1, scale: 1 }}
            transition={{ duration: 0.6, delay: 0.2 }}
            className="relative"
          >
            <div className="glass-card rounded-2xl p-6 shadow-2xl glow-purple relative overflow-hidden border border-slate-700/60">
              {/* Top Window Bar */}
              <div className="flex items-center justify-between pb-4 border-b border-slate-800 mb-4">
                <div className="flex space-x-2">
                  <div className="w-3 h-3 rounded-full bg-rose-500/80" />
                  <div className="w-3 h-3 rounded-full bg-amber-500/80" />
                  <div className="w-3 h-3 rounded-full bg-emerald-500/80" />
                </div>
                <div className="text-xs font-mono text-slate-400 bg-slate-900/60 px-3 py-1 rounded-md border border-slate-800">
                  agent_orchestrator.py
                </div>
              </div>

              {/* Chat Simulation */}
              <div className="space-y-4 font-sans text-sm">
                <div className="flex items-start space-x-3">
                  <div className="w-8 h-8 rounded-lg bg-indigo-500/20 text-indigo-400 flex items-center justify-center flex-shrink-0 border border-indigo-500/30">
                    U
                  </div>
                  <div className="bg-slate-800/90 rounded-2xl p-3.5 text-slate-200 border border-slate-700 max-w-[85%]">
                    Can you extract financial data from Q3_Report.pdf and compute total revenue?
                  </div>
                </div>

                <div className="flex items-start space-x-3">
                  <div className="w-8 h-8 rounded-lg bg-purple-500/20 text-cyan-400 flex items-center justify-center flex-shrink-0 border border-purple-500/30">
                    <Bot className="w-4 h-4" />
                  </div>
                  <div className="space-y-2 max-w-[85%]">
                    {/* Tool Badge */}
                    <div className="inline-flex items-center space-x-2 px-3 py-1 rounded-lg bg-cyan-950/60 border border-cyan-500/30 text-cyan-300 text-xs font-mono">
                      <Cpu className="w-3.5 h-3.5 text-cyan-400 animate-spin" />
                      <span>Executing Tool: PDF_Reader + Python_Calculator</span>
                    </div>
                    <div className="bg-slate-900/90 rounded-2xl p-3.5 text-slate-200 border border-slate-800">
                      📄 Extracted 3 text chunks from <strong>Q3_Report.pdf</strong> via ChromaDB RAG.
                      <br /><br />
                      🧮 <code>total_revenue = sum([1.25M, 3.40M, 0.85M])</code>
                      <br />
                      <strong>Result: $5,500,000 USD</strong>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </motion.div>
        </div>
      </section>

      {/* ---------------- 2. TRUSTED TECHNOLOGIES ---------------- */}
      <section className="py-12 border-y border-slate-800/80 bg-slate-900/40">
        <div className="max-w-7xl mx-auto px-6 text-center">
          <p className="text-xs uppercase tracking-widest font-semibold text-slate-400 mb-8">
            Built With Industry-Leading Technologies
          </p>
          <div className="grid grid-cols-2 sm:grid-cols-4 lg:grid-cols-7 gap-4">
            {TECH_LOGOS.map((item, idx) => (
              <div key={idx} className="glass-card p-4 rounded-xl flex flex-col items-center justify-center hover:border-purple-500/50 transition-all group">
                <span className="text-2xl mb-1 group-hover:scale-110 transition-transform">{item.icon}</span>
                <span className="font-bold text-sm text-slate-200">{item.name}</span>
                <span className="text-[10px] text-slate-400">{item.desc}</span>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* ---------------- 3. FEATURES SECTION ---------------- */}
      <section id="features" className="py-24 px-6 md:px-12 max-w-7xl mx-auto relative">
        <div className="text-center max-w-3xl mx-auto mb-16 space-y-4">
          <h2 className="text-3xl md:text-4xl font-extrabold">
            Supercharged Capabilities for <span className="text-gradient">Every Workflow</span>
          </h2>
          <p className="text-slate-400 text-base md:text-lg">
            An end-to-end suite of tools and retrieval systems working seamlessly together.
          </p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          {FEATURES.map((feat, idx) => {
            const Icon = feat.icon;
            return (
              <motion.div 
                key={idx}
                whileHover={{ y: -8 }}
                className="glass-card p-6 rounded-2xl border border-slate-800 hover:border-purple-500/40 transition-all relative overflow-hidden group"
              >
                <div className={`w-12 h-12 rounded-xl bg-gradient-to-tr ${feat.color} p-[1px] mb-5`}>
                  <div className="w-full h-full bg-[#0F172A] rounded-[11px] flex items-center justify-center">
                    <Icon className="w-6 h-6 text-white" />
                  </div>
                </div>
                <h3 className="text-xl font-bold text-white mb-2">{feat.title}</h3>
                <p className="text-slate-400 text-sm leading-relaxed">{feat.desc}</p>
              </motion.div>
            );
          })}
        </div>
      </section>

      {/* ---------------- 4. HOW IT WORKS ---------------- */}
      <section id="how-it-works" className="py-24 px-6 md:px-12 bg-slate-900/60 border-y border-slate-800/80">
        <div className="max-w-7xl mx-auto">
          <div className="text-center max-w-2xl mx-auto mb-16 space-y-4">
            <h2 className="text-3xl md:text-4xl font-extrabold">
              How The Agent <span className="text-gradient">Orchestrates</span>
            </h2>
            <p className="text-slate-400 text-base">
              A transparent four-step loop that turns ambiguous requests into precise answers.
            </p>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-4 gap-6 relative">
            {HOW_IT_WORKS.map((item, idx) => (
              <div key={idx} className="glass-card p-6 rounded-2xl relative border border-slate-800">
                <span className="text-4xl font-black text-slate-700/60 block mb-4 font-mono">{item.step}</span>
                <h3 className="text-lg font-bold text-white mb-2">{item.title}</h3>
                <p className="text-slate-400 text-xs leading-relaxed">{item.desc}</p>
                {idx < 3 && (
                  <ChevronRight className="hidden md:block absolute -right-4 top-1/2 -translate-y-1/2 text-purple-400 z-10 w-6 h-6" />
                )}
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* ---------------- 5. WHY CHOOSE ---------------- */}
      <section className="py-24 px-6 md:px-12 max-w-7xl mx-auto">
        <div className="text-center max-w-2xl mx-auto mb-16 space-y-4">
          <h2 className="text-3xl md:text-4xl font-extrabold">
            Why Build With <span className="text-gradient">This Architecture</span>
          </h2>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          {WHY_CHOOSE.map((item, idx) => {
            const Icon = item.icon;
            return (
              <div key={idx} className="glass-card p-6 rounded-2xl border border-slate-800 text-center">
                <div className="w-12 h-12 rounded-xl bg-purple-500/10 text-purple-400 flex items-center justify-center mx-auto mb-4 border border-purple-500/20">
                  <Icon className="w-6 h-6" />
                </div>
                <h3 className="text-lg font-bold text-white mb-2">{item.title}</h3>
                <p className="text-slate-400 text-xs leading-relaxed">{item.desc}</p>
              </div>
            );
          })}
        </div>
      </section>

      {/* ---------------- 6. TECH STACK ---------------- */}
      <section id="tech-stack" className="py-24 px-6 md:px-12 bg-slate-900/60 border-y border-slate-800/80">
        <div className="max-w-7xl mx-auto">
          <div className="text-center max-w-2xl mx-auto mb-16">
            <h2 className="text-3xl md:text-4xl font-extrabold">
              Complete Production <span className="text-gradient">Tech Stack</span>
            </h2>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
            {TECH_CATEGORIES.map((cat, idx) => (
              <div key={idx} className="glass-card p-6 rounded-2xl border border-slate-800">
                <h3 className="text-lg font-bold text-cyan-400 mb-4 border-b border-slate-800 pb-2">{cat.category}</h3>
                <ul className="space-y-2.5">
                  {cat.items.map((item, i) => (
                    <li key={i} className="flex items-center space-x-2 text-slate-300 text-sm">
                      <CheckCircle2 className="w-4 h-4 text-purple-400" />
                      <span>{item}</span>
                    </li>
                  ))}
                </ul>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* ---------------- 7. DASHBOARD PREVIEW ---------------- */}
      <section id="dashboard" className="py-24 px-6 md:px-12 max-w-7xl mx-auto">
        <div className="text-center max-w-2xl mx-auto mb-16 space-y-4">
          <h2 className="text-3xl md:text-4xl font-extrabold">
            Real-Time <span className="text-gradient">Analytics & Metrics</span>
          </h2>
          <p className="text-slate-400 text-base">
            Monitor chat activity, memory buffers, and ChromaDB vector chunk statistics.
          </p>
        </div>

        <div className="glass-card p-8 rounded-3xl border border-slate-700/60 shadow-2xl glow-cyan">
          <div className="grid grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
            <div className="bg-slate-900/80 p-5 rounded-2xl border border-slate-800">
              <span className="text-slate-400 text-xs font-medium">Total Chats</span>
              <p className="text-3xl font-black text-white mt-1">24</p>
            </div>
            <div className="bg-slate-900/80 p-5 rounded-2xl border border-slate-800">
              <span className="text-slate-400 text-xs font-medium">Total Messages</span>
              <p className="text-3xl font-black text-purple-400 mt-1">142</p>
            </div>
            <div className="bg-slate-900/80 p-5 rounded-2xl border border-slate-800">
              <span className="text-slate-400 text-xs font-medium">Uploaded Files</span>
              <p className="text-3xl font-black text-cyan-400 mt-1">8</p>
            </div>
            <div className="bg-slate-900/80 p-5 rounded-2xl border border-slate-800">
              <span className="text-slate-400 text-xs font-medium">Vector DB Chunks</span>
              <p className="text-3xl font-black text-emerald-400 mt-1">356</p>
            </div>
          </div>

          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            <div className="bg-slate-900/60 p-6 rounded-2xl border border-slate-800">
              <h4 className="text-sm font-bold text-slate-200 mb-4">Recent Uploaded Documents</h4>
              <div className="space-y-3 font-mono text-xs">
                <div className="flex justify-between p-3 rounded-lg bg-slate-800/60 border border-slate-700/50">
                  <span className="text-slate-300">📄 Sathvik_MV_Resume.pdf</span>
                  <span className="text-cyan-400">48.1 KB</span>
                </div>
                <div className="flex justify-between p-3 rounded-lg bg-slate-800/60 border border-slate-700/50">
                  <span className="text-slate-300">📊 Q3_Financial_Analysis.csv</span>
                  <span className="text-cyan-400">124.5 KB</span>
                </div>
                <div className="flex justify-between p-3 rounded-lg bg-slate-800/60 border border-slate-700/50">
                  <span className="text-slate-300">📝 System_Architecture.docx</span>
                  <span className="text-cyan-400">82.3 KB</span>
                </div>
              </div>
            </div>

            <div className="bg-slate-900/60 p-6 rounded-2xl border border-slate-800">
              <h4 className="text-sm font-bold text-slate-200 mb-4">Vector Database Status</h4>
              <div className="space-y-4 text-xs">
                <div>
                  <div className="flex justify-between text-slate-300 mb-1">
                    <span>ChromaDB Index Capacity</span>
                    <span>72%</span>
                  </div>
                  <div className="w-full bg-slate-800 h-2 rounded-full overflow-hidden">
                    <div className="bg-gradient-to-r from-purple-500 to-cyan-400 h-full w-[72%]" />
                  </div>
                </div>
                <div>
                  <div className="flex justify-between text-slate-300 mb-1">
                    <span>Memory Buffer Load</span>
                    <span>35%</span>
                  </div>
                  <div className="w-full bg-slate-800 h-2 rounded-full overflow-hidden">
                    <div className="bg-gradient-to-r from-indigo-500 to-purple-500 h-full w-[35%]" />
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* ---------------- 8. TESTIMONIALS ---------------- */}
      <section className="py-24 px-6 md:px-12 bg-slate-900/60 border-y border-slate-800/80">
        <div className="max-w-7xl mx-auto">
          <div className="text-center max-w-2xl mx-auto mb-16">
            <h2 className="text-3xl md:text-4xl font-extrabold">
              Loved By <span className="text-gradient">Engineers & Researchers</span>
            </h2>
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            {TESTIMONIALS.map((item, idx) => (
              <div key={idx} className="glass-card p-6 rounded-2xl border border-slate-800 flex flex-col justify-between">
                <p className="text-slate-300 text-sm leading-relaxed mb-6 italic">"{item.quote}"</p>
                <div className="flex items-center space-x-3">
                  <img src={item.avatar} alt={item.name} className="w-10 h-10 rounded-full object-cover border border-purple-400/30" />
                  <div>
                    <h4 className="text-sm font-bold text-white">{item.name}</h4>
                    <span className="text-xs text-slate-400">{item.role}</span>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* ---------------- 9. FAQ ---------------- */}
      <section id="faq" className="py-24 px-6 md:px-12 max-w-4xl mx-auto">
        <div className="text-center mb-16">
          <h2 className="text-3xl md:text-4xl font-extrabold">
            Frequently Asked <span className="text-gradient">Questions</span>
          </h2>
        </div>

        <div className="space-y-4">
          {FAQS.map((faq, idx) => (
            <div key={idx} className="glass-card rounded-2xl border border-slate-800 overflow-hidden">
              <button 
                onClick={() => toggleFaq(idx)}
                className="w-full p-6 text-left flex items-center justify-between font-semibold text-slate-200 hover:text-white"
              >
                <span>{faq.q}</span>
                {openFaq === idx ? <Minus className="w-5 h-5 text-purple-400" /> : <Plus className="w-5 h-5 text-slate-400" />}
              </button>
              <AnimatePresence>
                {openFaq === idx && (
                  <motion.div 
                    initial={{ height: 0, opacity: 0 }}
                    animate={{ height: 'auto', opacity: 1 }}
                    exit={{ height: 0, opacity: 0 }}
                    className="px-6 pb-6 text-slate-400 text-sm leading-relaxed border-t border-slate-800/60 pt-4"
                  >
                    {faq.a}
                  </motion.div>
                )}
              </AnimatePresence>
            </div>
          ))}
        </div>
      </section>

      {/* ---------------- 10. CALL TO ACTION ---------------- */}
      <section className="py-20 px-6 md:px-12 max-w-5xl mx-auto text-center">
        <div className="glass-card p-12 rounded-3xl border border-slate-700/60 relative overflow-hidden glow-purple">
          <h2 className="text-3xl sm:text-4xl font-extrabold text-white mb-4">
            Ready to Experience Intelligent AI?
          </h2>
          <p className="text-slate-300 max-w-xl mx-auto mb-8 text-base">
            Start interacting with document RAG, vector search, and tool orchestration today.
          </p>

          <div className="flex flex-col sm:flex-row items-center justify-center gap-4">
            <a 
              href={APP_URL} 
              target="_blank" 
              rel="noreferrer"
              className="w-full sm:w-auto px-8 py-4 rounded-xl bg-gradient-to-r from-indigo-600 via-purple-600 to-cyan-500 hover:opacity-90 font-semibold text-base transition-all shadow-xl"
            >
              Get Started Now
            </a>
            <a 
              href="https://github.com" 
              target="_blank" 
              rel="noreferrer"
              className="w-full sm:w-auto px-8 py-4 rounded-xl glass-card hover:bg-slate-800/80 font-semibold text-base text-slate-200 border border-slate-700 flex items-center justify-center space-x-2"
            >
              <svg className="w-5 h-5 fill-current" viewBox="0 0 24 24"><path d="M12 0C5.37 0 0 5.37 0 12c0 5.31 3.435 9.795 8.205 11.385.6.105.825-.255.825-.57 0-.285-.015-1.23-.015-2.235-3.015.555-3.795-.735-4.035-1.41-.135-.345-.72-1.41-1.23-1.695-.42-.225-1.02-.78-.015-.795.945-.015 1.62.87 1.845 1.23 1.08 1.815 2.805 1.305 3.495.99.105-.78.42-1.305.765-1.605-2.67-.3-5.46-1.335-5.46-5.925 0-1.305.465-2.385 1.23-3.225-.12-.3-.54-1.53.12-3.18 0 0 1.005-.315 3.3 1.23.96-.27 1.98-.405 3-.405s2.04.135 3 .405c2.295-1.56 3.3-1.23 3.3-1.23.66 1.65.24 2.88.12 3.18.765.84 1.23 1.905 1.23 3.225 0 4.605-2.805 5.625-5.475 5.925.435.375.81 1.095.81 2.22 0 1.605-.015 2.895-.015 3.3 0 .315.225.69.825.57A12.02 12.02 0 0024 12c0-6.63-5.37-12-12-12z"/></svg>
              <span>View GitHub</span>
            </a>
          </div>
        </div>
      </section>

      {/* ---------------- 11. FOOTER ---------------- */}
      <footer className="border-t border-slate-800 py-12 px-6 md:px-12 bg-slate-950 text-slate-400 text-sm">
        <div className="max-w-7xl mx-auto flex flex-col md:flex-row items-center justify-between gap-6">
          <div className="flex items-center space-x-3">
            <Bot className="w-6 h-6 text-cyan-400" />
            <span className="font-bold text-slate-200">AI Agent with Tool Orchestration</span>
          </div>

          <div className="flex items-center space-x-6">
            <a href="https://github.com" target="_blank" rel="noreferrer" className="hover:text-white transition-colors">
              <svg className="w-5 h-5 fill-current" viewBox="0 0 24 24"><path d="M12 0C5.37 0 0 5.37 0 12c0 5.31 3.435 9.795 8.205 11.385.6.105.825-.255.825-.57 0-.285-.015-1.23-.015-2.235-3.015.555-3.795-.735-4.035-1.41-.135-.345-.72-1.41-1.23-1.695-.42-.225-1.02-.78-.015-.795.945-.015 1.62.87 1.845 1.23 1.08 1.815 2.805 1.305 3.495.99.105-.78.42-1.305.765-1.605-2.67-.3-5.46-1.335-5.46-5.925 0-1.305.465-2.385 1.23-3.225-.12-.3-.54-1.53.12-3.18 0 0 1.005-.315 3.3 1.23.96-.27 1.98-.405 3-.405s2.04.135 3 .405c2.295-1.56 3.3-1.23 3.3-1.23.66 1.65.24 2.88.12 3.18.765.84 1.23 1.905 1.23 3.225 0 4.605-2.805 5.625-5.475 5.925.435.375.81 1.095.81 2.22 0 1.605-.015 2.895-.015 3.3 0 .315.225.69.825.57A12.02 12.02 0 0024 12c0-6.63-5.37-12-12-12z"/></svg>
            </a>
            <a href="https://linkedin.com" target="_blank" rel="noreferrer" className="hover:text-white transition-colors">
              <svg className="w-5 h-5 fill-current" viewBox="0 0 24 24"><path d="M19 0h-14c-2.761 0-5 2.239-5 5v14c0 2.761 2.239 5 5 5h14c2.762 0 5-2.239 5-5v-14c0-2.761-2.238-5-5-5zm-11 19h-3v-11h3v11zm-1.5-12.268c-.966 0-1.75-.79-1.75-1.764s.784-1.764 1.75-1.764 1.75.79 1.75 1.764-.783 1.764-1.75 1.764zm13.5 12.268h-3v-5.604c0-3.368-4-3.113-4 0v5.604h-3v-11h3v1.765c1.396-2.586 7-2.777 7 2.476v6.759z"/></svg>
            </a>
            <a href="mailto:contact@ai-agent.com" className="hover:text-white transition-colors">
              <Mail className="w-5 h-5" />
            </a>
          </div>

          <p className="text-xs text-slate-500">
            © {new Date().getFullYear()} AI Agent Project. All rights reserved.
          </p>
        </div>
      </footer>
    </div>
  );
}
