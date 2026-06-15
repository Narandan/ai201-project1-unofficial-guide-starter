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

**Chunk size:** 400 characters

**Overlap:** 50 characters

**Why these choices fit your documents:** The documents are primarily review-style text where each unit of meaning is one student's opinion about one course or professor. A 400-character chunk captures a complete review with its metadata (course code, ratings) without merging two separate reviews together. Larger chunks (800+) would merge multiple reviews, diluting specific claims. Smaller chunks (100-200) would split a single review across two chunks, making neither retrievable on its own. A 50-character overlap was chosen because reviews are largely independent — just enough to catch a review clipped at a boundary without introducing unnecessary repetition. Before chunking, documents were cleaned to remove Reddit voting metadata (Upvote/Downvote/Reply/Award/Share), Reddit usernames, RMP tag labels (Helpful, Caring, etc.), and excessive blank lines.

**Final chunk count:** 888 chunks across 10 documents

---

## Embedding Model

**Model used:** all-MiniLM-L6-v2 via sentence-transformers (runs locally, no API 
key required, no rate limits)

**Production tradeoff reflection:** For a production deployment I would weigh several tradeoffs. OpenAI's text-embedding-3-large scores higher on benchmarks but costs money per query — for a high-traffic system that cost adds up quickly. Context length is not a concern here since reviews are short, but for longer documents like syllabi or handbooks a model with a larger context window would be necessary. Multilingual support is not needed for this corpus but would matter for a diverse campus population. Local models like all-MiniLM-L6-v2 have lower latency and no privacy concerns since data never leaves the machine, which would be valuable for a system handling student data.

---

## Grounded Generation

**System prompt grounding instruction:** The system prompt explicitly instructs the model to answer using ONLY the information provided in the retrieved documents and not to use any outside knowledge or make assumptions beyond what is in the documents. The exact instruction is: "Answer questions using ONLY the information provided in the documents below. Do not use any outside knowledge or make assumptions beyond what is in the documents. If the documents do not contain enough information to answer the question, say exactly: 'I don't have enough information in my sources to answer that question.'" This forces the model to refuse rather than hallucinate when the retrieved context is insufficient.

**How source attribution is surfaced in the response:** Source attribution is handled programmatically, not left to the LLM. After generation, any LLM-generated Sources section is stripped from the response and replaced with a clean list of source filenames drawn directly from the retrieved chunk metadata. This ensures attribution is always accurate and never fabricated. For out-of-scope questions the sources section reads "None — question is outside the scope of available documents."

---

## Sample Chunks

The following chunks were produced by the ingestion and chunking pipeline (400-character chunks, 50-character overlap). Each is labeled with its source document.

**Chunk 1 — Source: `reddit_the_state_of_computer_science_at_fsu.txt`**
> "Go to fsu / r/fsu / 2y ago / DevelopmentExact554 / The state of Computer Science at FSU / Hey everyone I'm making this post to sound the alarm bell for those looking to get into CS at FSU. Don't. For those who don't know what's going on, the CS department since the pandemic has been on life support, not enough professors, not enough funding, and not good enough."

**Chunk 2 — Source: `reddit_the_state_of_computer_science_at_fsu.txt`**
> "enough. This is in stark contrast to the college of engineering which I've only heard high praise from, so if you want to be an engineer at FSU you have nothing to worry about, the same can't be said for CS. Why CS at FSU sucks. FSU itself doesn't even seem to really care about us, a prime example is the old sputnik building that we're housed in, that finally got funding to remove black mold fro"

**Chunk 3 — Source: `reddit_the_state_of_computer_science_at_fsu.txt`**
> "The professors, and Jesus are they awful. Most of them are ancient and are stuck in the past still teaching irrelevant coursework and acting like they're amazing. They can't fathom how a 19 year old can't understand a 'simple' topic that was taught 3 weeks ago in a single slide. 'We talked about this a month ago, you should know this, how do you not, it's so easy don't be lazy.'"

**Chunk 4 — Source: `reddit_the_state_of_computer_science_at_fsu.txt`**
> "The teaching faculty here are actually good. Mills, Jayaraman, Sonia, and the Myers are professors you actually learn from, Bob and Sharanya are controversial but at least you get something from the class. Too bad the department chair thinks they're '...a waste of resources.' and the hiring committee for the new teaching faculty won't hire anyone who doesn't have a PhD."

**Chunk 5 — Source: `rmp_gaitros_david.txt`**
> "Professor Gaitros' class is an easy to pass class but you probably won't learn very much while you're there. He's funny and he seems to know what he's talking about. Would Take Again: Yes / Grade: A / Textbook: No"

**Chunk 6 — Source: `rmp_wang_andy.txt`**
> "COP4610 / Jan 2nd, 2026 / For Credit: Yes / Attendance: Not Mandatory / Would Take Again: Yes / Grade: A / Textbook: N/A / Dr. Andy Wang is a great professor who genuinely cares about your performance in the class."

**Chunk 7 — Source: `rmp_mills_christopher.txt`**
> "Attendance: Mandatory / Would Take Again: Yes / Grade: A / Textbook: N/A / I took this class last summer and it was great. I took Java with Bob this semester and it's been so awful, I daydream about this class."

---

## Retrieval Test Results

### Query 1: "What do students say about David Gaitros teaching style?"

| Rank | Source | Text (excerpt) |
|------|--------|----------------|
| 1 | `rmp_gaitros_david.txt` | "...the kind of guy that has already made it himself, and wants to give back to the Comp Sci world by preparing his students for their road ahead. Quality: 2.0, Difficulty: 4.0" |
| 2 | `rmp_gaitros_david.txt` | "He makes class more entertaining by his jokes and can make certain things easier to learn by his comparison. Overall good guy and would recommend anyone to take him." |
| 3 | `rmp_gaitros_david.txt` | "Makes us learn information that students taking programming 2 haven't learned. Awful guy as well, real headcase. Stay away from this guy. Quality: 3.0, Difficulty: 3.0" |
| 4 | `reddit_professor_positivity_thread.txt` | "...when he's speaking and how genuinely interested he is in it all. I just wish I could have taken his class in person." |
| 5 | `rmp_gaitros_david.txt` | "Professor Gaitros' class is an easy to pass class but you probably won't learn very much while you're there. He's funny and he seems to know what he's talking about." |

**Why these chunks are relevant:** Four of the five results come directly from `rmp_gaitros_david.txt`, the dedicated RMP file for this professor. Each chunk contains a distinct student opinion about his teaching — ranging from praise for his humor to criticism of his ineffectiveness — which is exactly what the query asks for. The retriever correctly identified professor-specific review text as the most semantically similar content to a question about teaching style.

---

### Query 2: "Is attendance mandatory for Andy Wang COP4610?"

| Rank | Source | Text (excerpt) |
|------|--------|----------------|
| 1 | `rmp_wang_andy.txt` | "COP4610 / Jan 2nd, 2026 / Attendance: Not Mandatory / Would Take Again: Yes / Grade: A / Dr. Andy Wang is a great professor who genuinely cares about your performance in the class." |
| 2 | `rmp_mills_christopher.txt` | "Attendance: Mandatory / Would Take Again: Yes / Grade: A / Textbook: N/A / I took this class last summer and it was great." |
| 3 | `rmp_wang_andy.txt` | "Attendance: Not Mandatory / Would Take Again: Yes / Grade: B+ / Textbook: No / Online Class: Yes / Professor Wang made lectures very engaging." |
| 4 | `rmp_wang_andy.txt` | "COP4610 / Feb 24th, 2023 / Attendance: Not Mandatory / Would Take Again: Yes / Grade: A-" |
| 5 | `rmp_wang_andy.txt` | "...insightful in his very humorous lectures and encourages participation. Quality: 5.0, Difficulty: 4.0, COP4610" |

**Why these chunks are relevant:** The query contains both the professor name and course number, giving the embedder a strong signal. Three of the top five results are COP4610-specific Wang reviews that explicitly list "Attendance: Not Mandatory," directly answering the question. Result 2 from `rmp_mills_christopher.txt` is a minor retrieval noise — it matched on the word "Attendance" — but it did not affect the final answer since the Wang chunks dominated.

---

### Query 3: "What are students' biggest complaints about the FSU CS department?"

| Rank | Source | Text (excerpt) |
|------|--------|----------------|
| 1 | `reddit_if_your_a_professor_and_reading_this.txt` | "FSU students are shitty at doing this. It's a party school after all. This pandemic is actually exposing a big problem that our student body doesn't have proper expectations for college..." |
| 2 | `reddit_the_state_of_computer_science_at_fsu.txt` | "...in stark contrast to the college of engineering which I've only heard high praise from, so if you want to be an engineer at FSU you have nothing to worry about, the same can't be said for CS." |
| 3 | `reddit_the_state_of_computer_science_at_fsu.txt` | "...based on anecdotal evidence may not reflect well on our faculty/staff/students who work very hard to serve our duties and grow our careers..." |
| 4 | `reddit_if_your_a_professor_and_reading_this.txt` | "They are struggling to teach classes online, do research, take care of their families, and make sure their young children go to their online classes." |
| 5 | `reddit_the_state_of_computer_science_at_fsu.txt` | "Hey everyone I'm making this post to sound the alarm bell for those looking to get into CS at FSU. Don't. The CS department since the pandemic has been on life support, not enough professors, not enough funding..." |

---

## Example Responses

### Response 1 — Query: "What do students say about David Gaitros teaching style?"

> Students have mixed opinions about Dr. Gaitros' teaching style. Some students find him to be condescending and arrogant, while others appreciate his sense of humor and ability to make complex concepts easier to learn through comparisons. However, many students agree that he does not convey information well and does not engage students effectively. Some students also feel that his classes are easy to pass but do not provide much opportunity for learning. One student noted that he often begins classes with stories from his "glory days," which may come across as arrogant. Another student appreciated his passion for the subject when speaking, but wished they could have taken his class in person.
>
> Sources:
> • reddit_professor_positivity_thread.txt
> • rmp_gaitros_david.txt

---

### Response 2 — Query: "Is attendance mandatory for Andy Wang COP4610?"

> According to the documents, attendance is not mandatory for Dr. Andy Wang's COP4610 class.
>
> Sources:
> • rmp_mills_christopher.txt
> • rmp_wang_andy.txt

---

### Out-of-Scope Response — Query: "What is the best pizza place near FSU?"

> I don't have enough information in my sources to answer that question.
>
> Sources: None — question is outside the scope of available documents.

---

## Query Interface

**Interface type:** Gradio web UI, launched via `python app.py` and accessible at `http://localhost:7860`.

**Input fields:**

- **Your question** — a free-text box where the user types a plain-language question about FSU CS professors, courses, or department experiences.

**Output fields:**

- **Answer** — the grounded response generated from retrieved document chunks. If no relevant information exists, the system returns a standard refusal message.
- **Retrieved from** — a list of source document filenames the answer was drawn from, appended programmatically from chunk metadata (not generated by the LLM).

**Sample interaction transcript:**

User: Is attendance mandatory for Andy Wang COP4610?

Answer:
According to the documents, attendance is not mandatory for Dr. Andy Wang's
COP4610 class.

Retrieved from:
• rmp_mills_christopher.txt
• rmp_wang_andy.txt

## Evaluation Report

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

**Question that failed:** What do students say about Xin Yuan's course difficulty?

**What the system returned:** "Unfortunately, there is no information in the provided 
documents about a person named Xin Yuan or their course difficulty." — despite 
rmp_yuan_xin.txt appearing in the retrieved sources list.

**Root cause (tied to a specific pipeline stage):** The failure occurred at two pipeline stages. First, at ingestion: rmp_yuan_xin.txt is the smallest document in the corpus at only 3,709 characters, producing very few chunks. Second, at chunking: the 400-character fixed-size split separated the professor's name from the actual difficulty ratings across chunk boundaries. When the retriever pulled the top-5 chunks, the chunks containing "Xin Yuan" by name were not paired with the chunks containing difficulty descriptions — so the LLM received fragments that mentioned ratings numbers but not the professor's name, and fragments that mentioned the name but not the ratings. With no chunk connecting name to difficulty, the model correctly reported it couldn't find the information, even though the information existed in the corpus.

**What you would change to fix it:** Two fixes would help. First, add professor name as metadata to every chunk from an RMP file at ingestion time, so retrieval can filter by professor name directly rather than relying on the name appearing in the chunk text. Second, reduce chunk size for small documents like rmp_yuan_xin.txt so fewer chunks are needed to cover the full document, reducing the chance of name and rating being split across boundaries.

---

## Spec Reflection

**One way the spec helped you during implementation:** Writing the chunking strategy in planning.md before touching any code forced a deliberate decision about chunk size based on the actual structure of the documents. After reading sample RMP reviews and seeing they were short, self-contained paragraphs, the spec locked in 400 characters as the target — which meant when it came time to implement chunk_text(), there was no guessing. The spec also made it easy to direct Claude to generate code that matched the exact chunk size and overlap already decided on, rather than accepting whatever default the AI produced.

**One way your implementation diverged from the spec, and why:** The spec anticipated clean retrieval with distance scores below 0.5, but actual retrieval produced scores in the 0.68-1.0 range. This divergence happened because the RMP documents contain significant metadata mixed in with review text — course codes, quality ratings, date strings, and attendance fields — that dilutes the semantic signal of each chunk. The embedding model encodes all of that metadata alongside the actual opinion text, weakening similarity scores. The spec did not anticipate how much structured metadata would remain in the chunks after cleaning, and a more aggressive preprocessing step would have been warranted.

---

## AI Usage

**Instance 1** 
*What I gave the AI:* My Chunking Strategy section from planning.md (400 character chunks, 50 character overlap, review-style text) and my Documents section (10 .txt files in a documents/ folder). I asked Claude to implement two functions: load_documents() that reads all .txt files from the documents/ folder and returns raw text with source filenames, and chunk_text() that splits each document into 400-character chunks with 50-character overlap.
*What it produced:* A working ingest.py and chunker.py with the correct chunk size and overlap. The ingestion function loaded all 10 documents correctly and the chunker produced 888 chunks across the corpus.
*What I changed or overrode:* The initial cleaning function only stripped excessive blank lines. After inspecting sample chunks and finding Reddit metadata noise (Upvote/Downvote/Reply/Award/Share) and RMP tag labels (Helpful, Caring, etc.), I directed Claude to add regex-based cleaning and eventually manually removed tag labels directly from the source documents for cleaner results.

**Instance 2**
*What I gave the AI:* My Retrieval Approach section (all-MiniLM-L6-v2, top-k=5), my grounding requirement (answers from retrieved context only, with source attribution), and the Gradio skeleton from the project instructions. I asked Claude to implement embed_and_store(), retrieve(), generate_response(), and a Gradio UI with question input, answer output, and sources output.
*What it produced:* Working embedder.py, retriever.py, generator.py, and app.py files that together formed a complete end-to-end RAG pipeline. The system correctly retrieved relevant chunks, generated grounded responses, and refused out-of-scope questions.
*What I changed or overrode:* The initial generator allowed the LLM to write its own sources section, which produced fabricated or malformed source citations. I directed Claude to strip the LLM-generated sources andreplace them programmatically with the actual source filenames from chunk metadata, ensuring attribution was always accurate. I also added special handling for out-of-scope responses to avoid showing misleading source lists.
