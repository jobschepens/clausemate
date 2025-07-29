#!/usr/bin/env python3
"""Improved Cross-Chapter Coreference Network Visualization.

This script analyzes the unified relationships data to create a more meaningful
cross-chapter network that shows actual relationships between chapters based on
coreference chains that span multiple chapters.
"""

import csv
import json
import os
from collections import defaultdict
from datetime import datetime


def analyze_cross_chapter_relationships(relationships_file, cross_chapter_chains_file):
    """Analyze the relationships data to extract meaningful cross-chapter connections."""
    print("🔍 Analyzing cross-chapter relationships...")

    # Load cross-chapter chains
    with open(cross_chapter_chains_file, encoding="utf-8") as f:
        cross_chapter_chains = json.load(f)

    # Data structures to track relationships
    chapter_connections = defaultdict(
        lambda: defaultdict(int)
    )  # chapter_a -> chapter_b -> count
    chain_chapter_mapping = defaultdict(set)  # chain_id -> set of chapters
    chapter_entities = defaultdict(set)  # chapter -> set of entities

    # Read relationships CSV
    print("📖 Reading relationships data...")
    with open(relationships_file, encoding="utf-8") as f:
        reader = csv.DictReader(f)

        for row in reader:
            chapter_num = int(row["chapter_number"])
            coref_id = row.get("pronoun_coref_ids", "").strip("[]'\"")

            if coref_id and coref_id != "*":
                # Extract base coref ID (remove occurrence numbers)
                base_coref_id = coref_id.split("-")[0] if "-" in coref_id else coref_id

                # Track which chapters this coreference chain appears in
                chain_chapter_mapping[base_coref_id].add(chapter_num)

                # Track entities per chapter
                pronoun_text = row.get("pronoun_text", "")
                if pronoun_text:
                    chapter_entities[chapter_num].add(pronoun_text)

    print(f"📊 Found {len(chain_chapter_mapping)} coreference chains")

    # Identify truly cross-chapter chains
    true_cross_chapter_chains = {}
    for chain_id, chapters in chain_chapter_mapping.items():
        if len(chapters) > 1:  # Appears in multiple chapters
            true_cross_chapter_chains[chain_id] = sorted(chapters)

            # Count connections between chapters
            chapters_list = sorted(chapters)
            for i, ch1 in enumerate(chapters_list):
                for ch2 in chapters_list[i + 1 :]:
                    chapter_connections[ch1][ch2] += 1
                    chapter_connections[ch2][ch1] += 1  # Bidirectional

    print(f"✅ Found {len(true_cross_chapter_chains)} true cross-chapter chains")

    # Create chapter statistics
    chapter_stats = {}
    for chapter in range(1, 5):  # Assuming 4 chapters
        chapter_stats[chapter] = {
            "total_entities": len(chapter_entities[chapter]),
            "cross_chapter_chains": sum(
                1 for chains in true_cross_chapter_chains.values() if chapter in chains
            ),
            "connections": dict(chapter_connections[chapter]),
        }

    return {
        "true_cross_chapter_chains": true_cross_chapter_chains,
        "chapter_connections": dict(chapter_connections),
        "chapter_stats": chapter_stats,
        "total_cross_chapter_chains": len(true_cross_chapter_chains),
    }


def create_improved_visualization(analysis_data, cross_chapter_chains, output_file):
    """Create an improved HTML visualization showing actual cross-chapter relationships."""
    print("🎨 Creating improved visualization...")

    # Calculate connection strengths for edge weights
    max_connections = 0
    for ch1_connections in analysis_data["chapter_connections"].values():
        for count in ch1_connections.values():
            max_connections = max(max_connections, count)

    # Create nodes (chapters)
    chapter_colors = {
        1: "#FF6B6B",  # Red
        2: "#4ECDC4",  # Teal
        3: "#45B7D1",  # Blue
        4: "#96CEB4",  # Green
    }

    nodes = []
    for chapter in range(1, 5):
        stats = analysis_data["chapter_stats"][chapter]
        nodes.append(
            {
                "id": f"chapter_{chapter}",
                "label": f"Chapter {chapter}",
                "group": "chapter",
                "color": chapter_colors[chapter],
                "size": 30
                + stats["cross_chapter_chains"]
                * 2,  # Size based on cross-chapter involvement
                "font": {"size": 16, "color": "white"},
                "title": f"Chapter {chapter}<br/>Cross-chapter chains: {stats['cross_chapter_chains']}<br/>Total entities: {stats['total_entities']}",
            }
        )

    # Create edges (connections between chapters)
    edges = []
    edge_id = 0
    for ch1, connections in analysis_data["chapter_connections"].items():
        for ch2, count in connections.items():
            if ch1 < ch2:  # Avoid duplicate edges
                # Calculate edge weight (thickness) based on connection strength
                weight = (
                    max(1, min(10, (count / max_connections) * 10))
                    if max_connections > 0
                    else 1
                )

                edges.append(
                    {
                        "id": edge_id,
                        "from": f"chapter_{ch1}",
                        "to": f"chapter_{ch2}",
                        "width": weight,
                        "color": {"color": "#666666", "opacity": 0.7},
                        "title": f"{count} shared coreference chains",
                        "label": str(count)
                        if count > 5
                        else "",  # Show label for strong connections
                    }
                )
                edge_id += 1

    # Create the HTML content
    html_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Improved Cross-Chapter Coreference Network</title>
    <script src="https://unpkg.com/vis-network/standalone/umd/vis-network.min.js"></script>
    <link href="https://unpkg.com/vis-network/styles/vis-network.css" rel="stylesheet" type="text/css" />
    <style>
        body {{ font-family: Arial, sans-serif; margin: 20px; background-color: #f5f5f5; }}
        .container {{ max-width: 1200px; margin: 0 auto; background: white; padding: 20px; border-radius: 8px; box-shadow: 0 2px 10px rgba(0,0,0,0.1); }}
        .header {{ text-align: center; margin-bottom: 30px; }}
        .network-container {{ height: 600px; border: 1px solid #ddd; margin: 20px 0; }}
        .stats-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 20px; margin: 20px 0; }}
        .stat-card {{ background: #f8f9fa; padding: 15px; border-radius: 5px; border-left: 4px solid #007bff; }}
        .stat-value {{ font-size: 2em; font-weight: bold; color: #007bff; }}
        .stat-label {{ color: #666; margin-top: 5px; }}
        .controls {{ margin: 20px 0; padding: 15px; background: #e9ecef; border-radius: 5px; }}
        .btn {{ padding: 8px 16px; margin: 5px; background: #007bff; color: white; border: none; border-radius: 4px; cursor: pointer; }}
        .btn:hover {{ background: #0056b3; }}
        .legend {{ display: flex; flex-wrap: wrap; gap: 15px; margin: 15px 0; }}
        .legend-item {{ display: flex; align-items: center; }}
        .legend-color {{ width: 20px; height: 20px; border-radius: 50%; margin-right: 8px; }}
        .analysis-section {{ margin: 20px 0; padding: 15px; background: #f8f9fa; border-radius: 5px; }}
        table {{ width: 100%; border-collapse: collapse; margin: 15px 0; }}
        th, td {{ padding: 8px 12px; text-align: left; border-bottom: 1px solid #ddd; }}
        th {{ background-color: #f8f9fa; font-weight: bold; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>Improved Cross-Chapter Coreference Network</h1>
            <p>Interactive visualization showing actual coreference relationships between chapters</p>
            <p>Generated: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}</p>
        </div>

        <div class="stats-grid">
            <div class="stat-card">
                <div class="stat-value">4</div>
                <div class="stat-label">Total Chapters</div>
            </div>
            <div class="stat-card">
                <div class="stat-value">{analysis_data["total_cross_chapter_chains"]}</div>
                <div class="stat-label">True Cross-Chapter Chains</div>
            </div>
            <div class="stat-card">
                <div class="stat-value">{len(edges)}</div>
                <div class="stat-label">Chapter Connections</div>
            </div>
            <div class="stat-card">
                <div class="stat-value">{sum(sum(connections.values()) for connections in analysis_data["chapter_connections"].values()) // 2}</div>
                <div class="stat-label">Total Shared References</div>
            </div>
        </div>

        <div class="legend">
            <div class="legend-item">
                <div class="legend-color" style="background-color: #FF6B6B;"></div>
                <span>Chapter 1</span>
            </div>
            <div class="legend-item">
                <div class="legend-color" style="background-color: #4ECDC4;"></div>
                <span>Chapter 2</span>
            </div>
            <div class="legend-item">
                <div class="legend-color" style="background-color: #45B7D1;"></div>
                <span>Chapter 3</span>
            </div>
            <div class="legend-item">
                <div class="legend-color" style="background-color: #96CEB4;"></div>
                <span>Chapter 4</span>
            </div>
        </div>

        <div class="controls">
            <button class="btn" onclick="fitNetwork()">Fit to Screen</button>
            <button class="btn" onclick="togglePhysics()">Toggle Physics</button>
            <button class="btn" onclick="showConnectionMatrix()">Show Connection Matrix</button>
        </div>

        <div id="network" class="network-container"></div>

        <div class="analysis-section">
            <h3>Chapter Connection Analysis</h3>
            <table id="connection-matrix">
                <thead>
                    <tr>
                        <th>From/To</th>
                        <th>Chapter 1</th>
                        <th>Chapter 2</th>
                        <th>Chapter 3</th>
                        <th>Chapter 4</th>
                    </tr>
                </thead>
                <tbody>
"""

    # Add connection matrix
    for ch1 in range(1, 5):
        html_content += f"                    <tr><th>Chapter {ch1}</th>"
        for ch2 in range(1, 5):
            if ch1 == ch2:
                html_content += "<td>-</td>"
            else:
                count = analysis_data["chapter_connections"].get(ch1, {}).get(ch2, 0)
                html_content += f"<td>{count}</td>"
        html_content += "</tr>\n"

    html_content += f"""
                </tbody>
            </table>
            <p><strong>Note:</strong> Numbers represent the count of coreference chains shared between chapters.
            Thicker lines in the network indicate stronger connections.</p>
        </div>
    </div>

    <script>
        const nodes = new vis.DataSet({json.dumps(nodes)});
        const edges = new vis.DataSet({json.dumps(edges)});
        const data = {{ nodes: nodes, edges: edges }};

        const options = {{
            nodes: {{
                shape: 'dot',
                scaling: {{
                    min: 20,
                    max: 50
                }},
                font: {{
                    size: 16,
                    face: 'Arial'
                }}
            }},
            edges: {{
                color: {{ inherit: 'from' }},
                smooth: {{
                    type: 'continuous'
                }},
                arrows: {{
                    to: {{ enabled: false }}
                }}
            }},
            physics: {{
                stabilization: {{ iterations: 150 }},
                barnesHut: {{
                    gravitationalConstant: -2000,
                    springConstant: 0.04,
                    springLength: 200
                }}
            }},
            interaction: {{
                hover: true,
                tooltipDelay: 200
            }}
        }};

        const container = document.getElementById('network');
        const network = new vis.Network(container, data, options);

        let physicsEnabled = true;

        function fitNetwork() {{
            network.fit();
        }}

        function togglePhysics() {{
            physicsEnabled = !physicsEnabled;
            network.setOptions({{ physics: {{ enabled: physicsEnabled }} }});
        }}

        function showConnectionMatrix() {{
            document.getElementById('connection-matrix').scrollIntoView({{ behavior: 'smooth' }});
        }}

        // Add click event for detailed information
        network.on('click', function(params) {{
            if (params.nodes.length > 0) {{
                const nodeId = params.nodes[0];
                const chapterNum = nodeId.replace('chapter_', '');
                const stats = {json.dumps(analysis_data["chapter_stats"])};

                alert(`Chapter ${{chapterNum}} Details:\\n` +
                      `Cross-chapter chains: ${{stats[chapterNum].cross_chapter_chains}}\\n` +
                      `Total entities: ${{stats[chapterNum].total_entities}}\\n` +
                      `Connections: ${{Object.keys(stats[chapterNum].connections).length}} other chapters`);
            }}
        }});
    </script>
</body>
</html>
"""

    # Write the HTML file
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    with open(output_file, "w", encoding="utf-8") as f:
        f.write(html_content)

    print(f"✅ Improved visualization saved to: {output_file}")


def main():
    """Main function to create improved cross-chapter visualization."""
    # File paths
    relationships_file = (
        "data/output/unified_analysis_20250729_123353/unified_relationships.csv"
    )
    cross_chapter_chains_file = (
        "data/output/unified_analysis_20250729_123353/cross_chapter_chains.json"
    )
    output_file = "data/output/test_visualization/improved_cross_chapter_network.html"

    print("🚀 Creating improved cross-chapter coreference network visualization...")

    # Check if files exist
    if not os.path.exists(relationships_file):
        print(f"❌ Relationships file not found: {relationships_file}")
        return

    if not os.path.exists(cross_chapter_chains_file):
        print(f"❌ Cross-chapter chains file not found: {cross_chapter_chains_file}")
        return

    # Load cross-chapter chains
    with open(cross_chapter_chains_file, encoding="utf-8") as f:
        cross_chapter_chains = json.load(f)

    # Analyze relationships
    analysis_data = analyze_cross_chapter_relationships(
        relationships_file, cross_chapter_chains_file
    )

    # Create improved visualization
    create_improved_visualization(analysis_data, cross_chapter_chains, output_file)

    print("🎉 Improved cross-chapter network visualization completed successfully!")
    print("📊 Analysis Summary:")
    print(
        f"   - True cross-chapter chains: {analysis_data['total_cross_chapter_chains']}"
    )
    print(
        f"   - Chapter connections: {len([1 for ch_conn in analysis_data['chapter_connections'].values() for _ in ch_conn])}"
    )

    for chapter, stats in analysis_data["chapter_stats"].items():
        print(
            f"   - Chapter {chapter}: {stats['cross_chapter_chains']} cross-chapter chains, {len(stats['connections'])} connections"
        )


if __name__ == "__main__":
    main()
