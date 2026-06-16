# Publication policy

This project is designed to become public later, but it starts as a private repository.

The goal is to separate public-safe documentation from private working material.

## Public-safe content

The following content can be published after review:

- README documentation
- conceptual data model
- CSV schema documentation
- curated sample CSV files
- public-safe equipment categories
- public-safe soundchain examples
- public-safe music reference mappings
- relationship tables with public-safe sample data
- SQL schema and example queries
- Python scripts that do not expose private data
- dashboard screenshots based on curated public data

## Private content

The following content must stay private:

- full private inventory exports
- original Word source documents
- purchase prices
- purchase dates if too detailed
- serial numbers
- invoices
- private condition notes
- private location or storage notes
- complete value-related collection data
- copyrighted manuals or product images
- long copied manufacturer descriptions
- internal ChatGPT or Claude working notes

## Repository rule

Private data may be stored locally during development but must not be committed.

Protected folders:

    data/private/
    sources/private/

These folders are intentionally ignored by Git except for `.gitkeep` placeholder files.

## Public release checklist

Before making the repository public, check:

- no private source documents are committed
- no serial numbers are present
- no prices or sensitive purchase information are present
- no full private inventory is exposed
- no copyrighted third-party files are included
- all uncertain specifications are marked cautiously
- README explains the data project clearly
- sample data is curated and public-safe
- CSV files follow the documented schema
- data-quality assumptions are documented
- relationship tables contain only public-safe IDs and notes
