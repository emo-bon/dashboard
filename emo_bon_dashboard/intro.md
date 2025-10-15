# EMO-BON Dashboard

Welcome to the **EMO-BON (European Marine Omics Biodiversity Observation Network) Dashboard**!

This dashboard provides insights and visualizations of the EMO-BON Knowledge Graph, which contains data about marine observatories, sampling events, and quality analysis of the data.

## What's in this Dashboard?

This Jupyter Book is organized into the following sections:

:::{mermaid}
graph TD
    A[EMO-BON Dashboard] --> B[Dashboard Overview]
    A --> C[Quality Analysis]
    B --> D[Observatories]
    B --> E[Samples]
    C --> F[Data Quality Checks]
    C --> G[Validation Reports]
:::

### Dashboard Overview
Interactive visualizations and queries showing:
- **Observatories**: Information about marine monitoring stations across Europe
- **Samples**: Details about sampling events, collected specimens, and measurements

### Quality Analysis
SPARQL queries and analyses demonstrating:
- Data quality assessments
- Validation checks on the knowledge graph
- Consistency reports

## Data Source

All data is queried from the EMO-BON Knowledge Graph at:
- GraphDB endpoint: `https://emobon-kb.vliz.be/repositories/kgap`

```{tableofcontents}
```