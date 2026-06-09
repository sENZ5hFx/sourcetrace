/**
 * Git utilities for extracting history and metadata.
 */

import { execSync } from "child_process";
import { existsSync } from "fs";
import { join } from "path";

export interface GitInfo {
  isRepo: boolean;
  branch?: string;
  remoteUrl?: string;
  lastCommitDate?: string;
  totalCommits?: number;
}

export function getGitInfo(repoPath: string): GitInfo {
  if (!existsSync(join(repoPath, ".git"))) {
    return { isRepo: false };
  }

  try {
    const branch = execGit(repoPath, "rev-parse --abbrev-ref HEAD");
    const remoteUrl = execGit(repoPath, "remote get-url origin");
    const lastCommitDate = execGit(repoPath, "log -1 --format=%ci");
    const totalCommits = parseInt(execGit(repoPath, "rev-list --count HEAD") || "0", 10);

    return {
      isRepo: true,
      branch: branch || undefined,
      remoteUrl: remoteUrl || undefined,
      lastCommitDate: lastCommitDate || undefined,
      totalCommits: isNaN(totalCommits) ? undefined : totalCommits,
    };
  } catch {
    return { isRepo: true };
  }
}

export function getFileLastModified(repoPath: string, filePath: string): string | null {
  try {
    return execGit(repoPath, `log -1 --format=%ci -- "${filePath}"`);
  } catch {
    return null;
  }
}

function execGit(cwd: string, args: string): string {
  try {
    return execSync(`git ${args}`, { cwd, encoding: "utf-8", timeout: 5000 }).trim();
  } catch {
    return "";
  }
}
