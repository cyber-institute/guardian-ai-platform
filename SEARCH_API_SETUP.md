# Search API Setup for URL Discovery

The GUARDIAN system now uses web search APIs to find document source URLs efficiently, avoiding token usage for simple URL discovery tasks.

## Supported Search APIs

### 1. Google Custom Search API (Recommended)
- **Cost**: Free tier: 100 searches/day, Paid: $5 per 1000 queries
- **Setup**:
  1. Go to [Google Cloud Console](https://console.cloud.google.com/)
  2. Enable Custom Search API
  3. Create a Custom Search Engine at [programmablesearchengine.google.com](https://programmablesearchengine.google.com/)
  4. Get your API key and Search Engine ID (CX)

**Environment Variables:**
```bash
GOOGLE_SEARCH_API_KEY=your_api_key_here
GOOGLE_SEARCH_CX=your_search_engine_id_here
```

### 2. Bing Search API
- **Cost**: Free tier: 1000 searches/month, Paid: $7 per 1000 queries
- **Setup**:
  1. Go to [Azure Portal](https://portal.azure.com/)
  2. Create a Bing Search v7 resource
  3. Get your subscription key

**Environment Variables:**
```bash
BING_SEARCH_API_KEY=your_subscription_key_here
```

### 3. DuckDuckGo Instant Answer API (Free)
- **Cost**: Free
- **Limitations**: Limited results, rate limited
- **Setup**: No API key required, works out of the box

## Search Strategy

The system uses a multi-tier approach:

1. **Content Analysis**: First checks if URLs are already present in document content
2. **Google Custom Search**: Primary search with targeted queries
3. **Bing Search**: Fallback search with different algorithms  
4. **DuckDuckGo**: Free backup option
5. **Pattern Construction**: Fallback to known URL patterns for NIST, CISA, etc.

## Query Optimization

The system builds intelligent search queries:
- `"Document Title" filetype:pdf`
- `site:nist.gov "Document Title"`
- `site:cisa.gov "Document Title"`
- `"NIST SP 800-218A" site:nvlpubs.nist.gov`

## Trusted Domains

Only URLs from trusted sources are accepted:
- Government: nist.gov, cisa.gov, nasa.gov, whitehouse.gov, nsa.gov
- Standards: ieee.org, iso.org, ietf.org, w3.org
- Academic: doi.org, arxiv.org, acm.org, ncbi.nlm.nih.gov

## Usage Examples

```python
# Basic usage (no API keys required for DuckDuckGo fallback)
from utils.web_search_url_discovery import find_document_url_with_search

url = find_document_url_with_search(
    title="NIST SP 800-218A Secure Software Development Practices",
    organization="NIST",
    content="Document content..."
)
```

## Benefits vs LLM Token Usage

- **Cost Effective**: Search APIs cost $5-7 per 1000 queries vs $10-50 in LLM tokens
- **Faster**: Direct API calls vs multi-turn LLM conversations
- **More Accurate**: Specialized search algorithms vs general language understanding
- **Real-time**: Live web index vs training data cutoff
- **Scalable**: Rate limits vs token quotas

## Setup Priority

1. **Immediate**: System works with DuckDuckGo (free, no setup)
2. **Recommended**: Add Google Custom Search for best results
3. **Optional**: Add Bing Search for redundancy

The system gracefully degrades from paid APIs to free options automatically.