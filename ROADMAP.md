# AdLoop — Product Roadmap

The vision: build a **suite of MCP servers** that together form the ultimate toolkit for media buyers — managing ads, analytics, creative generation, competitor research, CRM, and cross-platform optimization across every major platform.

## Why Multiple Servers?

Instead of one monolithic MCP server, AdLoop is split into **independent, focused servers** that can be deployed, scaled, and updated independently.

| Benefit | Details |
|---|---|
| **Isolation** | A Meta SDK update can't break Google Ads tools |
| **Independent scaling** | Creative gen needs more resources than campaign management |
| **Smaller attack surface** | Each server only holds credentials for its platforms |
| **Faster deploys** | Change one server without redeploying everything |
| **Mix infrastructure** | Creative gen on GPU server, everything else on standard VMs |
| **Pick and choose** | Agencies can deploy only the servers they need |

Claude Code connects to all servers simultaneously — just `claude mcp add` each one.

---

## The Servers

```
┌─────────────────────────────────────────────────────────┐
│                   Claude Code / Cursor                   │
│                    (AI Assistant)                         │
└──────┬──────┬──────┬──────┬──────┬──────┬───────────────┘
       │      │      │      │      │      │
       ▼      ▼      ▼      ▼      ▼      ▼
   ┌──────┐┌──────┐┌──────┐┌──────┐┌──────┐┌──────┐
   │ ads  ││analytics││intel ││creative││ crm  ││report│
   │server││ server ││server││ server ││server││server│
   └──┬───┘└──┬───┘└──┬───┘└──┬───┘└──┬───┘└──┬───┘
      │       │       │       │       │       │
      ▼       ▼       ▼       ▼       ▼       ▼
   Google   GA4     Meta Ad  Flux    GHL    Sheets
   Meta     Search  Library  Runway         PDF
   TikTok   Console TikTok   GPT-4o
   Bing             Creative Creatomate
   LinkedIn         Center   Stability
```

---

## Server 1: adloop-ads (Campaign Management)

**What it does:** Manage ad campaigns across all major platforms through a unified interface with draft-then-confirm safety.

**Status:** Google Ads is live. Meta Ads is next priority.

### Google Ads (Live)
- Campaign, ad, keyword, search term performance reporting
- Campaign/ad/keyword creation with draft-then-confirm
- Negative keyword management
- Budget forecasting via Keyword Planner
- GAQL for advanced queries
- Account allowlist for access control

### Meta (Facebook/Instagram) Ads — Priority: P1
Official Python SDK (`facebook-business`). OAuth 2.0 with system user tokens.

**Read:**
- `meta_get_campaign_performance` — Metrics with breakdowns by age, gender, placement, device
- `meta_get_adset_performance` — Ad set level including targeting and budget
- `meta_get_ad_performance` — Ad-level metrics with creative details
- `meta_list_audiences` — Custom and lookalike audiences with sizes
- `meta_get_reach_estimate` — Estimate audience size for a targeting spec
- `meta_get_delivery_estimate` — Forecast reach/impressions for a budget

**Write (draft-then-confirm):**
- `meta_draft_campaign` — Campaigns with objectives (awareness, traffic, conversions, leads, sales)
- `meta_draft_adset` — Ad sets with targeting, budget, placements, optimization goal
- `meta_draft_ad` — Ads linking creative to ad set
- `meta_create_lookalike_audience` — Build lookalike from existing audience (1-10%)
- `meta_pause_entity` / `meta_enable_entity`
- `meta_confirm_and_apply`

**Meta-unique:** Lookalike audiences, placement optimization across FB/IG/Messenger/Audience Network, breakdown reporting by age/gender/platform, Lead Ads, dynamic catalog ads.

**Safety:** Budget in cents (not micros), spend cap guards, Special Ad Category enforcement, audience size minimums.

### TikTok Ads — Priority: P2
Official Python SDK (`tiktok-business-api-sdk`). OAuth 2.0.
- Campaign/ad group/ad CRUD with draft-then-confirm
- Performance reporting with breakdowns
- Custom and lookalike audience management
- Spark Ads (boost organic TikTok posts)

### Microsoft/Bing Ads — Priority: P2
Official Python SDK (`bingads`). OAuth 2.0 via Azure AD.
- Campaign management (nearly identical to Google Ads entity model)
- `import_from_google_ads` — API to directly import Google campaigns
- LinkedIn-data-based B2B targeting (unique to Microsoft)

### LinkedIn Ads — Priority: P3
No official Python SDK (REST client). OAuth 2.0.
- Campaign management for Sponsored Content, Messaging, Text Ads
- B2B targeting — job title, company, industry, seniority, skills
- Lead Gen Forms — pull submitted leads
- Matched Audiences — company/contact list targeting

### Dependencies
```
google-ads, google-analytics-data, google-analytics-admin, google-auth-oauthlib
facebook-business
tiktok-business-api-sdk
bingads
fastmcp, pyyaml
```

---

## Server 2: adloop-analytics (Analytics & Optimization)

**What it does:** Cross-platform analytics, attribution, budget optimization, and SEO intelligence.

### GA4 Analytics (Live)
- Custom reports, realtime reports, event tracking
- Cross-channel campaign-to-conversion mapping
- Landing page analysis
- Attribution checks (Ads vs GA4 discrepancies)

### Google Search Console — Priority: P1
Same Google OAuth. Very low effort, high value.
- `get_organic_search_performance` — Queries, impressions, clicks, CTR, position
- `find_paid_organic_overlap` — Keywords where you're paying for traffic you'd get organically
- `identify_seo_opportunities` — High-impression/low-CTR organic queries to target with paid

### Server-Side Tracking — Priority: P1
- `meta_send_conversion_event` — Meta CAPI for server-side event tracking
- `upload_enhanced_conversions` — Google Enhanced Conversions via `ConversionUploadService`
- `tiktok_send_event` — TikTok Events API

### Cross-Platform Budget Optimizer — Priority: P2
Internal algorithm using `scipy.optimize`. **Key differentiator — no existing tool does this well.**
- `analyze_cross_platform_efficiency` — Compare CPA/ROAS across Google, Meta, TikTok, Bing
- `suggest_budget_reallocation` — Recommend shifts based on marginal returns curves
- `simulate_budget_scenario` — Forecast results of a proposed allocation

### UTM Manager — Priority: P3
- `generate_utm` — Create consistent UTMs across all platforms
- `audit_utm_consistency` — Check for inconsistencies across active campaigns

### Dependencies
```
google-ads, google-analytics-data, google-analytics-admin, google-auth-oauthlib
facebook-business          # For CAPI
tiktok-business-api-sdk    # For Events API
scipy                      # Budget optimization
fastmcp, pyyaml
```

---

## Server 3: adloop-intel (Competitor Research & Ad Intelligence)

**What it does:** Research competitor ads, identify winners, build swipe files, analyze creative patterns.

### Meta Ad Library API — Priority: P1
Official REST API (`GET /ads_archive`). Identity-verified access token with `ads_read`. 200 calls/hour.

**Tools:**
- `search_competitor_ads` — Search by keyword, advertiser page ID, country, platform, media type
- `find_winner_ads` — Score ads by longevity, spend bucket, cross-platform deployment, variation count
- `analyze_competitor_strategy` — Pull all ads from a page ID, cluster by concept, identify winning angles
- `build_swipe_file` — Curate top-performing competitor ads across multiple advertisers
- `track_competitor` — Store baseline, detect new/killed/scaled ads on subsequent calls

**Winner Ad Scoring:**
| Signal | Why | Detection |
|---|---|---|
| Longevity | Advertisers kill losers fast | `days_active > 30` = likely profitable |
| Spend volume | Higher bucket = scaling | `spend.lower_bound` in top ranges |
| Still active | Running = making money | `ad_active_status == ACTIVE` |
| Multiple variations | Testing a proven angle | Similar copy, different media |
| Cross-platform | Confidence in creative | `publisher_platforms` count > 1 |

**AI Analysis Layer:**
- Hook classification (question, statistic, pain point, curiosity gap, social proof)
- CTA extraction and pattern analysis
- Copy structure identification (PAS, AIDA, Before/After/Bridge)
- Messaging clustering via embeddings to find dominant angles
- Trend detection — which angles are scaling vs. being killed

### TikTok Creative Center — Priority: P2
Internal endpoints (unofficial). Top ads filterable by country, industry, objective.
- `tiktok_get_top_ads` — Browse top-performing TikTok ads by vertical
- `tiktok_get_trending_content` — Trending hashtags, sounds, creative patterns

### Google Ads Transparency Center — Priority: P3
No public API. BigQuery dataset for political ads only.
- `google_transparency_search` — Generate URLs for manual review

### SEMrush — Priority: P3
REST API, API key auth.
- `get_competitor_ads` — Competitor ad copies and estimated spend
- `get_keyword_gap` — Keywords competitors rank for that you don't
- `get_domain_overview` — Traffic estimates and top keywords

### Dependencies
```
requests                    # Meta Ad Library API calls
playwright                  # Extract media from ad snapshots
fastmcp, pyyaml
```

---

## Server 4: adloop-creative (AI Creative Generation)

**What it does:** Generate ad images and videos using AI. Research winning ads, then produce original creatives inspired by winning patterns.

### Image Generation — Priority: P1

**Flux (Black Forest Labs)** — Primary. Best quality, excellent text rendering, all aspect ratios, $0.003-0.05/image.
**OpenAI GPT-4o** — Secondary. Best prompt adherence, good text-in-image for headlines/CTAs, $0.04-0.12/image.
**Stability AI** — Bulk. Cheapest at $0.002-0.006/image, ideal for mass A/B variant generation.

**Tools:**
- `generate_ad_image` — Create image from prompt with platform-specific aspect ratios (1:1 feed, 9:16 stories/reels, 16:9 display)
- `generate_image_variants` — Multiple variations of a concept for A/B testing
- `remix_from_competitor` — Analyze a winning ad's patterns, generate original creative inspired by them

### Video Generation — Priority: P1

**Runway ML** — Primary. Best AI video API, official SDK (`runwayml`), 5-10s clips at 720p-1080p, $0.05/credit.
**Creatomate** — Template-based. Purpose-built for ad production, official SDK (`creatomate`), dynamic text/image insertion, multi-format rendering, $49+/mo.
**Higgsfield AI** — Monitor. Focused on short-form social video with character consistency. API maturity uncertain — integrate when stable.

**Tools:**
- `generate_video_ad` — Short video clip from text/image prompt (product reveals, lifestyle scenes)
- `generate_from_template` — Render from Creatomate template with dynamic fields (headline, product image, CTA, colors)
- `adapt_to_placements` — One creative → multiple aspect ratios for all placements
- `generate_ad_variants` — Multiple creative variations for split testing

### Creative Pipeline
```
adloop-intel                    adloop-creative
┌─────────────────┐            ┌──────────────────┐
│ Competitor       │            │                  │
│ Research         │            │  Image Gen       │
│                  │  winning   │  (Flux/GPT-4o/   │
│ → Winner scoring │──patterns──│   Stability)     │
│ → Hook analysis  │            │                  │
│ → CTA patterns   │            │  Video Gen       │
│ → Visual styles  │            │  (Runway/        │
└─────────────────┘            │   Creatomate)    │
                               └────────┬─────────┘
                                        │ assets
                                        ▼
                               adloop-ads
                               ┌──────────────────┐
                               │ meta_draft_ad     │
                               │ draft_rsa         │
                               │ Deploy to         │
                               │ platforms         │
                               └──────────────────┘
```

### Dependencies
```
runwayml                    # AI video generation
creatomate                  # Template-based production
openai                      # GPT-4o image generation
stability-sdk               # Stability AI images
requests                    # Flux API (REST)
fastmcp, pyyaml
```

---

## Server 5: adloop-crm (CRM & Lead Management)

**What it does:** Connect ad platforms to CRM for lead management, automated follow-up, and closed-loop ROI reporting.

### GoHighLevel (GHL) — Priority: P1
OAuth 2.0. Strong API for CRM/pipeline. **Cannot create landing pages via API** (UI-only builder).

**Lead Management:**
- `ghl_create_contact` — Create leads from ad conversions with UTM attribution
- `ghl_create_opportunity` — Assign leads to pipeline stages
- `ghl_trigger_workflow` — Auto-enroll leads in SMS/email sequences
- `ghl_book_appointment` — Schedule sales calls from ad funnels
- `ghl_update_opportunity_status` — Mark as won/lost
- `ghl_search_contacts` — Find contacts by email, phone, tags

**Closed-Loop ROI:**
- `analyze_lead_to_close` — Full funnel: ad click → lead → opportunity → revenue
- Pull pipeline revenue from GHL + ad spend from adloop-ads servers
- Calculate true ROI: ad spend vs. closed deal revenue

**Landing Page Workaround:**
Generate pages externally (HTML via AI), host on Vercel/Cloudflare, pipe form submissions into GHL via API/webhooks.

### Ad Copy Generation — Priority: P2
Leverage the AI assistant already calling the MCP tools — no additional API needed.
- `suggest_ad_variants` — Generate diverse RSA headlines/descriptions
- `suggest_meta_ad_copy` — Primary text, headlines, descriptions for Meta
- `suggest_tiktok_script` — Hook-based scripts for TikTok video ads

### Dependencies
```
httpx                       # GHL API client (no official SDK)
fastmcp, pyyaml
```

---

## Server 6: adloop-reports (Client Reporting)

**What it does:** Generate client-facing reports across all platforms.

### PDF Reports — Priority: P1
Internal using `reportlab` + `jinja2`. No external API.
- `generate_client_report` — Cross-platform performance report as PDF
- Customizable templates per client
- Charts via `matplotlib`/`plotly`

### Google Sheets — Priority: P1
Same Google OAuth. Quick win using `gspread`.
- `export_to_sheets` — Push cross-platform data to Google Sheets
- `update_client_report` — Auto-populate client reporting templates

### Dependencies
```
reportlab                   # PDF generation
jinja2                      # Report templates
matplotlib                  # Charts
gspread                     # Google Sheets
google-auth-oauthlib
fastmcp, pyyaml
```

---

## Shared Components

These packages are extracted into a shared library (`adloop-core`) used by all servers:

```
adloop-core/
├── safety/
│   ├── preview.py          # ChangePlan, store_plan, get_plan (platform-agnostic)
│   ├── guards.py           # Budget caps, blocked operations, account allowlist
│   └── audit.py            # Mutation logging
├── auth/
│   └── multi_provider.py   # OAuth flows for Google, Meta, TikTok, Microsoft, LinkedIn, GHL
└── config/
    └── loader.py           # Unified config.yaml loading
```

---

## Deployment

Each server gets its own Docker container and Dokploy application:

| Server | Port | Host Example |
|---|---|---|
| adloop-ads | 3000 | `ads.adloop.yourdomain.com/mcp` |
| adloop-analytics | 3001 | `analytics.adloop.yourdomain.com/mcp` |
| adloop-intel | 3002 | `intel.adloop.yourdomain.com/mcp` |
| adloop-creative | 3003 | `creative.adloop.yourdomain.com/mcp` |
| adloop-crm | 3004 | `crm.adloop.yourdomain.com/mcp` |
| adloop-reports | 3005 | `reports.adloop.yourdomain.com/mcp` |

Connect all to Claude Code:
```bash
claude mcp add adloop-ads --transport http https://ads.adloop.yourdomain.com/mcp
claude mcp add adloop-analytics --transport http https://analytics.adloop.yourdomain.com/mcp
claude mcp add adloop-intel --transport http https://intel.adloop.yourdomain.com/mcp
claude mcp add adloop-creative --transport http https://creative.adloop.yourdomain.com/mcp
claude mcp add adloop-crm --transport http https://crm.adloop.yourdomain.com/mcp
claude mcp add adloop-reports --transport http https://reports.adloop.yourdomain.com/mcp
```

---

## Priority Matrix

| Server | Integration | Effort | Value | Priority |
|---|---|---|---|---|
| **adloop-ads** | Meta Ads | Medium | Very High | P1 |
| **adloop-analytics** | Google Search Console | Low | High | P1 |
| **adloop-analytics** | Meta CAPI + Enhanced Conversions | Low | High | P1 |
| **adloop-intel** | Meta Ad Library | Medium | Very High | P1 |
| **adloop-intel** | Winner Scoring Engine | Medium | Very High | P1 |
| **adloop-creative** | Image Gen (Flux + GPT-4o) | Medium | Very High | P1 |
| **adloop-creative** | Video Gen (Runway + Creatomate) | Medium | High | P1 |
| **adloop-ads** | TikTok Ads | Medium | High | P2 |
| **adloop-ads** | Bing Ads | Medium | Medium-High | P2 |
| **adloop-analytics** | Cross-Platform Budget Optimizer | Medium | Very High | P2 |
| **adloop-intel** | TikTok Creative Center | Medium | Medium | P2 |
| **adloop-intel** | Swipe File Builder | Medium | High | P2 |
| **adloop-crm** | GHL Integration | Medium | High | P2 |
| **adloop-reports** | PDF Reports | Medium | Medium-High | P2 |
| **adloop-reports** | Google Sheets | Low | Medium | P2 |
| **adloop-ads** | LinkedIn Ads | Medium | High (B2B) | P3 |
| **adloop-intel** | SEMrush | Medium | Medium | P3 |
| **adloop-crm** | Closed-Loop ROI Reporting | Medium | Very High | P3 |
| **adloop-analytics** | UTM Manager | Low | Medium | P3 |
