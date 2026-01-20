# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Cello is a **genetic circuit design automation tool** built with Spring Boot. It takes Verilog code (hardware description language) as input and outputs DNA sequences that implement the specified logic in living cells. The system maps Boolean logic to genetic parts (promoters, gates, transcriptional units) using computational algorithms.

## Build Commands

```bash
# Install local JAR dependencies (NetSynth, Eugene) to ~/.m2/repository
cd src/main/webapp/resources/library && bash install_local_jars.sh

# Compile the project
mvn clean compile

# Run tests
mvn test

# Run with CelloMain profile (command-line interface)
mvn -f ~/cello/pom.xml -DskipTests=true -PCelloMain -Dexec.args="-verilog demo_verilog.v"
```

## Run Commands

```bash
# Start web application (http://127.0.0.1:8080)
mvn spring-boot:run

# Results directory must exist at same level as repository (e.g., ~/cello_results/)
mkdir ~/cello_results/
```

## Key Options

Common command-line options (see `Args.java`):
- `-verilog <file.v>`: Verilog input file
- `-input_promoters <file.txt>`: Input promoter data
- `-output_genes <file.txt>`: Output gene data
- `-UCF <file.UCF.json>`: User Constraint File (gate library)
- `-assignment_algorithm [breadth_first|hill_climbing|simulated_annealing]`
- `-plasmid false`: Skip plasmid design
- `-eugene false`: Skip Eugene enumeration

## Architecture

### Processing Pipeline

1. **Input Layer** (`api/`): REST endpoints accept Verilog code
2. **Logic Synthesis** (`MIT/dnacompiler/`): ANTLR Verilog parser → NetSynth → NOR-Inverter Graph
3. **Gate Assignment** (`BuildCircuits*.java`): Maps Boolean gates to genetic gates using response functions (Hill equation). Algorithms: breadth-first search, hill climbing, simulated annealing.
4. **Plasmid Design** (`adaptors/`): Eugene language for combinatorial DNA assembly

### Key Directories

- `src/main/java/org/cellocad/`: Main Java source
  - `api/`: REST controllers (MainController, UCFController, FileController)
  - `MIT/dnacompiler/`: Core logic (~72KB), includes DNACompiler, Args, Gate, UCF
  - `MIT/logic_motif_synthesis/`: Circuit optimization
  - `adaptors/`: UCF, SBOL, MySQL, Eugene integrations
- `resources/UCF/`: Pre-defined gate libraries (UCF.json files)
- `resources/data/`: Input promoters, output genes, tandem promoter data
- `src/main/webapp/`: HTML/JS frontend

### Critical Dependencies

- **NetSynth.jar**: Logic synthesis from Verilog (local JAR)
- **Eugene-2.0.0**: Genetic design rule language (requires Java 1.7, not 1.8)
- **libSBOLj 2.2.1**: SBOL support
- **ANTLR 4.3**: Verilog grammar parsing

## Testing

Test files are in `src/test/java/`:
- `PermuteTest.java`: Permutation testing
- `ReloadCircuitsTest.java`: Circuit reload validation
- `EugeneMajorityCircuit.java`: Integration test with Eugene

## Database

- Uses Apache Derby for authentication (auto-created)
- MySQL connector available for production use

## API Usage

```bash
# Test connection
curl -u "username:password" http://127.0.0.1:8080/ping

# Submit design
curl -u "username:password" -X POST http://127.0.0.1:8080/submit \
  --data-urlencode "id=job001" \
  --data-urlencode "verilog_text@demo_verilog.v"
```

## Notes

- Java 1.7 required when using Eugene (v2.0.0 incompatible with Java 1.8)
- Optional figure generation requires: gnuplot, ghostscript, ImageMagick, graphviz
- Default input promoters: pTac, pTet, pBAD; default output: YFP