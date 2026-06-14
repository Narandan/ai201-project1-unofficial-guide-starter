# Project 1 Planning: The Unofficial Guide

> Write this document before you write any pipeline code.
> Your spec and architecture diagram are what you'll use to direct AI tools (Claude, Copilot, etc.) to generate your implementation — the more specific they are, the more useful the generated code will be.
> Update the Retrieval Approach and Chunking Strategy sections if you change your approach during implementation.
> Update this file before starting any stretch features.

---

## Domain

<!-- What domain did you choose? Why is this knowledge valuable and hard to find through official channels? -->
FSU Computer Science department — professor teaching styles, course difficulty, exam formats, and workload as reported by students. This knowledge is valuable because official sources (course catalogs, department websites) describe what courses cover but never tell you what it's actually like to take them. Students rely on word-of-mouth and scattered Reddit threads to make registration decisions.

---

## Documents

<!-- List your specific sources: URLs, subreddit names, forum threads, or file descriptions.
     Aim for at least 10 sources that together cover different subtopics or perspectives within your domain. -->

| # | --------------Source----------- | ---------Description-------------- | ----------------------URL or location-------------------- |
| - | ------------------------------- | ---------------------------------- | --------------------------------------------------------- |
| 1 | Rate My Professors              | Reviews for David Gaitros          | documents/rmp_gaitros_david.txt                           |
| 2 | Rate My Professors              | Reviews for Christopher Mills      | documents/rmp_mills_christopher.txt                       |
| 3 | Rate My Professors              | Reviews for Andy Wang              | documents/rmp_wang_andy.txt                               |
| 4 | Rate My Professors              | Reviews for Xin Yuan               | documents/rmp_yuan_xin.txt                                |
| 5 | Reddit r/FloridaStateUniversity | "If you're a professor... " thread | documents/reddit_if_your_a_professor_and_reading_this.txt |
| 6 | Reddit r/FloridaStateUniversity | Professor positivity thread        | documents/reddit_professor_positivity_thread.txt          |
| 7 | Reddit r/FloridaStateUniversity | "State of CS at FSU" thread        | documents/reddit_the_state_of_computer_science_at_fsu.txt |
| 8 | FSU CS Website                  | Undergraduate department overview  | documents/fsu_edu_undergraduate_department_of_computer_science.txt|
| 9 | FSU CS Website                  | BS degree program outcomes         | documents/fsu_edu_bs_degree_program_mission_educational_objectives_student_outcomes.txt |
| 10| FSU CS Website                  | Program guide for CS BA            | documents/fsu_edu_program_guide_computer_science_ba.txt   |

---

## Chunking Strategy

<!-- How will you split documents into chunks?
     State your chunk size (in tokens or characters), overlap size, and explain why those
     numbers fit the structure of your documents.
     A review-heavy corpus warrants different chunking than a long FAQ. -->

     Chunk size: 400 characters
     Each review is short and self-contained — the useful signal is in one paragraph. 400 characters captures a full review with its metadata (course code, ratings) without merging two separate reviews together.

     Overlap: 50 characters
     Small overlap because reviews are independent — you don't need much continuity between them. Just enough to catch a review that gets clipped at a boundary.
     
     Reasoning: The documents are review-style text where each unit of meaning is one student's opinion about one course/professor. Larger chunks (800+) would merge multiple reviews, diluting specific claims. Smaller chunks (100-200) would split a single review across two chunks, making neither retrievable on its own.

---

## Retrieval Approach

<!-- Which embedding model are you using (e.g., all-MiniLM-L6-v2 via sentence-transformers)?
     How many chunks will you retrieve per query (top-k)?
     If you were deploying this for real users and cost wasn't a constraint, what tradeoffs
     would you weigh in choosing a different embedding model — context length, multilingual
     support, accuracy on domain-specific text, latency? -->

Embedding model: all-MiniLM-L6-v2 via sentence-transformers (runs locally, no API key)

Top-k: 5

Production tradeoff reflection: For production I'd weigh OpenAI's text-embedding-3-large for accuracy vs. cost per query, and consider a multilingual model if the user base included non-English speakers. Context length isn't a concern here since reviews are short, but would matter for longer documents like syllabi or handbooks.

---

## Evaluation Plan

<!-- List your 5 test questions with their expected correct answers.
     Questions should be specific enough that you can judge whether the system's response
     is right or wrong. "What are good dining halls?" is too vague.
     "What do students say about wait times at [dining hall name] during lunch?" is testable. -->

| # | -------------------------Question--------------------------------- | --------------------Expected answer------------------------------- |
|---|--------------------------------------------------------------------| ------------------------------------------------------------------ |
| 1 | What do students say about David Gaitros's teaching style?         | Lectures aren't always helpful but he's responsive to emails, posts detailed YouTube videos, assignments and exams are doable |
| 2 | Is attendance mandatory for Andy Wang's COP4610?                   | No — multiple reviews list attendance as "Not Mandatory"           |
| 3 | Which FSU CS professors do students recommend most?                | Mills, Jayaraman, Sonia, and the Myers are mentioned positively in the Reddit thread |
| 4 | What are students' biggest complaints about the FSU CS department? | Not enough professors, limited/irrelevant electives, poor TAs, outdated coursework, underfunded |
| 5 | What do students say about Xin Yuan's course difficulty?           | Should be in your rmp_yuan_xin.txt — we'll verify this is answerable |

---

## Anticipated Challenges

<!-- What could go wrong? Name at least two specific risks with reasoning.
     Consider: noisy or inconsistent documents, missing source attribution, off-topic
     retrieval, chunks that split key information across boundaries. -->

1. **Review metadata bleeding into chunks** — RMP files mix ratings numbers, 
course codes, and tags (like "Helpful", "Caring") with actual review text. 
If chunks include that noise, retrieval may match on irrelevant metadata 
instead of meaningful content.

2. **Single-source dominance** — the Reddit thread on "State of CS at FSU" 
is long and opinionated. It may dominate retrieval results for department-level 
questions, drowning out RMP reviews that have different, equally valid 
perspectives.

---

## Architecture

<!-- Draw a diagram of your pipeline showing the five stages:
     Document Ingestion → Chunking → Embedding + Vector Store → Retrieval → Generation
     Label each stage with the tool or library you're using.
     You can use ASCII art, a Mermaid diagram, or embed a sketch as an image.
     You'll use this diagram as context when prompting AI tools to implement each stage. -->

┌─────────────────────────────────────────────────────────────────┐
│                        QUERY INTERFACE                          │
│                          (Gradio)                               │
└─────────────────────────────┬───────────────────────────────────┘
                              │ user query
                              ▼
┌──────────────┐    ┌──────────────────┐    ┌────────────────────┐
│   DOCUMENT   │    │    CHUNKING      │    │    EMBEDDING +     │
│  INGESTION   │───▶│  400 chars,      │───▶│   VECTOR STORE     │
│              │    │  50 char overlap │    │  all-MiniLM-L6-v2  │
│  .txt files  │    │  (LangChain or   │    │    + ChromaDB      │
│  (10 docs)   │    │   custom split)  │    │                    │
└──────────────┘    └──────────────────┘    └────────────┬───────┘
                                                         │
                                            semantic search (top-k=5)
                                                         │
                                                         ▼
┌─────────────────────────────────────────────────────────────────┐
│                         RETRIEVAL                               │
│              top 5 chunks + source metadata                     │
└─────────────────────────────┬───────────────────────────────────┘
                              │ retrieved chunks as context
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                        GENERATION                               │
│              Groq (llama-3.3-70b-versatile)                     │
│         grounded response + source attribution                  │
└─────────────────────────────────────────────────────────────────┘

---

## AI Tool Plan

<!-- For each part of the pipeline below, describe:
     - Which AI tool you plan to use (Claude, Copilot, ChatGPT, etc.)
     - What you'll give it as input (which sections of this planning.md, which requirements)
     - What you expect it to produce
     - How you'll verify the output matches your spec

     "I'll use AI to help me code" is not a plan.
     "I'll give Claude my Chunking Strategy section and ask it to implement chunk_text()
     with my specified chunk size and overlap" is a plan. -->

**Milestone 3 — Ingestion and chunking:**
I will give Claude my Documents section (file types, locations) and my Chunking 
Strategy section (400 char chunks, 50 char overlap, review-style text) and ask it 
to implement two functions: load_documents() that reads all .txt files from the 
documents/ folder and returns raw text with source filenames, and chunk_text() that 
splits each document into 400-character chunks with 50-character overlap. I will 
verify the output by printing 5 sample chunks and checking they are self-contained 
reviews without HTML artifacts or metadata noise.

**Milestone 4 — Embedding and retrieval:**
I will give Claude my Retrieval Approach section (all-MiniLM-L6-v2, top-k=5) and 
my pipeline diagram and ask it to implement embed_and_store() that embeds all chunks 
and loads them into ChromaDB with source metadata, and retrieve() that accepts a 
query string and returns the top 5 chunks with their source filenames. I will verify 
by running 3 of my evaluation questions and checking that returned chunks visibly 
relate to each question.

**Milestone 5 — Generation and interface:**
I will give Claude my grounding requirement (answers from retrieved context only, 
with source attribution) and the Gradio skeleton from the project instructions and 
ask it to implement generate_response() that passes retrieved chunks as context to 
Groq's llama-3.3-70b-versatile and returns a grounded answer with source citations, 
and a Gradio UI with a question input, answer output, and sources output. I will 
verify by asking a question my documents don't cover and confirming the system 
declines rather than hallucinating.
