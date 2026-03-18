# AdLoop

MCP server connecting Google Ads + GA4 into one AI-driven feedback loop. Deploy it as an HTTP server and connect it to Claude Code, Cursor, or any MCP-compatible AI assistant to read performance data, manage campaigns, and cross-reference Ads with Analytics — all through natural language.

## Features

### Google Ads (Read)
- **list_accounts** — List all accessible accounts under your MCC
- **get_campaign_performance** — Campaign metrics: impressions, clicks, cost, conversions, CPA, ROAS
- **get_ad_performance** — Ad-level data including RSA headlines, descriptions, final URLs
- **get_keyword_performance** — Keyword metrics with quality scores
- **get_search_terms** — What users actually typed before clicking your ads
- **get_negative_keywords** — List existing negative keywords
- **run_gaql** — Execute arbitrary GAQL queries for advanced analysis

### Google Ads (Write)
All write operations use a **draft-then-confirm** safety pattern. Nothing changes until you explicitly approve.

- **draft_campaign** — Create a full campaign structure (budget + campaign + ad group + keywords)
- **draft_responsive_search_ad** — Create RSA ads with headlines and descriptions
- **draft_keywords** — Add keywords to an ad group
- **add_negative_keywords** — Add negative keywords to a campaign
- **pause_entity / enable_entity** — Pause or enable campaigns, ad groups, ads, keywords
- **remove_entity** — Permanently remove entities (irreversible)
- **confirm_and_apply** — Execute a previewed change (defaults to dry_run=true)

### GA4 (Read)
- **get_account_summaries** — List all GA4 properties
- **run_ga4_report** — Custom reports with dimensions, metrics, date ranges
- **run_realtime_report** — Current active users and events
- **get_tracking_events** — All GA4 events and their volume

### Cross-Channel Analytics
- **analyze_campaign_conversions** — Map Ads clicks to GA4 conversions for real cost-per-conversion
- **landing_page_analysis** — Find pages that get ad clicks but zero conversions
- **attribution_check** — Compare Ads-reported vs GA4-reported conversions

### Tracking Tools
- **validate_tracking** — Compare codebase tracking events against actual GA4 data
- **generate_tracking_code** — Generate ready-to-paste gtag snippets

### Budget Planning
- **estimate_budget** — Forecast clicks, impressions, and cost using Keyword Planner

### Account Access Management
- **add_allowed_account** — Add an account to the allowlist
- **remove_allowed_account** — Remove an account from the allowlist
- **list_allowed_accounts** — Show allowed accounts with names

### Safety
- Configurable daily budget cap (prevents accidentally creating expensive campaigns)
- Dry-run mode enabled by default on all writes
- Full audit log of every mutation
- Broad match keyword warnings when Smart Bidding is not active
- Account allowlist to restrict which accounts can be accessed

## Prerequisites

- Python 3.11+
- A Google Ads MCC (Manager) account
- A Google Ads API Developer Token (from the API Center in your MCC)
- A Google Cloud project with these APIs enabled:
  - Google Ads API
  - Google Analytics Data API
  - Google Analytics Admin API
- OAuth 2.0 Desktop credentials (Client ID + Client Secret)
- An OAuth refresh token

## Setup

### 1. Google Cloud Project

1. Create a project at [console.cloud.google.com](https://console.cloud.google.com)
2. Enable the required APIs:
   - Google Ads API
   - Google Analytics Data API
   - Google Analytics Admin API
3. Go to **Google Auth Platform > Branding** and configure the consent screen
4. Set the publishing status to **In production** (otherwise refresh tokens expire in 7 days)
5. Go to **Google Auth Platform > Clients** and create a **Desktop app** OAuth client
6. Note down the **Client ID** and **Client Secret**

### 2. Generate a Refresh Token

```bash
pip install google-auth-oauthlib
python get_refresh_token.py --client-id YOUR_CLIENT_ID --client-secret YOUR_CLIENT_SECRET
```

This opens a browser for authorization and prints your refresh token.

### 3. Deploy

#### Docker (recommended)

```bash
docker build -t adloop .
docker run -p 3000:3000 adloop
```

The server will be available at `http://localhost:3000/mcp`.

#### Local

```bash
uv sync
uv run adloop --transport streamable-http
```

### 4. Connect to Claude Code

```bash
claude mcp add adloop-mcp --transport http http://YOUR_HOST:3000/mcp
```

### 5. Configure Credentials

Once connected, call the `setup_credentials` tool with your credentials:

```
developer_token: Your Google Ads API developer token
customer_id: Your MCC account ID (no dashes)
login_customer_id: Same as customer_id for MCC
oauth_client_id: From Google Cloud Console
oauth_client_secret: From Google Cloud Console
oauth_refresh_token: From step 2
google_project_id: Your Google Cloud project ID
max_daily_budget: Safety cap for new campaigns (default 50.0)
require_dry_run: true (recommended)
```

### 6. Restrict Account Access (Optional)

By default, all accounts under your MCC are accessible. To restrict to specific accounts:

```
add_allowed_account("869-012-1119")
add_allowed_account("975-324-5852")
```

Use `list_allowed_accounts` to see the current allowlist with account names, and `remove_allowed_account` to revoke access.

### 7. Verify

Run `health_check` to confirm Google Ads and GA4 connectivity.

## Usage Examples

**Check campaign performance:**
> "Show me campaign performance for Bubba's Tubs & Pools for the last 30 days"

**Find wasted spend:**
> "What search terms triggered ads on the Hot Frost account? Show me any that look irrelevant"

**Add negative keywords:**
> "Add 'free' and 'DIY' as negative keywords to campaign 12345678 on account 869-012-1119"

**Cross-channel analysis:**
> "Compare Google Ads conversions vs GA4 conversions for Destination St. John's — are there discrepancies?"

**Budget planning:**
> "Estimate traffic for the keywords 'hot tub installation' and 'pool supplies' in Canada"

## Architecture

```
Claude Code / Cursor / AI Assistant
        │
        │ MCP Protocol (streamable-http)
        ▼
   ┌─────────────┐
   │  AdLoop MCP  │
   │   Server     │
   └──────┬──────┘
          │
    ┌─────┴─────┐
    ▼           ▼
Google Ads   GA4 API
  API
```

- **Transport:** Streamable HTTP (`/mcp` endpoint)
- **Framework:** FastMCP 3.x
- **Google Ads API:** v23 (pinned)
- **Safety layer:** All writes go through draft → preview → confirm flow

## Environment Variables

| Variable | Default | Description |
|---|---|---|
| `ADLOOP_HOST` | `0.0.0.0` | Server bind address |
| `ADLOOP_PORT` | `3000` | Server port |
| `ADLOOP_CONFIG` | `~/.adloop/config.yaml` | Config file path |

## License

MIT
