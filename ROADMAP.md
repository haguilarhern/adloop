# AdLoop MCP — Product Roadmap

The vision: turn AdLoop into the **ultimate MCP server for media buyers** — a single AI-driven interface to manage ads, analytics, creative generation, competitor research, CRM, and cross-platform optimization.

---

## Phase 1 — Meta Ads + Server-Side Tracking

### Meta (Facebook/Instagram) Ads Integration
Second-largest ad platform. Official Python SDK (`facebook-business`). OAuth 2.0 with system user tokens (never expire).

**Read Tools:**
- `meta_get_campaign_performance` — Metrics with breakdowns by age, gender, placement, device
- `meta_get_adset_performance` — Ad set level including targeting and budget
- `meta_get_ad_performance` — Ad-level metrics with creative details
- `meta_list_audiences` — Custom and lookalike audiences with sizes
- `meta_get_reach_estimate` — Estimate audience size for a targeting spec
- `meta_get_delivery_estimate` — Forecast reach/impressions for a budget

**Write Tools (draft-then-confirm):**
- `meta_draft_campaign` — Create campaign with objective (awareness, traffic, conversions, leads, sales)
- `meta_draft_adset` — Create ad set with targeting, budget, placements, optimization goal
- `meta_draft_ad` — Create ad linking creative to ad set
- `meta_create_lookalike_audience` — Build lookalike from existing audience (1-10% similarity)
- `meta_pause_entity` / `meta_enable_entity` — Status changes
- `meta_confirm_and_apply` — Execute previewed changes

**Meta-Unique Features:**
- Lookalike audiences (Google deprecated similar audiences)
- Placement optimization across Facebook, Instagram, Messenger, Audience Network
- Breakdown reporting by age, gender, platform, placement in a single query
- Lead Ads (instant forms) — collect leads without a landing page
- Dynamic/catalog ads — automatically show products from a feed

**Safety Adaptations:**
- Budget in cents (not micros) — divide by 100 instead of 1,000,000
- Spend cap guard — check account spend cap before budget increases
- Special Ad Category enforcement (housing, employment, credit)
- Audience size minimum warnings

### Meta Conversions API (CAPI)
Server-side event tracking for improved attribution post-iOS 14.5. Same SDK.
- `meta_send_conversion_event` — Send purchase, lead, add-to-cart events server-side

### Google Enhanced Conversions
Already have the `google-ads` SDK. Add `ConversionUploadService`.
- `upload_enhanced_conversions` — Send hashed first-party data for better conversion matching

### Google Search Console
Same Google OAuth already configured. Very low effort, high value.
- `get_organic_search_performance` — Queries, impressions, clicks, CTR, position
- `find_paid_organic_overlap` — Keywords where you're paying for traffic you'd get organically
- `identify_seo_opportunities` — High-impression/low-CTR organic queries to target with paid

---

## Phase 2 — Competitor Research & Ad Intelligence

### Meta Ad Library API
Official REST API (`GET /ads_archive`). Requires identity-verified access token with `ads_read` permission. 200 calls/hour rate limit.

**Tools:**
- `search_competitor_ads` — Search by keyword, advertiser page ID, country, platform, media type
- `find_winner_ads` — Score ads by longevity, spend bucket, cross-platform deployment, variation count
- `analyze_competitor_strategy` — Pull all ads from a page ID, cluster by concept, identify winning angles
- `build_swipe_file` — Curate top-performing competitor ads across multiple advertisers
- `track_competitor` — Store baseline, detect new/killed/scaled ads on subsequent calls

**Winner Ad Scoring:**
- Longevity (ads running 30+ days are likely profitable)
- Spend volume (higher spend bucket = scaling)
- Still active = strong signal
- Multiple variations of same concept = testing a proven angle
- Cross-platform deployment = confidence in creative

**AI Analysis Layer:**
- Hook classification (question, statistic, pain point, curiosity gap, social proof)
- CTA extraction and pattern analysis
- Copy structure identification (PAS, AIDA, Before/After/Bridge)
- Messaging clustering via embeddings to find dominant angles
- Trend detection — which angles are scaling vs. being killed

### TikTok Creative Center
No official API, but internal endpoints accessible. Top-performing ad examples filterable by country, industry, objective, format, time period.
- `tiktok_get_top_ads` — Browse top-performing TikTok ads by vertical and objective
- `tiktok_get_trending_content` — Trending hashtags, sounds, and creative patterns

### Google Ads Transparency Center
No public API. BigQuery public dataset available for political ads only.
- `google_transparency_search` — Generate URLs for manual review (no scraping)
- BigQuery integration for political ad research if needed

---

## Phase 3 — AI Creative Generation

### Image Generation
**Primary: Flux (Black Forest Labs)** — Best image quality, excellent text rendering, flexible aspect ratios, $0.003-0.05/image.
**Secondary: OpenAI GPT-4o** — Best prompt adherence, good text-in-image for headlines/CTAs, $0.04-0.12/image.
**Bulk: Stability AI** — Cheapest ($0.002-0.006/image), great for mass A/B variant generation.

**Tools:**
- `generate_ad_image` — Create ad image from prompt with platform-specific aspect ratios (1:1 feed, 9:16 stories/reels, 16:9 display)
- `generate_image_variants` — Generate multiple variations of a concept for A/B testing
- `remix_from_competitor` — Analyze a winning competitor ad, generate original creative inspired by the same patterns

### Video Generation
**Primary: Runway ML** — Best AI video generation API, official Python SDK (`runwayml`), 5-10s clips at 720p-1080p.
**Template-based: Creatomate** — Purpose-built for automated ad video/image production, official Python SDK (`creatomate`), supports dynamic text/image insertion, multi-format rendering.

**Tools:**
- `generate_video_ad` — Create short video clip from text/image prompt (product reveals, lifestyle scenes)
- `generate_from_template` — Render ad creative from Creatomate template with dynamic fields (headline, product image, CTA, colors)
- `adapt_to_placements` — One creative → multiple aspect ratios for all placements

### Creative Pipeline
```
Competitor Research (Phase 2)
    → Identify winning patterns
    → Extract hooks, CTAs, visual styles
        ↓
Creative Brief (AI-generated)
    → Prompt for image/video generation
    → Template selection + dynamic fields
        ↓
Asset Generation (Phase 3)
    → Flux/GPT-4o for images
    → Runway ML for video clips
    → Creatomate for template-based production
        ↓
Ad Creation (Phase 1)
    → meta_draft_ad / draft_responsive_search_ad
    → Upload generated assets
    → Deploy across platforms
```

---

## Phase 4 — TikTok, Bing, Cross-Platform Optimization

### TikTok Ads
Fastest-growing ad platform. Official Python SDK (`tiktok-business-api-sdk`). OAuth 2.0.

**Tools:**
- Campaign/ad group/ad CRUD with draft-then-confirm
- Performance reporting with breakdowns
- Custom and lookalike audience management
- Spark Ads (boost organic TikTok posts as ads)
- TikTok Events API — server-side conversion tracking

### Microsoft/Bing Ads
5-10% of search market. Official Python SDK (`bingads`). Unique LinkedIn profile targeting on search.

**Tools:**
- Campaign management (nearly identical entity model to Google Ads)
- `import_from_google_ads` — API to directly import Google campaigns into Bing
- LinkedIn-data-based B2B targeting (unique to Microsoft)
- Performance reporting comparable to Google Ads

### Cross-Platform Budget Optimizer
No external API — internal algorithm using `scipy.optimize`. **Key differentiator.**

**Tools:**
- `analyze_cross_platform_efficiency` — Compare CPA/ROAS across Google, Meta, TikTok, Bing
- `suggest_budget_reallocation` — Recommend budget shifts based on marginal returns curves
- `simulate_budget_scenario` — Forecast results of a proposed allocation

### Ad Copy Generation
Leverage the AI assistant already calling the MCP tools — no additional API needed.
- `suggest_ad_variants` — Generate diverse RSA headlines/descriptions
- `suggest_meta_ad_copy` — Generate primary text, headlines, descriptions for Meta
- Works across platforms using the LLM already in context

---

## Phase 5 — CRM Integration & Closed-Loop Reporting

### GoHighLevel (GHL) CRM
Strong API for CRM/pipeline. OAuth 2.0. **Cannot create landing pages programmatically** (UI-only builder).

**What's feasible:**
- `ghl_create_contact` — Create leads from ad conversions with UTM attribution
- `ghl_create_opportunity` — Assign leads to pipeline stages automatically
- `ghl_trigger_workflow` — Auto-enroll leads in follow-up sequences (SMS, email)
- `ghl_book_appointment` — Schedule sales calls from ad funnels
- `ghl_update_opportunity_status` — Mark leads as won/lost

**Closed-Loop ROI Reporting:**
- Pull pipeline revenue from GHL + ad spend from Google/Meta/TikTok
- Calculate true ROI: ad spend vs. closed deal revenue
- `analyze_lead_to_close` — Full funnel: ad click → lead → opportunity → revenue

**Landing Page Workaround:**
GHL can't build pages via API, so generate pages externally (HTML via AI), host on Vercel/Cloudflare, pipe form submissions into GHL via API/webhooks.

### LinkedIn Ads
Essential for B2B agencies. No official Python SDK (build REST client). Approval process can be slow.

**Tools:**
- Campaign management (campaign groups, campaigns, creatives)
- B2B targeting — job title, company, industry, seniority, skills, company size
- Lead Gen Forms — pull submitted leads
- Matched Audiences — company/contact list targeting

### SEMrush Integration
Competitor intelligence. REST API, API key auth.
- `get_competitor_ads` — See competitor ad copies and estimated spend
- `get_keyword_gap` — Find keywords competitors rank for that you don't
- `get_domain_overview` — Traffic estimates and top keywords

---

## Phase 6 — Reporting & Utilities

### PDF Report Generation
Internal using `reportlab` + `jinja2`. No external API.
- `generate_client_report` — Cross-platform performance report as PDF
- Customizable templates per client
- Charts via `matplotlib`/`plotly`

### Google Sheets Reporting
Same Google OAuth. Quick win using `gspread`.
- `export_to_sheets` — Push cross-platform data to Google Sheets
- `update_client_report` — Auto-populate client reporting templates

### UTM Parameter Manager
Pure internal logic, no external API.
- `generate_utm` — Create consistent UTMs across all platforms
- `audit_utm_consistency` — Check for inconsistencies across active campaigns

---

## Architecture

### Module Structure
```
src/adloop/
├── ads/              # Google Ads (existing)
├── ga4/              # Google Analytics (existing)
├── meta/             # Meta/Facebook Ads (new)
│   ├── client.py
│   ├── read.py
│   ├── write.py
│   └── audiences.py
├── tiktok/           # TikTok Ads (new)
├── bing/             # Microsoft Ads (new)
├── linkedin/         # LinkedIn Ads (new)
├── ghl/              # GoHighLevel CRM (new)
├── intelligence/     # Competitor research & ad libraries (new)
│   ├── meta_library.py
│   ├── tiktok_creative.py
│   ├── winner_scoring.py
│   └── swipe_file.py
├── creative/         # AI creative generation (new)
│   ├── image_gen.py      # Flux, GPT-4o, Stability AI
│   ├── video_gen.py      # Runway ML
│   └── templates.py      # Creatomate
├── optimizer/        # Cross-platform budget optimization (new)
├── seo/              # Search Console + keyword research (new)
├── reporting/        # PDF/Sheets generation (new)
├── tracking/         # Existing + CAPI + Enhanced Conversions (extend)
├── safety/           # Existing (extend for multi-platform)
└── server.py         # All tool registrations
```

### Multi-Platform Auth
```yaml
# config.yaml
google:
  credentials_path: ~/.adloop/credentials.json
  token_path: ~/.adloop/token.json
meta:
  app_id: "..."
  app_secret: "..."
  system_user_token: "..."
tiktok:
  app_id: "..."
  app_secret: "..."
  access_token: "..."
microsoft:
  client_id: "..."
  developer_token: "..."
  refresh_token: "..."
linkedin:
  client_id: "..."
  client_secret: "..."
  access_token: "..."
ghl:
  client_id: "..."
  client_secret: "..."
  location_id: "..."
creative:
  flux_api_key: "..."
  openai_api_key: "..."
  runway_api_key: "..."
  creatomate_api_key: "..."
  stability_api_key: "..."
intelligence:
  meta_ad_library_token: "..."
  semrush_api_key: "..."
```

### New Dependencies
```
facebook-business            # Meta Ads + CAPI
tiktok-business-api-sdk      # TikTok Ads + Events
bingads                       # Microsoft Advertising
runwayml                      # AI video generation
creatomate                    # Template-based ad production
openai                        # GPT-4o image generation
stability-sdk                 # Stability AI images
gspread                       # Google Sheets
scipy                         # Budget optimization
reportlab                     # PDF generation
jinja2                        # Report templates
```

---

## Priority Matrix

| Integration | Effort | Value | Phase |
|---|---|---|---|
| **Meta Ads** | Medium | Very High | P1 |
| **Meta CAPI** | Low | High | P1 |
| **Google Enhanced Conversions** | Low | High | P1 |
| **Google Search Console** | Low | High | P1 |
| **Meta Ad Library (competitor research)** | Medium | Very High | P2 |
| **Winner Ad Scoring Engine** | Medium | Very High | P2 |
| **Swipe File Builder** | Medium | High | P2 |
| **AI Image Generation (Flux + GPT-4o)** | Medium | Very High | P3 |
| **AI Video Generation (Runway ML)** | Medium | High | P3 |
| **Template-Based Production (Creatomate)** | Medium | High | P3 |
| **TikTok Ads** | Medium | High | P4 |
| **Bing Ads** | Medium | Medium-High | P4 |
| **Cross-Platform Budget Optimizer** | Medium | Very High | P4 |
| **Ad Copy Generation** | Low | High | P4 |
| **GHL CRM Integration** | Medium | High | P5 |
| **LinkedIn Ads** | Medium | High (B2B) | P5 |
| **SEMrush** | Medium | Medium | P5 |
| **Closed-Loop ROI Reporting** | Medium | Very High | P5 |
| **PDF Reports** | Medium | Medium-High | P6 |
| **Google Sheets Reporting** | Low | Medium | P6 |
| **UTM Manager** | Low | Medium | P6 |
