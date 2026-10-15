# The Agent Workflow Atlas

**14 concrete goals. Specialised agents. Visible handoffs. Human-owned decisions.**

A companion to the [Claude Code Agent Team Guide](../../README.md), grounded in every workflow listed on [VYR Agent OS](https://vyrwork.com/agent-os?utm_source=github&utm_medium=referral&utm_campaign=claude_agent_guide&utm_content=atlas). Detail pages checked **27 September 2026**; the overview's 14 cards and their status labels rechecked **15 October 2026**.

Start with the [AI Receptionist](ai-receptionist.md): a concierge coordinates knowledge, availability and booking agents, while unsupported requests go to staff with their context intact.

| VYR source status | Count | What it means here |
|---|---:|---|
| LIVE | 3 | The public site describes a production backend; important limits are retained below. |
| DEMO | 1 | Working voice software on sample data, without live booking integration. |
| BUILT FOR YOU | 10 | Specified designs to build and integrate; not deployed client results. |

The diagrams propose **how agents can cooperate**. They are educational designs, not audited maps of VYR's private infrastructure. Worked examples are fictional. Measures are evaluation suggestions, not achieved results. Model selection belongs to the [build playbook](BUILD_PLAYBOOK.md); no particular model is attributed to VYR's production systems.

## Explore the workflows

| # | Use case | Concrete goal | Source status |
|---|---|---|---|
| 01 | [AI Receptionist](ai-receptionist.md) | Turn an inbound call into a correct sample booking or a useful staff handoff. | DEMO |
| 02 | [Content Operations](content-operations.md) | Prepare a sourced article and release only the version an editor approves. | LIVE |
| 03 | [Lead Generation](lead-generation.md) | Deliver a sourced prospect list that a sales owner can review. | LIVE |
| 04 | [Social Command Center](social-command-center.md) | Turn approved content into a controlled release and observe its actual delivery. | LIVE |
| 05 | [Clinic Front Desk](clinics.md) | Resolve appointment administration while keeping clinical questions with clinic staff. | BUILT FOR YOU |
| 06 | [Invoice Processing](invoice-processing.md) | Convert an invoice into a reviewed accounting draft with explainable exceptions. | BUILT FOR YOU |
| 07 | [Customer Support](customer-support.md) | Get each enquiry to a supported answer or the right person with full context. | BUILT FOR YOU |
| 08 | [HR Operations](hr-operations.md) | Make a new starter's onboarding complete, attributable and reviewable. | BUILT FOR YOU |
| 09 | [Recruitment Screening](recruitment-screening.md) | Prepare a transparent application review and coordinate recruiter-approved interviews. | BUILT FOR YOU |
| 10 | [F&B Supplier Reorder](food-and-beverage.md) | Prepare the right stock replenishment for a manager's decision. | BUILT FOR YOU |
| 11 | [Tuition Trial Booking](tuition-centres.md) | Match a parent's enquiry to a genuinely available trial class. | BUILT FOR YOU |
| 12 | [Lead Nurture](lead-nurture.md) | Prepare a relevant next contact for the deal owner's approval. | BUILT FOR YOU |
| 13 | [Compliance Evidence](compliance-evidence.md) | Give a reviewer a traceable evidence pack and an honest gap register. | BUILT FOR YOU |
| 14 | [Beauty & Wellness](beauty-and-wellness.md) | Coordinate service, therapist, room and package information into a valid booking. | BUILT FOR YOU |

## Read the live boundaries first

- **Content Operations:** a live eleven-agent pipeline, grouped here into five educational roles; the main page says new generation is paused behind its approval backlog. Publication requires a human decision.
- **Lead Generation:** source, enrich, deduplicate and check prospect records; the workflow ends at a reviewed CSV and never sends outreach.
- **Social Command Center:** its live FeedHive console is read-only. A separate publisher checks approval against exact copy, image, accounts, labels and schedule before any new write.
- **Voice Receptionist:** uses sample business facts and calendars. A sample booking is not an actual appointment.

VYR's proposed cross-workflow shared-memory layer is **build-to-order and not wired into the three live pipelines**. Run-specific handoff packets in these diagrams do not imply deployed shared memory. [Current source overview](https://vyrwork.com/agent-os)

## Using the atlas

Each case includes a goal, trigger, collaboration diagram, input/output contracts, human decision, completion condition, fictional worked example and evaluation ideas. Read the [build playbook](BUILD_PLAYBOOK.md) to translate a case into an implementation brief. See the [source register](SOURCES.md) for all 14 original workflow pages.
