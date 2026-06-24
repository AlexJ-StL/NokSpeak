import { Server } from "@modelcontextprotocol/sdk/server/index.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { CallToolRequestSchema, ListToolsRequestSchema } from "@modelcontextprotocol/sdk/types.js";
import { z } from "zod";

// Initialize the formal Model Context Protocol Server
const server = new Server(
  {
    name: "nokspeak-validator",
    version: "2.1.0",
  },
  {
    capabilities: {
      tools: {},
    },
  }
);

// Define valid tokens for strict v2.1 matching
const VALID_PRONOUNS = ["sesh", "par", "wei", "rek"];
const VALID_EPISTEMICS = ["savref", "savraz", "savtren", "savfuz"];
const VALID_CONTEXTS = ["nok", "fok", "exo"];
const VALID_OPERATORS = ["++", "--", "~", "~~"];
const VALID_NODES = [":mi", ":ai", ":sys", ":usr"];

// Strict Regular Expression matching the token sequence:
// [Optional Version Prefix]Marker[Operator][Optional Node Suffix]
const NOK_REGEX = /^(?:nok(\d+\.\d+):)?([a-z]{3,7})(\+\+|--|~~|~)(:[a-z]{2,3})?$/;

/**
 * Validates and structurally breaks down an isolated token payload
 */
function analyzeToken(token: string) {
  const cleanToken = token.trim();
  const match = cleanToken.match(NOK_REGEX);

  if (!match) {
    return { isValid: false, error: "Token format mismatch. Must follow: [nokX.Y:]Marker[Operator][Node]" };
  }

  const [_, version, baseMarker, operator, nodeSuffix] = match;

  // Determine token category allocation
  let category = "unknown";
  if (VALID_PRONOUNS.includes(baseMarker)) category = "pronoun";
  else if (VALID_EPISTEMICS.includes(baseMarker)) category = "epistemic";
  else if (VALID_CONTEXTS.includes(baseMarker)) category = "context";

  if (category === "unknown") {
    return { isValid: false, error: `Unknown core marker context: '${baseMarker}'` };
  }

  if (nodeSuffix && !VALID_NODES.includes(nodeSuffix)) {
    return { isValid: false, error: `Invalid routing header suffix node target: '${nodeSuffix}'` };
  }

  return {
    isValid: true,
    component: {
      marker: baseMarker,
      category: category,
      operator: operator,
      node: nodeSuffix || ":mi", // Default local node context
      version: version || "n/a"
    }
  };
}

// Register Tool Manifests
server.setRequestHandler(ListToolsRequestSchema, async () => {
  return {
    tools: [
      {
        name: "validate_nok_expression",
        description: "Checks and parses an isolated single NokSpeak v2.1 syntax expression block.",
        inputSchema: {
          type: "object",
          properties: {
            expression: { type: "string", description: "The token sequence to test (e.g., 'savref++:sys')" }
          },
          required: ["expression"]
        }
      },
      {
        name: "parse_text_blocks",
        description: "Scans strings to isolate and extract embedded/trailing NokSpeak metadata markers.",
        inputSchema: {
          type: "object",
          properties: {
            text: { type: "string", description: "The raw natural language response context to parse." }
          },
          required: ["text"]
        }
      }
    ]
  };
});

// Implement Tool Logic Verification Loop
server.setRequestHandler(CallToolRequestSchema, async (request) => {
  const { name, arguments: args } = request.params;

  try {
    if (name === "validate_nok_expression") {
      const { expression } = z.object({ expression: z.string() }).parse(args);
      const analysis = analyzeToken(expression);

      return {
        content: [{ type: "text", text: JSON.stringify(analysis, null, 2) }],
        isError: !analysis.isValid
      };
    } 
    
    if (name === "parse_text_blocks") {
      const { text } = z.object({ text: z.string() }).parse(args);
      
      // Look for explicit code-blocked or inline space-delimited markers.
      // Word-boundary anchoring prevents false positives inside URLs, identifiers,
      // or other non-token text containing operator-like character sequences.
      const wordPattern = /(?:^|[\s.,;:!?()\[\]"'])(`?)([a-z]{3,7}(?:\+\+|--|~~|~)(?::[a-z]{2,3})?)(`?)(?=$|[\s.,;:!?()\[\]"'])/gi;
      const discoveredMatches = text.match(wordPattern) || [];
      
      const extractions = discoveredMatches.map(match => {
        const structuralToken = match.replace(/`/g, "");
        return {
          raw: match,
          analysis: analyzeToken(structuralToken)
        };
      });

      return {
        content: [{ type: "text", text: JSON.stringify({ totalCount: extractions.length, extractions }, null, 2) }]
      };
    }

    throw new Error(`Execution error: Tool '${name}' not supported by this server instance.`);
  } catch (error: any) {
    return {
      content: [{ type: "text", text: JSON.stringify({ error: error.message }) }],
      isError: true
    };
  }
});

// Fire up transport layer over system IO lines
async function runServer() {
  const transport = new StdioServerTransport();
  await server.connect(transport);
  console.error("NokSpeak v2.1 Validation Matrix running over STDIO channels.");
}

runServer().catch((err) => {
  console.error("Fatal failure launching MCP infrastructure:", err);
  process.exit(1);
});