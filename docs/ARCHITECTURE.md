# System Architecture

This document provides a detailed overview of the system's architecture, data models, and runtime data flow. The diagrams herein are generated using a combination of manual and automated techniques to ensure they are both descriptive and maintainable.

---

## 1. High-Level Component Diagram

This diagram illustrates the major components of the project and their primary interactions. It provides a "bird's-eye view" of the repository's structure.

```mermaid
graph TD
    subgraph "Input & Output"
        A["📄 Raw TSV Data<br>(data/input/)"]
        Z["📊 Final CSV Report<br>(data/output/)"]
    end

    subgraph "Application Core (src/)"
        B["Orchestrator<br>(main.py, run_phase2.py)"]
        C["Shared Configuration<br>(config.py)"]
        D["Shared Data Models<br>(data/models.py)"]

        subgraph "Core Pipeline"
            direction LR
            P1["1. Parsers<br>(parsers/)"]
            P2["2. Extractors<br>(extractors/)"]
            P3["3. Analyzers<br>(analyzers/)"]
        end
    end

    subgraph "Development & Analysis Tooling"
        T1["Nox & Pre-commit<br>(noxfile.py, .pre-commit-config.yaml)"]
        T2["CI/CD Workflow<br>(.github/workflows/pylint.yml)"]
        T3["Analysis Scripts<br>(tools/)"]
    end

    %% Data Flow
    A -- "Reads raw text" --> P1
    P1 -- "Creates List&lt;Token&gt;" --> P2
    P2 -- "Creates List&lt;ClauseMateRelationship&gt;" --> P3
    P3 -- "Enriches relationships" --> B
    B -- "Writes to disk" --> Z

    %% Component Dependencies
    B -- "Uses" --> C
    B -- "Coordinates" --> P1
    B -- "Coordinates" --> P2
    B -- "Coordinates" --> P3
    P1 -- "Uses" --> D
    P2 -- "Uses" --> D
    P3 -- "Uses" --> D
    T3 -- "Analyzes" --> Z
```

---

## 2. Core Data Models (UML Class Diagram)

This diagram shows the primary data structures defined in `src/data/models.py` and their relationships. These models are the backbone of the application, ensuring type safety and clear data contracts between components.

```mermaid
classDiagram
    class Token {
        +idx: int
        +text: str
        +sentence_num: int
        +grammatical_role: str
        +thematic_role: str
        +coreference_link: Optional[str]
        +coreference_type: Optional[str]
    }

    class Phrase {
        +text: str
        +coreference_id: str
        +start_idx: int
        +end_idx: int
        +grammatical_role: str
        +thematic_role: str
        +coreference_type: str
        +animacy: AnimacyType
        +givenness: str
    }

    class AntecedentInfo {
        +most_recent_text: str
        +most_recent_distance: str
        +first_text: str
        +first_distance: str
    }

    class ClauseMateRelationship {
        +sentence_id: str
        +sentence_num: int
        +pronoun: Token
        +clause_mate: Phrase
        +num_clause_mates: int
        +antecedent_info: AntecedentInfo
        +to_dict(): Dict
    }

    class SentenceContext {
        +sentence_id: str
        +sentence_num: int
        +tokens: List~Token~
        +critical_pronouns: List~Token~
        +coreference_phrases: List~CoreferencePhrase~
    }

    ClauseMateRelationship o-- "1" Token : has_pronoun
    ClauseMateRelationship o-- "1" Phrase : has_clause_mate
    ClauseMateRelationship o-- "1" AntecedentInfo : has_antecedent_info
    SentenceContext o-- "*" Token : contains
```

---

## 3. Runtime Data Flow (Sequence Diagram)

This diagram illustrates the sequence of operations when the application is run. It shows how the main orchestrator coordinates the different pipeline components to process the input data and generate the final output.

```mermaid
sequenceDiagram
    participant User
    participant Orchestrator (main.py)
    participant TSVParser (parsers/)
    participant RelationshipExtractor (extractors/)
    participant DistanceAnalyzer (analyzers/)
    participant FileSystem

    User->>Orchestrator: python src/run_phase2.py
    Orchestrator->>FileSystem: Read TSV file
    FileSystem-->>Orchestrator: Return file content

    Orchestrator->>TSVParser: Parse(file_content)
    TSVParser-->>Orchestrator: Return List~SentenceContext~

    loop For each SentenceContext
        Orchestrator->>RelationshipExtractor: Extract(sentence_context)
        RelationshipExtractor-->>Orchestrator: Return List~ClauseMateRelationship~
    end

    loop For each ClauseMateRelationship
        Orchestrator->>DistanceAnalyzer: Analyze(relationship)
        DistanceAnalyzer-->>Orchestrator: Return enriched_relationship
    end

    Orchestrator->>FileSystem: Write enriched relationships to CSV
    FileSystem-->>Orchestrator: Confirm write
    Orchestrator-->>User: Process complete
```

---

## 4. Code-Level Flowchart (Generated)

This diagram provides a more granular, code-level view of the project's execution flow. It is automatically generated from the source code using the `code2flow` tool, showing the call relationships between functions and classes.

```dot
digraph G {
concentrate=true;
splines="ortho";
rankdir="LR";
subgraph legend{
    rank = min;
    label = "legend";
    Legend [shape=none, margin=0, label = <
        <table cellspacing="0" cellpadding="0" border="1"><tr><td>Code2flow Legend</td></tr><tr><td>
        <table cellspacing="0">
        <tr><td>Regular function</td><td width="50px" bgcolor='#cccccc'></td></tr>
        <tr><td>Trunk function (nothing calls this)</td><td bgcolor='#966F33'></td></tr>
        <tr><td>Leaf function (this calls nothing else)</td><td bgcolor='#6db33f'></td></tr>
        <tr><td>Function call</td><td><font color='black'>&#8594;</font></td></tr>
        </table></td></tr></table>
        >];
}node_f6ffcca9 [label="0: (global)()" name="main::(global)" shape="rect" style="rounded,filled" fillcolor="#966F33" ];
node_3198fd76 [label="54: __init__()" name="main::ClauseMateAnalyzer.__init__" shape="rect" style="rounded,filled" fillcolor="#cccccc" ];
node_1e0a34bd [label="113: _analyze_complete()" name="main::ClauseMateAnalyzer._analyze_complete" shape="rect" style="rounded,filled" fillcolor="#cccccc" ];
node_aca7d719 [label="167: _analyze_streaming()" name="main::ClauseMateAnalyzer._analyze_streaming" shape="rect" style="rounded,filled" fillcolor="#cccccc" ];
node_7f773000 [label="238: _extract_sentence_number()" name="main::ClauseMateAnalyzer._extract_sentence_number" shape="rect" style="rounded,filled" fillcolor="#6db3f" ];
node_27f1cfcf [label="87: analyze_file()" name="main::ClauseMateAnalyzer.analyze_file" shape="rect" style="rounded,filled" fillcolor="#cccccc" ];
node_47c58137 [label="198: export_results()" name="main::ClauseMateAnalyzer.export_results" shape="rect" style="rounded,filled" fillcolor="#6db3f" ];
node_ff68e1cf [label="230: get_statistics()" name="main::ClauseMateAnalyzer.get_statistics" shape="rect" style="rounded,filled" fillcolor="#6db3f" ];
node_579f30f0 [label="246: main()" name="main::main" shape="rect" style="rounded,filled" fillcolor="#cccccc" ];
node_095cc69b [label="285: _analyze_antecedents()" name="relationship_extractor::RelationshipExtractor._analyze_antecedents" shape="rect" style="rounded,filled" fillcolor="#cccccc" ];
node_df748bee [label="228: _convert_to_phrase()" name="relationship_extractor::RelationshipExtractor._convert_to_phrase" shape="rect" style="rounded,filled" fillcolor="#cccccc" ];
node_527f5e13 [label="257: _determine_animacy()" name="relationship_extractor::RelationshipExtractor._determine_animacy" shape="rect" style="rounded,filled" fillcolor="#6db3f" ];
node_44dc4c7e [label="441: _extract_occurrence_number()" name="relationship_extractor::RelationshipExtractor._extract_occurrence_number" shape="rect" style="rounded,filled" fillcolor="#6db3f" ];
node_c4de6f11 [label="185: _get_pronoun_coreference_ids()" name="relationship_extractor::RelationshipExtractor._get_pronoun_coreference_ids" shape="rect" style="rounded,filled" fillcolor="#6db3f" ];
node_8109aeee [label="39: extract()" name="relationship_extractor::RelationshipExtractor.extract" shape="rect" style="rounded,filled" fillcolor="#cccccc" ];
node_3ed52370 [label="83: extract_relationships()" name="relationship_extractor::RelationshipExtractor.extract_relationships" shape="rect" style="rounded,filled" fillcolor="#cccccc" ];
node_da72f235 [label="140: find_clause_mates()" name="relationship_extractor::RelationshipExtractor.find_clause_mates" shape="rect" style="rounded,filled" fillcolor="#966F33" ];
node_6557e20b [label="403: enrich_token()" name="tsv_parser::DefaultTokenProcessor.enrich_token" shape="rect" style="rounded,filled" fillcolor="#6db3f" ];
node_2bc925f0 [label="381: validate_token()" name="tsv_parser::DefaultTokenProcessor.validate_token" shape="rect" style="rounded,filled" fillcolor="#6db3f" ];
node_fea27965 [label="28: __init__()" name="tsv_parser::TSVParser.__init__" shape="rect" style="rounded,filled" fillcolor="#6db3f" ];
node_3bb680cc [label="348: _create_sentence_context()" name="tsv_parser::TSVParser._create_sentence_context" shape="rect" style="rounded,filled" fillcolor="#cccccc" ];
node_63f40cc3 [label="333: _extract_first_words()" name="tsv_parser::TSVParser._extract_first_words" shape="rect" style="rounded,filled" fillcolor="#6db3f" ];
node_82235d45 [label="294: _extract_sentence_id()" name="tsv_parser::TSVParser._extract_sentence_id" shape="rect" style="rounded,filled" fillcolor="#6db3f" ];
node_b9c38f81 [label="315: _extract_sentence_num()" name="tsv_parser::TSVParser._extract_sentence_num" shape="rect" style="rounded,filled" fillcolor="#966F33" ];
node_8b2b4219 [label="280: is_sentence_boundary()" name="tsv_parser::TSVParser.is_sentence_boundary" shape="rect" style="rounded,filled" fillcolor="#6db3f" ];
node_9f598d6b [label="42: parse_file()" name="tsv_parser::TSVParser.parse_file" shape="rect" style="rounded,filled" fillcolor="#966F33" ];
node_e588f6df [label="69: parse_sentence_streaming()" name="tsv_parser::TSVParser.parse_sentence_streaming" shape="rect" style="rounded,filled" fillcolor="#cccccc" ];
node_7d1b8ddb [label="186: parse_token_line()" name="tsv_parser::TSVParser.parse_token_line" shape="rect" style="rounded,filled" fillcolor="#6db3f" ];
node_f6ffcca9 -> node_579f30f0 [color="#E69F00" penwidth="2"];
node_3198fd76 -> node_fea27965 [color="#D55E00" penwidth="2"];
node_1e0a34bd -> node_7f773000 [color="#0072B2" penwidth="2"];
node_1e0a34bd -> node_8109aeee [color="#0072B2" penwidth="2"];
node_1e0a34bd -> node_8109aeee [color="#0072B2" penwidth="2"];
node_1e0a34bd -> node_8109aeee [color="#0072B2" penwidth="2"];
node_1e0a34bd -> node_e588f6df [color="#0072B2" penwidth="2"];
node_aca7d719 -> node_8109aeee [color="#E69F00" penwidth="2"];
node_aca7d719 -> node_e588f6df [color="#E69F00" penwidth="2"];
node_27f1cfcf -> node_1e0a34bd [color="#CC79A7" penwidth="2"];
node_27f1cfcf -> node_aca7d719 [color="#CC79A7" penwidth="2"];
node_579f30f0 -> node_3198fd76 [color="#000000" penwidth="2"];
node_579f30f0 -> node_27f1cfcf [color="#000000" penwidth="2"];
node_579f30f0 -> node_47c58137 [color="#000000" penwidth="2"];
node_579f30f0 -> node_ff68e1cf [color="#000000" penwidth="2"];
node_095cc69b -> node_44dc4c7e [color="#009E73" penwidth="2"];
node_095cc69b -> node_c4de6f11 [color="#009E73" penwidth="2"];
node_df748bee -> node_527f5e13 [color="#D55E00" penwidth="2"];
node_8109aeee -> node_3ed52370 [color="#D55E00" penwidth="2"];
node_3ed52370 -> node_095cc69b [color="#000000" penwidth="2"];
node_3ed52370 -> node_df748bee [color="#000000" penwidth="2"];
node_3ed52370 -> node_c4de6f11 [color="#000000" penwidth="2"];
node_da72f235 -> node_c4de6f11 [color="#0072B2" penwidth="2"];
node_3bb680cc -> node_6557e20b [color="#F0E442" penwidth="2"];
node_b9c38f81 -> node_82235d45 [color="#E69F00" penwidth="2"];
node_9f598d6b -> node_e588f6df [color="#009E73" penwidth="2"];
node_e588f6df -> node_2bc925f0 [color="#CC79A7" penwidth="2"];
node_e588f6df -> node_3bb680cc [color="#CC79A7" penwidth="2"];
node_e588f6df -> node_3bb680cc [color="#CC79A7" penwidth="2"];
node_e588f6df -> node_63f40cc3 [color="#CC79A7" penwidth="2"];
node_e588f6df -> node_8b2b4219 [color="#CC79A7" penwidth="2"];
node_e588f6df -> node_7d1b8ddb [color="#CC79A7" penwidth="2"];
subgraph cluster_3fcaca2d {
    node_579f30f0 node_f6ffcca9;
    label="File: main";
    name="main";
    style="filled";
    graph[style=dotted];
    subgraph cluster_3ef21504 {
        node_3198fd76 node_27f1cfcf node_1e0a34bd node_aca7d719 node_47c58137 node_ff68e1cf node_7f773000;
        label="Class: ClauseMateAnalyzer";
        name="ClauseMateAnalyzer";
        style="filled";
        graph[style=dotted];
    };
};
subgraph cluster_5aea24f6 {
    label="File: relationship_extractor";
    name="relationship_extractor";
    style="filled";
    graph[style=dotted];
    subgraph cluster_300af77a {
        node_8109aeee node_3ed52370 node_da72f235 node_c4de6f11 node_df748bee node_527f5e13 node_095cc69b node_44dc4c7e;
        label="Class: RelationshipExtractor";
        name="RelationshipExtractor";
        style="filled";
        graph[style=dotted];
    };
};
subgraph cluster_1fcf976 {
    label="File: tsv_parser";
    name="tsv_parser";
    style="filled";
    graph[style=dotted];
    subgraph cluster_fe1af2ee {
        node_fea27965 node_9f598d6b node_e588f6df node_7d1b8ddb node_8b2b4219 node_82235d45 node_b9c38f81 node_63f40cc3 node_3bb680cc;
        label="Class: TSVParser";
        name="TSVParser";
        style="filled";
        graph[style=dotted];
    };
    subgraph cluster_3b7ae052 {
        node_2bc925f0 node_6557e20b;
        label="Class: DefaultTokenProcessor";
        name="DefaultTokenProcessor";
        style="filled";
        graph[style=dotted];
    };
};
}
```

---

## 5. Diagram Generation and Rendering

This architecture document is a living document, designed to be updated as the codebase evolves. The diagrams are generated using specific tools that translate text-based definitions or source code into visuals. This approach, often called "Diagrams as Code," makes the documentation easy to version control and maintain.

A Python script, `tools/render_arch_doc.py`, automates the process of converting this Markdown file into a standalone HTML document with fully rendered diagrams.

### 5.1. Manually Created Diagrams (Mermaid.js)

The **High-Level Component Diagram**, **Core Data Models (UML)**, and **Runtime Data Flow (Sequence Diagram)** are created using [Mermaid.js](https://mermaid-js.github.io/mermaid/#/).

*   **What it is:** Mermaid is a JavaScript-based tool that renders diagrams and charts from text in a syntax similar to Markdown.
*   **How to reproduce/update:**
    1.  Edit the ` ```mermaid ... ``` ` code blocks directly in this Markdown file.
    2.  The syntax is well-documented on the Mermaid.js website.
    3.  Many Markdown editors (like the one on GitHub or in VS Code with the *Markdown Preview Mermaid Support* extension) provide live previews.
    4.  Run `python tools/render_arch_doc.py` to see the changes in the final HTML.

### 5.2. Auto-Generated Diagram (code2flow & Graphviz)

The **Code-Level Flowchart** is generated automatically by analyzing the Python source code.

*   **What it is:** The flowchart is a call graph that shows which functions and methods call each other. The graph's structure is defined using the **DOT language**, a plain text graph description language that is part of the [Graphviz](https://graphviz.org/) ecosystem.
*   **How to reproduce/update:**
    1.  The DOT graph definition inside the ` ```dot ... ``` ` block is generated by the [code2flow](https://github.com/scottrogowski/code2flow) Python package.
    2.  To regenerate the DOT code after significant changes to the `src` directory, you can run the following command:
        ```bash
        code2flow src/main.py src/parsers/tsv_parser.py src/extractors/relationship_extractor.py src/analyzers/base.py --output docs/project_flow.gv
        ```
    3.  Copy the contents of the generated `docs/project_flow.gv` file and paste it inside the ` ```dot ... ``` ` block in this file.
    4.  Run `python tools/render_arch_doc.py` to update the final HTML.

### 5.3. Final HTML Rendering Process

The `tools/render_arch_doc.py` script performs the following steps to create `docs/ARCHITECTURE.html`:

1.  **Reads `ARCHITECTURE.md`:** The script starts by reading the raw Markdown content of this file.

2.  **Renders the DOT Graph:**
    *   It finds the `dot` code block.
    *   To avoid requiring a local installation of Graphviz, the script sends the DOT code to the `https://quickchart.io/graphviz` web service.
    *   The service returns a Scalable Vector Graphic (SVG) of the flowchart, which is saved as `docs/project_flow.svg`.
    *   The script then replaces the ` ```dot ... ``` ` block in the Markdown with an `<img>` tag pointing to the new SVG file.

3.  **Renders Mermaid Diagrams:**
    *   The script uses the `markdown` library with the `markdown-mermaid` extension. This wraps the Mermaid code blocks in the necessary HTML tags.

4.  **Assembles the Final HTML:**
    *   The script converts the modified Markdown to an HTML body.
    *   It then wraps this body in a complete HTML structure and injects the **Mermaid.js** library from a CDN, which allows the browser to render the Mermaid diagrams.

### 5.4. How to Regenerate the Full HTML Document

If you make any changes to this `ARCHITECTURE.md` file, run the following command from the project root to regenerate the final HTML document:

```bash
python tools/render_arch_doc.py
```

This will update `docs/ARCHITECTURE.html` with all the latest content and diagrams.
