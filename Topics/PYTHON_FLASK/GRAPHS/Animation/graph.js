// graph.js -- Include it as a script in index.html

    // Define a visual area for animation to display.
    const svg = d3.select("#visual-area"),
          width = +svg.attr("width"),
          height = +svg.attr("height");

    // Create layer groups globally.
    const linkGroup   = svg.append("g").attr("class", "links");
    const arrowGroup  = svg.append("g").attr("class", "arrows");
    const nodeGroup   = svg.append("g").attr("class", "nodes");
    const labelGroup  = svg.append("g").attr("class", "labels");
    const edgeLabelGroup = svg.append("g").attr("class", "edge-labels");

    // Define arrow marker once.
    svg.append("defs").append("marker")
      .attr("id", "arrowhead")
      .attr("viewBox", "0 -5 10 10")
      .attr("refX", 19)   // Adjust based on node radius
      .attr("refY", 0)
      .attr("markerWidth", 6)
      .attr("markerHeight", 6)
      .attr("orient", "auto")
      .append("path")
      .attr("d", "M0,-5L10,0L0,5")
      .attr("stroke-width", 2)
      .attr("fill", "orange");

    // Define simulation globally once
   const simulation = d3.forceSimulation()
     .force("link", d3.forceLink().id(d => d.id).distance(120))
     .force("charge", d3.forceManyBody().strength(-300))
     .force("center", d3.forceCenter(width / 2, height / 2))
     .force("collide", d3.forceCollide(40));

    // Minimal addArrow function
    function addArrow(edgeSelection) {
       edgeSelection.attr("marker-end", "url(#arrowhead)");
    }


    // It draws the backend generated graph.
    async function fetchGraphAndDraw() {
      try {
        const graphResponse = await fetch("/graph");
        if (!graphResponse.ok) 
	      throw new Error("Graph fetch error: " + graphResponse.status);

        const graphData = await graphResponse.json();
        console.log("Graph data:", graphData);

        drawGraph(graphData);
      } catch (err) {
        console.error("Error fetching graph:", err);
        alert("Failed to fetch graph from backend.");
      }
    }

    let graphReady = false; // Graph is not defined yet

    document.getElementById("generateGraphBackend").onclick = async () => {
      const numNodes = parseInt(document.getElementById("numNodes").value);
      const maxConn = parseInt(document.getElementById("max_conn").value);

      try {
        const response = await fetch("/generate_graph", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ nodes: numNodes, max_conn: maxConn })
        });

        if (!response.ok) throw new Error("Backend error: " + response.status);

        await response.json(); // Backend stores graph
        await fetchGraphAndDraw();

        graphReady = true; // Mark graph as ready

        document.getElementById("numNodes").value = "";
        document.getElementById("max_conn").value = "";
      } catch (err) {
        console.error("Error generating graph:", err);
        alert("Failed to generate graph from backend.");
      }
    };

    function drawGraph(graphData) {
      // Clear old graph
      nodeGroup.selectAll("*").remove();
      linkGroup.selectAll("*").remove();

      // Draw links
      const links = linkGroup.selectAll("line")
        .data(graphData.edges)
        .enter().append("line")
        .attr("stroke", "#999");

      // Draw nodes
      const nodes = nodeGroup.selectAll(".node")
        .data(graphData.nodes)
        .enter().append("g")
        .attr("class", "node")
        .call(d3.drag()
          .on("start", dragstarted)
          .on("drag", dragged)
          .on("end", dragended));

      nodes.append("circle")
          .attr("r", 20)
          .attr("fill", "steelblue");

      // Node label
      nodes.append("text")
        .attr("class", "node-label")
        .attr("text-anchor", "middle")
        .attr("dy", ".35em")   // center vertically
        .attr("font-size", "14px")
        .attr("font-weight", "bold")
        .text(d => d.label);

      // DFS number placeholder
      nodes.append("text")
        .attr("class", "dfs-number")
        .attr("text-anchor", "middle")
        .attr("dy", "1.2em")    // below label
        .attr("font-size", "12px")
        .attr("fill", "black");

      // Bind nodes and edges to simulation
      simulation.nodes(graphData.nodes);
      simulation.force("link").links(graphData.edges);

      // Add centering and collision forces
      simulation
        .force("center", d3.forceCenter(width / 2, height / 2))
        .force("collide", d3.forceCollide(40));

      // Update positions on tick
      simulation.on("tick", () => {
        links
          .attr("x1", d => d.source.x)
          .attr("y1", d => d.source.y)
          .attr("x2", d => d.target.x)
          .attr("y2", d => d.target.y);

        nodes.attr("transform", d => {
          // Clamp positions to keep nodes inside canvas
          d.x = Math.max(30, Math.min(width - 30, d.x));
          d.y = Math.max(30, Math.min(height - 30, d.y));
          return `translate(${d.x},${d.y})`;
        });
      });

      // Restart simulation
      simulation.alpha(1).restart();

      return { nodes, links };
    }

    function dragstarted(event, d) {

      simulation.stop();
      d.fx = d.x;
      d.fy = d.y;
    }

    function dragged(event, d) {
      d.x = event.x;
      d.y = event.y;

      // Update node position directly
      d3.select(event.sourceEvent.target.parentNode)
        .attr("transform", `translate(${d.x},${d.y})`);

      // Update links
      linkGroup.selectAll("line")
        .attr("x1", l => l.source.x)
        .attr("y1", l => l.source.y)
        .attr("x2", l => l.target.x)
        .attr("y2", l => l.target.y);
    }

    function dragended(event, d) {
      d.fx = null;
      d.fy = null;
    }

   function removeArrowhead(edge) {
      svg.select(`.arrow-${edge.source.label}-${edge.target.label}`).remove();
   }



   function highlightTraversal(data, nodes, links) {
     const traversal = data.order || [];
     const tree_edges = data.tree_edges || [];

     // Reset styles
     nodes.select("circle")
       .attr("fill", "steelblue");

     // Reset labels (keep them bold and centered)
     nodes.select("text.node-label")
       .text(d => d.label)
       .attr("font-size", "14px")
       .attr("font-weight", "bold")
       .attr("dy", "-0.2em");   // slight upward shift

     // Reset DFS numbers (clear them initially)
     nodes.select("text.dfs-number")
       .text("")
       .attr("dy", "1.2em");    // keep them below the label

     links.attr("stroke", "#999")
       .attr("stroke-width", 1)
       .attr("marker-end", null);

     traversal.forEach((node, i) => {
       setTimeout(() => {
         const sel = nodes.filter(d => d.id === node.id);

         // Highlight circle
         sel.select("circle").attr("fill", "orange");

         // Show traversal number below the label
         sel.select("text.dfs-number")
            .text(i + 1)
            .attr("font-size", "14px")
            .attr("font-weight", "bold");

         // Highlight edge + arrow
         if (i > 0 && tree_edges[i - 1]) {
           const edge = tree_edges[i - 1];
           const edgeSelection = links.filter(d =>
             d.source.id === edge.parent && d.target.id === edge.child
           );
           edgeSelection.attr("stroke", "orange")
                     .attr("stroke-width", 3)
                     .attr("marker-end", "url(#arrowhead)");
         }
       }, i * 1000);
     });
   }
   


    // Run DFS function.
    document.getElementById("runDFS").onclick = async () => {
      if (!graphReady) {
        // Graph not generated yet
        alert("Please generate a graph first!");
        return;
      }
      // Default start node is "A".
      const startNode = document.getElementById("startNode").value || "A";
      const response = await fetch("/dfs", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ start: startNode.charCodeAt(0) - 65 })
      });
      const data = await response.json();
      highlightTraversal(data, nodeGroup.selectAll(".node"), 
	      linkGroup.selectAll("line"));
    };

    // Run BFS function.
    document.getElementById("runBFS").onclick = async () => {
      if (!graphReady) {
        // Backend has not generated graph yet.
        alert("Please generate a graph first!");
        return;
      }
      // Default start node is A.
      const startNode = document.getElementById("startNode").value || "A";
      const response = await fetch("/bfs", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ start: startNode.charCodeAt(0) - 65 })
      });
      const data = await response.json();
      highlightTraversal(data, nodeGroup.selectAll(".node"), 
	      linkGroup.selectAll("line"));
   };


   // You can reset graph
   document.getElementById("resetGraph").onclick = async () => {
     try {
       // Fetch the current graph again from backend
       const graphResponse = await fetch("/graph");
       if (!graphResponse.ok) 
	     throw new Error("Graph fetch error: " + graphResponse.status);

       const graphData = await graphResponse.json();
       console.log("Reset graph:", graphData);

       // Redraw graph with default colors
       drawGraph(graphData);
     } catch (err) {
       console.error("Error resetting graph:", err);
       alert("Failed to reset graph.");
     }
   };   


