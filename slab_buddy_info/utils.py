class Utils:
    def display_slabinfo(self, slab_data):
        """Display slab allocator information.

        Args:
            slab_data (list): List of dictionaries containing slab information.

        Linux slabinfo example:
        # name            <active_objs> <num_objs> <objsize> <objperslab> <pagesperslab> : tunables <limit> <batchcount> <sharedfactor> : slabdata <active_slabs> <num_slabs> <sharedavail>
        ufs_inode_cache        0      0    808   20    4 : tunables    0    0    0 : slabdata      0      0      0
        qnx4_inode_cache       0      0    680   24    4 : tunables    0    0    0 : slabdata      0      0      0
        """
        header = "{:<20} {:>12} {:>10} {:>8} {:>12} {:>14} {:>10} {:>12} {:>14} {:>14} {:>14} {:>12}"
        print(
            header.format(
                "Name",
                "ActiveObjs",
                "NumObjs",
                "ObjSize",
                "ObjPerSlab",
                "PagesPerSlab",
                "Limit",
                "BatchCount",
                "SharedFactor",
                "ActiveSlabs",
                "NumSlabs",
                "SharedAvail",
            )
        )
        for slab in slab_data:
            row = "{:<20} {:>12} {:>10} {:>8} {:>12} {:>14} {:>10} {:>12} {:>14} {:>14} {:>14} {:>12}"
            print(
                row.format(
                    slab["name"],
                    slab["active_objs"],
                    slab["num_objs"],
                    slab["objsize"],
                    slab["objperslab"],
                    slab["pagesperslab"],
                    slab["limit"] if slab["limit"] is not None else "",
                    slab["batchcount"] if slab["batchcount"] is not None else "",
                    slab["sharedfactor"] if slab["sharedfactor"] is not None else "",
                    slab["active_slabs"] if slab["active_slabs"] is not None else "",
                    slab["num_slabs"] if slab["num_slabs"] is not None else "",
                    slab["sharedavail"] if slab["sharedavail"] is not None else "",
                )
            )

    def display_buddyinfo(self, buddy_data):
        """Display buddy allocator information.

        Args:
            buddy_data (list): List of dictionaries containing buddy information.
        """
        for entry in buddy_data:
            print(f"Node {entry['node']}, Zone {entry['zone']}:")
            print("Order | Free Blocks")
            for order, count in enumerate(entry["free_counts"]):
                print(f"{order:>5} | {count}")
            print()

    def text_bar_graph(self, labels, values, max_width=50):
        """Display a simple text-based bar graph.

        Args:
            labels (list): List of labels for the x-axis.
            values (list): List of values corresponding to each label.
            max_width (int): Maximum width of the bar graph in characters.
        """
        max_value = max(values) if max(values) > 0 else 1
        for label, value in zip(labels, values):
            bar_length = int((value / max_value) * max_width)
            bar = "#" * bar_length
            print(f"{label:<20} | {bar} ({value})")

    def generate_time_series_graph(self, data, filename="slab_buddy_graph", top_n=10):
        """Generate time-series graphs for slab usage and save as an HTML file.

        Args:
            data (dict): Dictionary containing timestamps and slab usage data.
            filename (str): Base filename to save the HTML file.
            top_n (int): Number of top slabs to include in the graph.
        """
        timestamps = data["timestamps"]
        slab_usage = data["slab_usage"]

        # Limit to top N slabs based on maximum usage
        top_slabs = sorted(
            slab_usage.items(), key=lambda item: max(item[1]), reverse=True
        )[:top_n]
        slab_names = [name for name, _ in top_slabs]

        # Prepare data for JavaScript
        js_data = []
        for name in slab_names:
            usage_list = slab_usage[name]
            js_data.append({"name": name, "data": usage_list})

        # Generate HTML content
        html_content = self.generate_html_time_series_graph(
            timestamps, js_data, title="Slab Usage Over Time"
        )

        # Save to file
        full_filename = f"{filename}.html"
        with open(full_filename, "w") as f:
            f.write(html_content)

    def generate_html_time_series_graph(self, timestamps, js_data, title):
        # Escape double quotes in slab names
        for item in js_data:
            item["name"] = item["name"].replace('"', '\\"')

        html = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>{title}</title>
            <style>
                body {{ font-family: Arial, sans-serif; }}
                .chart-container {{
                    width: 1000px;
                    height: 600px;
                    position: relative;
                }}
                .legend {{
                    margin-top: 10px;
                }}
                .legend-item {{
                    display: inline-block;
                    margin-right: 15px;
                }}
                .legend-color {{
                    display: inline-block;
                    width: 12px;
                    height: 12px;
                    margin-right: 5px;
                    vertical-align: middle;
                }}
            </style>
        </head>
        <body>
            <h2>{title}</h2>
            <div>
                Select Slabs:
                <select id="slabSelect" multiple size="10" onchange="updateChart()">
                    {"".join([f'<option value="{item["name"]}" selected>{item["name"]}</option>' for item in js_data])}
                </select>
            </div>
            <div class="chart-container">
                <canvas id="chartCanvas" width="1000" height="600"></canvas>
            </div>
            <div class="legend" id="legend"></div>
            <script>
                const timestamps = {timestamps};
                const slabData = {js_data};
                const canvas = document.getElementById('chartCanvas');
                const ctx = canvas.getContext('2d');

                function getColor(index) {{
                    const colors = ["red", "green", "blue", "orange", "purple", "cyan", "magenta", "yellow", "black", "gray"];
                    return colors[index % colors.length];
                }}

                function drawAxes(maxUsage) {{
                    const padding = 90;
                    ctx.strokeStyle = "#000";
                    ctx.lineWidth = 1;
                    // Y axis
                    ctx.beginPath();
                    ctx.moveTo(padding, padding);
                    ctx.lineTo(padding, canvas.height - padding);
                    ctx.stroke();
                    // X axis
                    ctx.beginPath();
                    ctx.moveTo(padding, canvas.height - padding);
                    ctx.lineTo(canvas.width - padding, canvas.height - padding);
                    ctx.stroke();

                    // Y axis labels and grid lines
                    ctx.fillStyle = "#000";
                    ctx.textAlign = "right";
                    ctx.textBaseline = "middle";
                    const ySteps = 10;
                    for(let i = 0; i <= ySteps; i++) {{
                        let y = padding + (canvas.height - 2 * padding) * i / ySteps;
                        let value = maxUsage * (1 - i / ySteps);
                        ctx.beginPath();
                        ctx.moveTo(padding - 5, y);
                        ctx.lineTo(padding, y);
                        ctx.stroke();
                        ctx.fillText(value.toFixed(0), padding - 15, y); // Adjust label position
                        // Grid line
                        ctx.strokeStyle = "#e0e0e0";
                        ctx.beginPath();
                        ctx.moveTo(padding, y);
                        ctx.lineTo(canvas.width - padding, y);
                        ctx.stroke();
                        ctx.strokeStyle = "#000";
                    }}

                    // X axis labels and grid lines
                    ctx.textAlign = "center";
                    ctx.textBaseline = "top";
                    const xSteps = timestamps.length - 1;
                    for(let i = 0; i <= xSteps; i++) {{
                        let x = padding + (canvas.width - 2 * padding) * i / xSteps;
                        if (i % Math.ceil(xSteps / 10) === 0 || i === xSteps) {{
                            ctx.beginPath();
                            ctx.moveTo(x, canvas.height - padding);
                            ctx.lineTo(x, canvas.height - padding + 5);
                            ctx.stroke();
                            ctx.fillText(timestamps[i], x, canvas.height - padding + 5);
                        }}
                        // Grid line
                        ctx.strokeStyle = "#e0e0e0";
                        ctx.beginPath();
                        ctx.moveTo(x, padding);
                        ctx.lineTo(x, canvas.height - padding);
                        ctx.stroke();
                        ctx.strokeStyle = "#000";
                    }}

                    // Axis labels
                    ctx.fillStyle = "#000";
                    ctx.textAlign = "center";
                    ctx.textBaseline = "bottom";
                    ctx.fillText("Time", canvas.width / 2, canvas.height - 5);
                    ctx.save();
                    ctx.translate(padding - 70, canvas.height / 2); // Adjust label position
                    ctx.rotate(-Math.PI / 2);
                    ctx.fillText("Memory Usage (Bytes)", 0, 0);
                    ctx.restore();
                }}

                function drawLine(data, color, maxUsage) {{
                    const padding = 90;
                    ctx.beginPath();
                    ctx.strokeStyle = color;
                    for(let i = 0; i < data.length; i++) {{
                        let x = padding + (canvas.width - 2 * padding) * i / (data.length -1);
                        let y = padding + (canvas.height - 2 * padding) * (1 - data[i] / maxUsage);
                        if(i === 0) {{
                            ctx.moveTo(x, y);
                        }} else {{
                            ctx.lineTo(x, y);
                        }}
                    }}
                    ctx.stroke();
                }}

                function drawChart() {{
                    ctx.clearRect(0, 0, canvas.width, canvas.height);
                    const selectedOptions = Array.from(document.getElementById('slabSelect').selectedOptions);
                    const selectedNames = selectedOptions.map(option => option.value);
                    let maxUsage = 0;
                    for(let slab of slabData) {{
                        if(selectedNames.includes(slab.name)) {{
                            maxUsage = Math.max(maxUsage, ...slab.data, maxUsage);
                        }}
                    }}
                    if(maxUsage === 0) maxUsage = 1; // Avoid division by zero
                    else maxUsage *= 1.1;            // Add some padding

                    drawAxes(maxUsage);

                    let colorIndex = 0;
                    const legend = document.getElementById('legend');
                    legend.innerHTML = '';
                    for(let slab of slabData) {{
                        if(selectedNames.includes(slab.name)) {{
                            let color = getColor(colorIndex);
                            drawLine(slab.data, color, maxUsage);
                            // Add legend item
                            let legendItem = document.createElement('div');
                            legendItem.className = 'legend-item';
                            legendItem.innerHTML = `<div class='legend-color' style='background-color:${{color}};'></div>${{slab.name}}`;
                            legend.appendChild(legendItem);
                            colorIndex++;
                        }}
                    }}
                }}

                function updateChart() {{
                    drawChart();
                }}

                // Initial draw
                // Default to showing all slabs
                window.onload = function() {{
                    const slabSelect = document.getElementById('slabSelect');
                    for(let i = 0; i < slabSelect.options.length; i++) {{
                        slabSelect.options[i].selected = true;
                    }}
                    updateChart();
                }};
            </script>
        </body>
        </html>
        """
        return html

    def prepare_buddy_graph_data(self, buddy_data):
        """Prepare data for buddy allocator graph.

        Args:
            buddy_data (list): List of dictionaries containing buddy information.

        Returns:
            tuple: A tuple containing labels and values for the graph.
        """
        labels = []
        values = []
        for entry in buddy_data:
            node_zone = f"Node {entry['node']} Zone {entry['zone']}"
            for order, count in enumerate(entry["free_counts"]):
                labels.append(f"{node_zone} Order {order}")
                values.append(count)
        return labels, values

    def generate_html_bar_graph(self, labels, values, title="Graph"):
        """Generate an HTML page with an inline SVG bar graph.

        Args:
            labels (list): List of labels for the x-axis.
            values (list): List of values corresponding to each label.
            title (str): Title of the graph.

        Returns:
            str: HTML content as a string.
        """
        max_value = max(values) if max(values) > 0 else 1
        width = 800
        bar_height = 20
        bar_spacing = 5
        total_height = (bar_height + bar_spacing) * len(values) + 50

        svg_bars = ""
        for i, (label, value) in enumerate(zip(labels, values)):
            bar_length = int((value / max_value) * width)
            y_position = 50 + i * (bar_height + bar_spacing)
            svg_bars += f"""
            <rect x="0" y="{y_position}" width="{bar_length}" height="{bar_height}" fill="steelblue"></rect>
            <text x="{bar_length + 5}" y="{y_position + bar_height / 2 + 5}" font-size="12">{label} ({value})</text>
            """

        html_content = f"""
        <!DOCTYPE html>
        <html>
        <head>
            <title>{title}</title>
        </head>
        <body>
            <h2>{title}</h2>
            <svg width="{width + 200}" height="{total_height}">
                {svg_bars}
            </svg>
        </body>
        </html>
        """
        return html_content

    def display_html_in_terminal(self, html_content):
        """Display a message indicating that HTML output cannot be shown in the terminal.

        Args:
            html_content (str): HTML content (unused in this method).
        """
        print("HTML output cannot be displayed in the terminal.")
        print("Please save the output to a file using the '--save' option.")
