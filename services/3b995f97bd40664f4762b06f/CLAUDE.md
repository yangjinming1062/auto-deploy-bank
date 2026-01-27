# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Brick is an open-source RDF schema for building metadata. It consists of:
- An RDF class hierarchy (OWL ontology) describing building subsystems and entities
- A set of relationships for connecting building entities into a directed graph
- SHACL shapes for validation and tag-based class inference

The ontology is generated programmatically from Python dictionaries in `bricksrc/`, then serialized to `Brick.ttl`.

## Common Commands

```bash
# Generate the Brick ontology (required before running tests)
make

# Run all tests
pytest

# Run specific test categories
pytest tests/test_inference.py          # Tag/class inference tests
pytest tests/test_quantities.py         # Quantity/unit tests
pytest tests/test_hierarchy_inference.py  # Class hierarchy tests
pytest tests/test_measures_inference.py   # Substance/quantity inference

# Format code
make format

# Run pre-commit hooks
pre-commit run --all-files

# Version comparison
python tools/compare_versions/compare_versions.py --oldbrick 1.0.3 URL --newbrick 1.1.0 ./Brick.ttl
```

Using uv (recommended):
```bash
uv sync              # Install dependencies
uv run pytest        # Run tests
uv run make          # Generate ontology
uv run python generate_brick.py
```

## Architecture

### Ontology Generation Pipeline

1. **Definition sources** (`bricksrc/*.py`): Python dictionaries define Brick classes and relationships
   - `equipment.py`: Equipment subclasses (HVAC, ICT, Security, Safety)
   - `sensor.py`, `setpoint.py`, `command.py`, `alarm.py`, `status.py`: Point types
   - `location.py`: Location hierarchies (Zone, Room, Floor, etc.)
   - `quantities.py`, `substances.py`: Measurable quantities and substances
   - `relationships.py`: Object/datatype properties (hasPoint, feedsAir, etc.)
   - `entity_properties.py`: Entity property definitions with SHACL shapes

2. **Main generation** (`generate_brick.py`): Combines all definitions into RDF triples
   - Uses `rdflib` to build OWL ontology and SHACL shapes
   - Generates tag inference rules via SHACL-AF
   - Outputs: `Brick.ttl`, `Brick+imports.ttl`, `Brick+extensions.ttl`, `Brick-only.ttl`

3. **Ontology imports** (`bricksrc/ontology.py`): Defines metadata and external imports
   - Imports: QUDT (units), BACnet, RealEstateCore (REC), REF (ASHRAE 223)

4. **Definitions file** (`bricksrc/definitions.csv`): Human-readable definitions for Brick classes

### Key Files

- `bricksrc/namespaces.py`: RDF namespace definitions (BRICK, TAG, OWL, SKOS, QUDT, etc.)
- `bricksrc/version.py`: Version number (semver: major.minor.patch)
- `handle_extensions.py`: Processes extension modules that add classes/properties
- `validation.ttl`: SHACL validation rules for Brick models

### Tag-Based Classification

Classes are defined by their tags. Applying `hasTag` relationships to an entity triggers SHACL rules that infer the most specific class. For example, an entity with `[TAG.Point, TAG.Air, TAG.Temperature, TAG.Sensor]` is inferred as an `Air_Temperature_Sensor`.

## Extending the Ontology

### Adding a New Class

1. Add class definition to the appropriate `bricksrc/<type>.py` file:
```python
"My_New_Sensor": {
    "tags": [TAG.Sensor, TAG.New, TAG.Measurement],
    "subclasses": {...}
}
```

2. Add definition text to `bricksrc/definitions.csv` (alphabetically ordered)

3. Regenerate: `make`

### Adding a New Property

Edit `bricksrc/relationships.py`:
```python
"myProperty": {
    A: [OWL.ObjectProperty],
    "domain": BRICK.Equipment,
    "range": BRICK.Point,
    SKOS.definition: Literal("Description of the relationship"),
}
```

### Extensions

Extensions are Python modules that define additional classes/properties. They are loaded via:
```bash
python generate_brick.py extensions.demo.new_sensors
```

## Dependencies

- **rdflib**: RDF graph management and serialization
- **pyshacl**: SHACL validation
- **brickschema**: Additional Brick tooling and reasoning
- **owlrl**: OWL inference

## Versioning

Semantic versioning (major.minor.patch). Patch releases merged to `master`; minor releases developed in separate branches (e.g., `v1.3`) and merged when ready.

## Imports

The ontology imports external vocabularies defined in `bricksrc/ontology.py`. These are resolved at build time and saved to `imports/`.