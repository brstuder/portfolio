# Arine

**Technical Writer, *April 2025 - Mar 2026***

| Criteria | Description |
|---|---|
| Documentation | Document360, Confluence, SnagIt, Claude, Gemini |
| Subject matter/industry | SaaS, healthcare, product UI |
| Points of contact | Knowledge Base (KB) team, product managers, technical product managers |
| Target audience | Clinicians, pharmacists, and other healthcare professionals |

Most recently I served as the solo technical writer at Arine (uh-*REEN*), a healthcare optimization platform for pharmacists, clinicians, and other medical professionals. Our documentation is considered proprietary, so I'm unable to share any direct writing samples here. However, I can still freely discuss my professional work more broadly.

## Key Projects and Responsibilities

### Migration to Document360

Moving Arine's documentation out of static PDFs into a living knowledge base was not an easy accomplishment. The KB team eventually selected Document360 as a content management system to handle the total turnaround for product docs. Our documentation is closed-source, which means coordination with our full-stack engineering team was necessary to build out the proper user authentication.

After higher-level logistics had been determined, the sheer bulk of the work required removal of any unique or advanced style elements, then converting the content into a basic, readable format. CSS was finally applied across the entire knowledge base, reducing the manual work that had been going into formatting PDFs. Overall, the project accomplished a number of feats the KB team had hoped for:

* The KB team could now own the publishing process itself (previously a full stack responsibility), allowing documentation to be drafted and published in a CI/CD pipeline instead of only during major software releases.
* Total turnaround time (time from drafting content, SME review, and publishing) was reduced by over half as a result of the manual/tedious processes removed completely.
* Greater insight into user activity was now available, as this was previously a black hole due to our PDFs not tracking these metrics.

### Writing and Editing AI Agent

AI adoption is a skill quickly becoming in-demand. I took initiative within my team to identify use cases where an AI writing agent could provide and additional layer of coherence across our content. Setting up a basic Claude Code environment to work, I provided the following materials as my base context:

* A `claude.md` file providing both an identity and workflow approach as the basis for all writing functions.
* All of our user-facing documentation, converted into Markdown (using Pandoc) for easy ingestion
* Our company style guide that emphasizes key vocabulary, formatting, and other language guidelines.

With this, Claude was able to read through our existing documentation, and perform the following tasks:

* Find existing content that did not conform to our style guide
* Determine areas of content which would need rewrites based on proposed new feature functionality (read from Jira tickets)
* Identify excessively wordy or misformatted content, indicating where content could be reformatted for readability