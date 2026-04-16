from __future__ import annotations

from copy import deepcopy

BRAND = "Gradient Signal"
POSITIONING = "What changed in AI, and what it changes for builders."
TAGLINE = "A signal-first AI engineering brief for teams who care about deployment reality."

AUDIENCE = [
    "AI engineers shipping agent, retrieval, and copilots into production",
    "Applied researchers translating model updates into product decisions",
    "ML platform teams responsible for cost, reliability, security, and governance",
    "Technical founders deciding which model and infrastructure bets actually matter",
]

EDITORIAL_RULES = [
    "Only cover changes that materially affect capability, cost, latency, reliability, evals, security, licensing, access, or deployment/compliance.",
    "Lead with primary sources whenever they exist, then summarize the builder impact in plain language.",
    "Treat new launches as hypotheses until we can explain the operational consequences and tradeoffs.",
    "Prefer concrete deltas over posture, personality, or prediction markets.",
]

WHAT_WE_IGNORE = [
    "Viral demos that do not show repeatable deployment paths, controls, or pricing.",
    "Leaderboard wins without methods, eval details, or a clear production implication.",
    "Roadmap theater, teaser posts, and vague AGI narratives that do not change what builders can ship.",
    "Model personality discourse, social chatter, and speculative hot takes dressed up as strategy.",
    "Feature launches that look flashy but do not alter cost, quality, safety, or integration constraints.",
]

METHODOLOGY_SECTIONS = [
    {
        "title": "Materiality before novelty",
        "body": (
            "A story belongs in Gradient Signal only if it changes a real engineering decision: "
            "what to build on, what to avoid, what it costs, how it is governed, or how it behaves in production."
        ),
    },
    {
        "title": "Primary-source-first reporting",
        "body": (
            "We anchor each brief in release notes, product docs, changelogs, or vendor statements before "
            "using secondary coverage. That keeps the brief close to the actual contract builders inherit."
        ),
    },
    {
        "title": "Operational framing",
        "body": (
            "Each item answers the same question: what changed for teams shipping AI systems this week, and "
            "what tradeoff does that introduce?"
        ),
    },
    {
        "title": "Skeptical by default",
        "body": (
            "We do not confuse launch volume with leverage. If a claim cannot survive contact with deployment, "
            "compliance, or cost constraints, it does not make the cut."
        ),
    },
]

LATEST_BRIEF = {
    "slug": "2026-04-16-launch-brief",
    "title": "Latest Brief: Six changes that matter more than the chatter",
    "published_on": "2026-04-16",
    "summary": (
        "This launch issue tracks six recent vendor moves that actually change the build surface for AI teams: "
        "agent runtime primitives, hosted orchestration, high-cyber-capability access controls, regulated "
        "deployment options, inference routing, and a stronger permissive open-model option."
    ),
    "editor_note": (
        "The bar for inclusion is simple: if a story does not change a builder decision next quarter, it does not belong here."
    ),
    "items": [
        {
            "slug": "openai-agents-sdk-sandbox",
            "headline": "OpenAI adds native sandbox execution to the Agents SDK",
            "announced_on": "2026-04-15",
            "category": "agents-runtime",
            "summary": (
                "OpenAI added first-party sandbox execution to the Agents SDK, bundling code execution with workspace isolation "
                "instead of pushing teams toward custom container glue."
            ),
            "why_it_matters": (
                "This lowers the setup cost for agent workflows that need controlled tool execution, while making isolation and "
                "runtime policy part of the platform conversation rather than an afterthought."
            ),
            "sources": [
                {
                    "label": "OpenAI",
                    "url": "https://openai.com/index/the-next-evolution-of-the-agents-sdk/",
                }
            ],
        },
        {
            "slug": "anthropic-managed-agents-advisor",
            "headline": "Anthropic launches Managed Agents beta and the Advisor tool",
            "announced_on": "2026-04-09",
            "category": "agents-platform",
            "summary": (
                "Anthropic expanded its platform across April 8 and 9 with Managed Agents beta and the Advisor tool, positioning more of the long-horizon "
                "agent runtime and review loop as a hosted service."
            ),
            "why_it_matters": (
                "Builders get a more opinionated path for orchestration and a clearer quality-versus-cost lever for complex tasks, "
                "which is useful if they want less infrastructure ownership and can accept tighter platform coupling."
            ),
            "sources": [
                {
                    "label": "Anthropic API release notes",
                    "url": "https://docs.anthropic.com/en/release-notes/api",
                },
                {
                    "label": "Anthropic Advisor tool",
                    "url": "https://docs.anthropic.com/en/agents-and-tools/tool-use/advisor-tool",
                },
            ],
        },
        {
            "slug": "claude-mythos-preview-gated",
            "headline": "Anthropic and AWS keep Claude Mythos Preview gated after a sharp cyber-capability jump",
            "announced_on": "2026-04-07",
            "category": "security-safety",
            "summary": (
                "Anthropic and AWS left Claude Mythos Preview behind stronger access controls after internal evaluation showed a "
                "meaningful jump in cyber capability."
            ),
            "why_it_matters": (
                "This is a concrete signal that access policy and verification expectations will keep tightening for high-capability models, "
                "especially where offensive security risk rises faster than ordinary enterprise controls."
            ),
            "sources": [
                {
                    "label": "Anthropic",
                    "url": "https://red.anthropic.com/2026/mythos-preview/",
                },
                {
                    "label": "AWS",
                    "url": "https://aws.amazon.com/about-aws/whats-new/2026/04/amazon-bedrock-claude-mythos/",
                },
            ],
        },
        {
            "slug": "copilot-data-residency-fedramp",
            "headline": "GitHub Copilot gets US/EU data residency and FedRAMP-compliant inference",
            "announced_on": "2026-04-13",
            "category": "compliance",
            "summary": (
                "GitHub added US and EU data residency plus FedRAMP-compliant inference options for Copilot, moving the product further "
                "into regulated deployment territory."
            ),
            "why_it_matters": (
                "For enterprise and public-sector teams, this reduces one of the biggest blockers to assisted coding adoption: whether "
                "the deployment model can satisfy residency and compliance constraints without custom carve-outs."
            ),
            "sources": [
                {
                    "label": "GitHub changelog",
                    "url": "https://github.blog/changelog/2026-04-13-copilot-data-residency-in-us-eu-and-fedramp-compliance-now-available/",
                }
            ],
        },
        {
            "slug": "gemini-flex-priority-tiers",
            "headline": "Google adds Flex and Priority inference tiers to the Gemini API",
            "announced_on": "2026-04-02",
            "category": "cost-reliability",
            "summary": (
                "Google introduced Flex and Priority inference tiers for Gemini API traffic, making the cost-versus-reliability choice more explicit."
            ),
            "why_it_matters": (
                "Teams now have a clearer routing primitive for splitting workloads by urgency and service expectations, which matters when "
                "serving both background jobs and user-facing requests from the same model estate."
            ),
            "sources": [
                {
                    "label": "Google",
                    "url": "https://blog.google/innovation-and-ai/technology/developers-tools/introducing-flex-and-priority-inference",
                }
            ],
        },
        {
            "slug": "gemma-4-apache2",
            "headline": "Google releases Gemma 4 under Apache 2.0",
            "announced_on": "2026-04-02",
            "category": "open-models",
            "summary": (
                "Google released Gemma 4 under Apache 2.0, strengthening the set of permissively licensed options available for controlled deployments."
            ),
            "why_it_matters": (
                "Apache 2.0 licensing matters when teams need private, on-prem, or edge-friendly deployments without negotiating around restrictive use terms."
            ),
            "sources": [
                {
                    "label": "Google announcement",
                    "url": "https://blog.google/innovation-and-ai/technology/developers-tools/gemma-4/",
                },
                {
                    "label": "Google Developers Blog",
                    "url": "https://developers.googleblog.com/bring-state-of-the-art-agentic-skills-to-the-edge-with-gemma-4/",
                },
            ],
        },
    ],
    "what_we_ignore": WHAT_WE_IGNORE,
    "cta": {
        "title": "Get the next brief",
        "body": (
            "For launch, the reliable signup path is direct email. Send a short note with your role and what you're tracking if you want the next brief."
        ),
        "launch_note": "Live deployments default to direct email so the public CTA does not depend on ephemeral file storage.",
        "demo_note": "Local demo environments can optionally show a disposable waitlist form, but public launches use direct email.",
        "button_label": "Email the team",
    },
}


def get_latest_brief() -> dict:
    """Return a copy of the latest brief for templates and JSON endpoints."""
    return deepcopy(LATEST_BRIEF)


def get_site_context() -> dict:
    """Return shared site copy for templates and llms.txt."""
    return {
        "brand": BRAND,
        "positioning": POSITIONING,
        "tagline": TAGLINE,
        "audience": list(AUDIENCE),
        "editorial_rules": list(EDITORIAL_RULES),
        "what_we_ignore": list(WHAT_WE_IGNORE),
        "methodology_sections": deepcopy(METHODOLOGY_SECTIONS),
    }

