/**
 * crawl-server.js
 * A plain-text link graph server that mimics https://langa.pl/crawl/
 * Compatible with the httpx async crawler script.
 *
 * Usage:
 *   node crawl-server.js
 *
 * Then run the crawler against it:
 *   prefix = 'http://localhost:3000/crawl/'
 */

const http = require("http");

const HOST = "localhost";
const PORT = 3000;
const BASE = `http://${HOST}:${PORT}`;

/**
 * The link graph.
 * Keys are URL paths, values are arrays of child paths.
 * The server will serve each node as plain text, one URL per line.
 *
 *           /crawl/
 *          /       \
 *       /a/         /b/
 *      /   \           \
 *   /a/1/  /a/2/       /b/1/
 *              \
 *           /a/2/deep/    <-- dead end (no children)
 */
// Delay config (milliseconds) — simulates natural network/processing latency
const DELAY = {
  min: 300,   // fastest a node will respond
  max: 1200,  // slowest a node will respond
};

const sleep = (ms) => new Promise((resolve) => setTimeout(resolve, ms));

const naturalDelay = () =>
  sleep(Math.floor(Math.random() * (DELAY.max - DELAY.min + 1)) + DELAY.min);

const GRAPH = {
  // Root
  "/crawl/": ["/crawl/a/", "/crawl/b/", "/crawl/c/", "/crawl/d/"],
 
  // Branch A
  "/crawl/a/":       ["/crawl/a/1/", "/crawl/a/2/", "/crawl/a/3/"],
  "/crawl/a/1/":     ["/crawl/a/1/x1/", "/crawl/a/1/x2/"],
  "/crawl/a/1/x1/":  [],
  "/crawl/a/1/x2/":  [],
  "/crawl/a/2/":     ["/crawl/a/2/x1/", "/crawl/a/2/x2/"],
  "/crawl/a/2/x1/":  [],
  "/crawl/a/2/x2/":  [],
  "/crawl/a/3/":     [],
 
  // Branch B
  "/crawl/b/":       ["/crawl/b/1/", "/crawl/b/2/", "/crawl/b/3/"],
  "/crawl/b/1/":     ["/crawl/b/1/x1/", "/crawl/b/1/x2/", "/crawl/b/1/x3/"],
  "/crawl/b/1/x1/":  [],
  "/crawl/b/1/x2/":  [],
  "/crawl/b/1/x3/":  [],
  "/crawl/b/2/":     [],
  "/crawl/b/3/":     ["/crawl/b/3/x1/", "/crawl/b/3/x2/"],
  "/crawl/b/3/x1/":  [],
  "/crawl/b/3/x2/":  [],
 
  // Branch C
  "/crawl/c/":       ["/crawl/c/1/", "/crawl/c/2/", "/crawl/c/3/"],
  "/crawl/c/1/":     [],
  "/crawl/c/2/":     ["/crawl/c/2/x1/"],
  "/crawl/c/2/x1/":  ["/crawl/c/2/x1/omega/"],
  "/crawl/c/2/x1/omega/": [],
  "/crawl/c/3/":     ["/crawl/c/3/x1/", "/crawl/c/3/x2/", "/crawl/c/3/x3/"],
  "/crawl/c/3/x1/":  [],
  "/crawl/c/3/x2/":  [],
  "/crawl/c/3/x3/":  [],
 
  // Branch D
  "/crawl/d/":       ["/crawl/d/1/", "/crawl/d/2/", "/crawl/d/3/"],
  "/crawl/d/1/":     ["/crawl/d/1/x1/", "/crawl/d/1/x2/"],
  "/crawl/d/1/x1/":  [],
  "/crawl/d/1/x2/":  [],
  "/crawl/d/2/":     ["/crawl/d/2/x1/", "/crawl/d/2/x2/", "/crawl/d/2/x3/"],
  "/crawl/d/2/x1/":  [],
  "/crawl/d/2/x2/":  [],
  "/crawl/d/2/x3/":  [],
  "/crawl/d/3/":     [],
};

const server = http.createServer(async (req, res) => {
  const path = req.url;

  // Only handle paths in our graph
  if (!(path in GRAPH)) {
    res.writeHead(404, { "Content-Type": "text/plain" });
    res.end(`404 Not Found: ${path}\n`);
    return;
  }

  // Simulate natural fetch latency before responding
  const delay = Math.floor(Math.random() * (DELAY.max - DELAY.min + 1)) + DELAY.min;
  console.log(`[waiting] ${path} — delaying ${delay}ms`);
  await naturalDelay();

  const children = GRAPH[path];

  // Respond with one full URL per line (same format as langa.pl/crawl/)
  const body = children.map((p) => `${BASE}${p}`).join("\n");

  res.writeHead(200, { "Content-Type": "text/plain" });
  res.end(body ? body + "\n" : "");

  console.log(`[served] ${path} → [${children.length} links]`);
});

server.listen(PORT, HOST, () => {
  console.log(`\n🕷️  Crawl maze server running at ${BASE}/crawl/\n`);
  console.log(`Delay: ${DELAY.min}ms – ${DELAY.max}ms (random per request)\n`);
  console.log("Graph structure:");
  for (const [node, children] of Object.entries(GRAPH)) {
    const label = children.length ? children.join(", ") : "(dead end)";
    console.log(`  ${node.padEnd(25)} → ${label}`);
  }
  console.log("\nPoint your crawler at:");
  console.log(`  prefix = '${BASE}/crawl/'\n`);
});