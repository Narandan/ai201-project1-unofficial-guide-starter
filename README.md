# The Unofficial Guide — Project 1

> **How to use this template:**
> Complete each section *after* you've built and tested the corresponding part of your system.
> Do not write placeholder text — if a section isn't done yet, leave it blank and come back.
> Every section below is required for submission. One-liners will not receive full credit.

---

## Domain

     FSU Computer Science department — professor teaching styles, course difficulty, exam formats, and workload as reported by students. This knowledge is valuable because official sources (course catalogs, department websites) describe what courses cover but never tell you what it's actually like to take them. Students rely on word-of-mouth and scattered Reddit threads to make registration decisions, and this system makes that scattered knowledge searchable and answerable.
---

## Document Sources

<!-- List every source you collected documents from.
     Be specific: include URLs, subreddit names, forum thread titles, or file names.
     Aim for variety — sources that together cover different subtopics or perspectives. -->

| # | Source | Type | URL or file path |
|---|--------|------|-----------------|
| 1 | Rate My Professors | Professor reviews | documents/rmp_gaitros_david.txt |
| 2 | Rate My Professors | Professor reviews | documents/rmp_mills_christopher.txt |
| 3 | Rate My Professors | Professor reviews | documents/rmp_wang_andy.txt |
| 4 | Rate My Professors | Professor reviews | documents/rmp_yuan_xin.txt |
| 5 | Reddit r/FloridaStateUniversity | Forum thread | documents/reddit_if_your_a_professor_and_reading_this.txt |
| 6 | Reddit r/FloridaStateUniversity | Forum thread | documents/reddit_professor_positivity_thread.txt |
| 7 | Reddit r/FloridaStateUniversity | Forum thread | documents/reddit_the_state_of_computer_science_at_fsu.txt |
| 8 | FSU CS Website | Department overview | documents/fsu_edu_undergraduate_department_of_computer_science.txt |
| 9 | FSU CS Website | Degree program outcomes| documents/fsu_edu_bs_degree_program_mission_educational_objectives_student_outcomes.txt |
| 10 | FSU CS Website | Program guide | documents/fsu_edu_program_guide_computer_science_ba.txt |

---

## Chunking Strategy

<!-- Describe your chunking approach with enough specificity that someone else could reproduce it.
     Include:
     - Chunk size (characters or tokens) and why that size fits your documents
     - Overlap size and why (or why not) you used overlap
     - Any preprocessing you did before chunking (e.g., stripping HTML, removing headers)
     - What your final chunk count was across all documents -->

**Chunk size:** 400 characters

**Overlap:** 50 characters

**Why these choices fit your documents:** The documents are primarily review-style 
text where each unit of meaning is one student's opinion about one course or 
professor. A 400-character chunk captures a complete review with its metadata 
(course code, ratings) without merging two separate reviews together. Larger chunks 
(800+) would merge multiple reviews, diluting specific claims. Smaller chunks 
(100-200) would split a single review across two chunks, making neither retrievable 
on its own. A 50-character overlap was chosen because reviews are largely independent 
— just enough to catch a review clipped at a boundary without introducing unnecessary 
repetition. Before chunking, documents were cleaned to remove Reddit voting metadata 
(Upvote/Downvote/Reply/Award/Share), Reddit usernames, RMP tag labels (Helpful, 
Caring, etc.), and excessive blank lines.

**Final chunk count:** 888 chunks across 10 documents

---

## Embedding Model

<!-- Name the embedding model you used and explain your choice.
     Then answer: if you were deploying this system for real users and cost wasn't a constraint,
     what tradeoffs would you weigh in choosing a different model?
     Consider: context length limits, multilingual support, accuracy on domain-specific text,
     latency, and local vs. API-hosted. -->

**Model used:** all-MiniLM-L6-v2 via sentence-transformers (runs locally, no API 
key required, no rate limits)

**Production tradeoff reflection:** For a production deployment I would weigh several 
tradeoffs. OpenAI's text-embedding-3-large scores higher on benchmarks but costs 
money per query — for a high-traffic system that cost adds up quickly. Context length 
is not a concern here since reviews are short, but for longer documents like syllabi 
or handbooks a model with a larger context window would be necessary. Multilingual 
support is not needed for this corpus but would matter for a diverse campus 
population. Local models like all-MiniLM-L6-v2 have lower latency and no privacy 
concerns since data never leaves the machine, which would be valuable for a system 
handling student data.

---

## Grounded Generation

<!-- Explain how your system enforces grounding — how does it prevent the LLM from answering
     beyond the retrieved documents?
     Describe both your system prompt (what instruction you gave the model) and any structural
     choices (e.g., how you formatted the context, whether you filtered low-relevance chunks).
     Do not just say "I told it to use the documents" — show the actual instruction or explain
     the mechanism. -->

**System prompt grounding instruction:** The system prompt explicitly instructs the 
model to answer using ONLY the information provided in the retrieved documents and 
not to use any outside knowledge or make assumptions beyond what is in the documents. 
The exact instruction is: "Answer questions using ONLY the information provided in 
the documents below. Do not use any outside knowledge or make assumptions beyond 
what is in the documents. If the documents do not contain enough information to 
answer the question, say exactly: 'I don't have enough information in my sources 
to answer that question.'" This forces the model to refuse rather than hallucinate 
when the retrieved context is insufficient.

**How source attribution is surfaced in the response:** Source attribution is handled 
programmatically, not left to the LLM. After generation, any LLM-generated Sources 
section is stripped from the response and replaced with a clean list of source 
filenames drawn directly from the retrieved chunk metadata. This ensures attribution 
is always accurate and never fabricated. For out-of-scope questions the sources 
section reads "None — question is outside the scope of available documents."

---

## Evaluation Report

<!-- Run your 5 test questions from planning.md through your system and record the results.
     Be honest — a partially accurate or inaccurate result that you explain well is more
     valuable than a suspiciously perfect result. -->

| # | Question | Expected answer | System response (summarized) | Retrieval quality | Response accuracy |
|---|----------|-----------------|------------------------------|-------------------|-------------------|
| 1 | What do students say about David Gaitros's teaching style? | Lectures not always helpful, responsive to emails, YouTube videos, exams doable | Mixed opinions — condescending to some, humorous to others, classes easy to pass but not much learned | Relevant | Accurate |
| 2 | Is attendance mandatory for Andy Wang's COP4610? | No — multiple reviews list attendance as Not Mandatory | No, attendance is not mandatory | Relevant | Accurate |
| 3 | Which FSU CS professors do students recommend most? | Mills, Jayaraman, Sonia, and the Myers mentioned positively | Ruddell, Mills, Sharanya, and Bob mentioned — missed Jayaraman and the Myers | Partially relevant | Partially accurate |
| 4 | What are students' biggest complaints about the FSU CS department? | Not enough professors, limited electives, poor TAs, outdated coursework, underfunded | Lack of proper teaching, insufficient professors, inadequate funding, poor facilities | Relevant | Accurate |
| 5 | What do students say about Xin Yuan's course difficulty? | Courses rated 4-5 difficulty, very time-consuming, lots of homework, but rewarding | Said no information available despite rmp_yuan_xin.txt appearing in retrieved sources | Partially relevant | Inaccurate |

**Retrieval quality:** Relevant / Partially relevant / Off-target  
**Response accuracy:** Accurate / Partially accurate / Inaccurate

---

## Failure Case Analysis

<!-- Identify at least one question where retrieval or generation did not work as expected.
     Write a specific explanation of *why* it failed, tied to a part of the pipeline.

     "The answer was wrong" is not an explanation.

     "The relevant information was split across a chunk boundary, so retrieval returned
     only half the context — the model didn't have enough to answer correctly" is an explanation.

     "The embedding model treated the professor's nickname as out-of-vocabulary and returned
     results from an unrelated review" is an explanation. -->

**Question that failed:** What do students say about Xin Yuan's course difficulty?

**What the system returned:** "Unfortunately, there is no information in the provided 
documents about a person named Xin Yuan or their course difficulty." — despite 
rmp_yuan_xin.txt appearing in the retrieved sources list.

**Root cause (tied to a specific pipeline stage):** The failure occurred at two 
pipeline stages. First, at ingestion: rmp_yuan_xin.txt is the smallest document 
in the corpus at only 3,709 characters, producing very few chunks. Second, at 
chunking: the 400-character fixed-size split separated the professor's name from 
the actual difficulty ratings across chunk boundaries. When the retriever pulled 
the top-5 chunks, the chunks containing "Xin Yuan" by name were not paired with 
the chunks containing difficulty descriptions — so the LLM received fragments 
that mentioned ratings numbers but not the professor's name, and fragments that 
mentioned the name but not the ratings. With no chunk connecting name to difficulty, 
the model correctly reported it couldn't find the information, even though the 
information existed in the corpus.

**What you would change to fix it:** Two fixes would help. First, add professor 
name as metadata to every chunk from an RMP file at ingestion time, so retrieval 
can filter by professor name directly rather than relying on the name appearing 
in the chunk text. Second, reduce chunk size for small documents like rmp_yuan_xin.txt 
so fewer chunks are needed to cover the full document, reducing the chance of 
name and rating being split across boundaries.

---

## Spec Reflection

<!-- Reflect on how planning.md shaped your implementation.
     Answer both questions with at least 2–3 sentences each. -->

**One way the spec helped you during implementation:** Writing the chunking strategy 
in planning.md before touching any code forced a deliberate decision about chunk 
size based on the actual structure of the documents. After reading sample RMP reviews 
and seeing they were short, self-contained paragraphs, the spec locked in 400 
characters as the target — which meant when it came time to implement chunk_text(), 
there was no guessing. The spec also made it easy to direct Claude to generate code 
that matched the exact chunk size and overlap already decided on, rather than 
accepting whatever default the AI produced.

**One way your implementation diverged from the spec, and why:** The spec anticipated 
clean retrieval with distance scores below 0.5, but actual retrieval produced scores 
in the 0.68-1.0 range. This divergence happened because the RMP documents contain 
significant metadata mixed in with review text — course codes, quality ratings, 
date strings, and attendance fields — that dilutes the semantic signal of each chunk. 
The embedding model encodes all of that metadata alongside the actual opinion text, 
weakening similarity scores. The spec did not anticipate how much structured metadata 
would remain in the chunks after cleaning, and a more aggressive preprocessing step 
would have been warranted.

---

## AI Usage

**Instance 1**

- *What I gave the AI:* My Chunking Strategy section from planning.md (400 character 
chunks, 50 character overlap, review-style text) and my Documents section (10 .txt 
files in a documents/ folder). I asked Claude to implement two functions: 
load_documents() that reads all .txt files from the documents/ folder and returns 
raw text with source filenames, and chunk_text() that splits each document into 
400-character chunks with 50-character overlap.
- *What it produced:* A working ingest.py and chunker.py with the correct chunk 
size and overlap. The ingestion function loaded all 10 documents correctly and the 
chunker produced 888 chunks across the corpus.
- *What I changed or overrode:* The initial cleaning function only stripped excessive 
blank lines. After inspecting sample chunks and finding Reddit metadata noise 
(Upvote/Downvote/Reply/Award/Share) and RMP tag labels (Helpful, Caring, etc.), 
I directed Claude to add regex-based cleaning and eventually manually removed tag 
labels directly from the source documents for cleaner results.

**Instance 2**

- *What I gave the AI:* My Retrieval Approach section (all-MiniLM-L6-v2, top-k=5), 
my grounding requirement (answers from retrieved context only, with source 
attribution), and the Gradio skeleton from the project instructions. I asked Claude 
to implement embed_and_store(), retrieve(), generate_response(), and a Gradio UI 
with question input, answer output, and sources output.
- *What it produced:* Working embedder.py, retriever.py, generator.py, and app.py 
files that together formed a complete end-to-end RAG pipeline. The system correctly 
retrieved relevant chunks, generated grounded responses, and refused out-of-scope 
questions.
- *What I changed or overrode:* The initial generator allowed the LLM to write its 
own sources section, which produced fabricated or malformed source citations. I 
directed Claude to strip the LLM-generated sources and replace them programmatically 
with the actual source filenames from chunk metadata, ensuring attribution was always 
accurate. I also added special handling for out-of-scope responses to avoid showing 
misleading source lists.
