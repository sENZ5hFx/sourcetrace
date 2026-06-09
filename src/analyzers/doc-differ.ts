/**
 * Doc Differ Analyzer
 *
 * Finds where documentation contradicts code.
 * Detects staleness, lies, and drift between what docs say and what code does.
 */

import type { AnalyzerOptions, AnalyzerResult, Contradiction } from "../types.js";
import type { ScannedFile } from "../utils/fs.js";

interface DocClaim {
  text: string;
  source: string;
  line: number;
  category: "algorithm" | "command" | "env-var" | "path" | "behavior" | "dependency";
}

export async function diffDocs(
  files: ScannedFile[],
  options: AnalyzerOptions
): Promise<AnalyzerResult<Contradiction[]>> {
  const startTime = Date.now();
  const contradictions: Contradiction[] = [];
  const filesRead: string[] = [];

  const docFiles = files.filter((f) => f.isDoc);
  const codeFiles = files.filter((f) => !f.isDoc && !f.isConfig);

  for (const doc of docFiles) {
    filesRead.push(doc.relativePath);
    const claims = extractClaims(doc);

    for (const claim of claims) {
      const contradiction = verifyClaim(claim, codeFiles, files);
      if (contradiction) {
        contradictions.push({
          ...contradiction,
          id: `contradiction-${contradictions.length + 1}`,
        });
      }
    }
  }

  return {
    data: contradictions,
    files_read: filesRead,
    duration_ms: Date.now() - startTime,
  };
}

function extractClaims(doc: ScannedFile): DocClaim[] {
  const claims: DocClaim[] = [];
  const lines = doc.content.split("\n");

  for (let i = 0; i < lines.length; i++) {
    const line = lines[i];

    // Algorithm claims (e.g., "uses Ed25519", "HMAC-SHA256")
    const algoMatch = line.match(/(?:uses?|implement|sign|encrypt|hash|algorithm)\s+[\w-]+/i);
    if (algoMatch) {
      claims.push({
        text: line.trim(),
        source: doc.relativePath,
        line: i + 1,
        category: "algorithm",
      });
    }

    // Command claims (code blocks with shell commands)
    if (line.trim().startsWith("```") && i + 1 < lines.length) {
      const nextLines: string[] = [];
      for (let j = i + 1; j < lines.length && !lines[j].trim().startsWith("```"); j++) {
        nextLines.push(lines[j]);
      }
      for (const cmdLine of nextLines) {
        if (cmdLine.match(/^\s*(npm|yarn|pnpm|pip|python|cargo|go|make|docker)/)) {
          claims.push({
            text: cmdLine.trim(),
            source: doc.relativePath,
            line: i + 1,
            category: "command",
          });
        }
      }
    }

    // Env var claims
    const envMatch = line.match(/[A-Z][A-Z0-9_]{2,}/g);
    if (envMatch) {
      for (const envVar of envMatch) {
        if (isLikelyEnvVar(envVar)) {
          claims.push({
            text: `${envVar} (referenced in docs)`,
            source: doc.relativePath,
            line: i + 1,
            category: "env-var",
          });
        }
      }
    }

    // Path claims
    const pathMatch = line.match(/`([^`]*\/[^`]+)`/g);
    if (pathMatch) {
      for (const p of pathMatch) {
        claims.push({
          text: p.replace(/`/g, ""),
          source: doc.relativePath,
          line: i + 1,
          category: "path",
        });
      }
    }
  }

  return claims;
}

function verifyClaim(
  claim: DocClaim,
  codeFiles: ScannedFile[],
  allFiles: ScannedFile[]
): Omit<Contradiction, "id"> | null {
  switch (claim.category) {
    case "algorithm":
      return verifyAlgorithmClaim(claim, codeFiles);
    case "env-var":
      return verifyEnvVarClaim(claim, codeFiles, allFiles);
    case "path":
      return verifyPathClaim(claim, allFiles);
    default:
      return null;
  }
}

function verifyAlgorithmClaim(
  claim: DocClaim,
  codeFiles: ScannedFile[]
): Omit<Contradiction, "id"> | null {
  const algorithms = [
    "Ed25519", "HMAC-SHA256", "HMAC-SHA512", "RSA", "AES-256",
    "SHA-256", "SHA-512", "bcrypt", "argon2", "scrypt",
    "ECDSA", "ChaCha20", "Poly1305",
  ];

  const docAlgos = algorithms.filter((a) =>
    claim.text.toLowerCase().includes(a.toLowerCase())
  );

  if (docAlgos.length === 0) return null;

  // Search code for actual algorithm usage
  for (const file of codeFiles) {
    const codeAlgos = algorithms.filter((a) =>
      file.content.toLowerCase().includes(a.toLowerCase())
    );

    // If code uses a different algorithm than docs claim
    for (const docAlgo of docAlgos) {
      for (const codeAlgo of codeAlgos) {
        if (docAlgo.toLowerCase() !== codeAlgo.toLowerCase()) {
          // Found a potential mismatch — verify it's in a relevant context
          if (isRelevantAlgoContext(file.content, codeAlgo)) {
            return {
              doc_claim: `Documentation references ${docAlgo}`,
              doc_source: `${claim.source}:${claim.line}`,
              code_reality: `Code actually uses ${codeAlgo}`,
              code_source: file.relativePath,
              severity: "critical",
              explanation: `Documentation claims ${docAlgo} but the implementation uses ${codeAlgo}. This will mislead developers about the actual cryptographic/hashing approach.`,
            };
          }
        }
      }
    }
  }

  return null;
}

function verifyEnvVarClaim(
  claim: DocClaim,
  codeFiles: ScannedFile[],
  allFiles: ScannedFile[]
): Omit<Contradiction, "id"> | null {
  const envVarMatch = claim.text.match(/([A-Z][A-Z0-9_]{2,})/);
  if (!envVarMatch) return null;

  const envVar = envVarMatch[1];

  // Check if the env var actually exists in code
  const inCode = codeFiles.some((f) => f.content.includes(envVar));
  const inEnvExample = allFiles.some(
    (f) => (f.relativePath.includes(".env") || f.relativePath.includes("env.example")) && f.content.includes(envVar)
  );

  if (!inCode && !inEnvExample) {
    return {
      doc_claim: `Documentation references env var ${envVar}`,
      doc_source: `${claim.source}:${claim.line}`,
      code_reality: `${envVar} not found in any source file or .env template`,
      code_source: "N/A",
      severity: "stale",
      explanation: `The environment variable ${envVar} is mentioned in documentation but doesn't appear in the codebase. It may have been renamed or removed.`,
    };
  }

  return null;
}

function verifyPathClaim(
  claim: DocClaim,
  allFiles: ScannedFile[]
): Omit<Contradiction, "id"> | null {
  const path = claim.text;

  // Skip URLs and obvious non-file paths
  if (path.startsWith("http") || path.startsWith("//") || path.includes("*")) return null;

  // Check if the claimed path exists in the file tree
  const exists = allFiles.some((f) => f.relativePath === path || f.relativePath.endsWith(path));

  if (!exists && path.includes("/") && !path.startsWith("$")) {
    return {
      doc_claim: `Documentation references path: ${path}`,
      doc_source: `${claim.source}:${claim.line}`,
      code_reality: `Path ${path} does not exist in the repository`,
      code_source: "file tree",
      severity: "stale",
      explanation: `The path ${path} is referenced in docs but doesn't exist. It may have been moved or deleted.`,
    };
  }

  return null;
}

function isLikelyEnvVar(s: string): boolean {
  // Must be at least 4 chars, contain at least one underscore, not be a common acronym
  if (s.length < 4) return false;
  if (!s.includes("_")) return false;
  const commonNonEnv = new Set(["TODO", "NOTE", "FIXME", "HACK", "README", "JSON", "HTML", "HTTP", "HTTPS", "API"]);
  return !commonNonEnv.has(s);
}

function isRelevantAlgoContext(content: string, algo: string): boolean {
  // Check if the algorithm appears in a signing, hashing, or crypto context
  const lines = content.split("\n");
  for (const line of lines) {
    if (line.toLowerCase().includes(algo.toLowerCase())) {
      if (line.match(/sign|hash|hmac|encrypt|decrypt|verify|digest|key/i)) {
        return true;
      }
    }
  }
  return false;
}
