# Script action manifest v1

## Purpose

A script action gives one local command a discoverable name, icon, inputs,
preview and execution policy. It is a small escape hatch for personal tooling,
not an extension marketplace or an in-process plugin API.

Manifests live in:

```text
$XDG_CONFIG_HOME/blazelauncher/actions/*.toml
```

Blazelauncher never downloads, installs or updates them automatically.

## Proposed v1 example

```toml
schema = 1
id = "local.slugify"
name = "Slugify text"
description = "Convert input text to a URL-safe slug"
icon = "insert-text"
keywords = ["slug", "text", "url"]

command = ["/home/example/.local/bin/slugify", "{query}"]
working_directory = "{home}"
input = "query"
output = "text/plain"
timeout_ms = 3000
risk = "pure"
confirmation = "never"
```

This schema is a proposal to implement and validate under its roadmap issue.
Once code ships a schema version, incompatible changes require a new version or
documented migration.

## Fields

| Field | Required | Rule |
| --- | --- | --- |
| `schema` | yes | Integer `1`. Reject unknown versions. |
| `id` | yes | Stable reverse-domain or `local.*`-style identifier; unique after normalisation. |
| `name` | yes | Short user-visible label. |
| `description` | yes | Plain-text explanation of the outcome. |
| `icon` | no | Theme icon name or validated local image path. |
| `keywords` | no | Bounded list of plain-text discovery terms. |
| `command` | yes | Non-empty argv array; never a shell string. |
| `working_directory` | no | Existing/resolvable directory template. |
| `input` | yes | `none`, `query`, `clipboard-text` or `payload-text`. |
| `output` | yes | `none` or `text/plain` in v1. |
| `timeout_ms` | yes | Bounded duration within project-defined minimum/maximum. |
| `risk` | yes | `pure`, `read-only`, `side-effecting`, `networked` or `unknown`. |
| `confirmation` | yes | `never` or `always`; `never` is valid only for `pure`/`read-only`. |

The manifest's risk claim improves disclosure but is not a security sandbox.
Blazelauncher cannot prove that an arbitrary executable is pure. First run and
changed-manifest behaviour should therefore remain conservative.

## Template values

V1 permits complete-token or safely substituted values only:

- `{query}` — current palette query after the action is selected;
- `{clipboard}` — current text clipboard, only when input declares it;
- `{payload}` — composed `text/plain` input;
- `{home}` — resolved user home for working-directory convenience.

No command substitution, glob expansion, pipes, redirects, environment
expansion or shell syntax is interpreted. The engine builds an argv array and
uses `shell=False`. Missing required input is a validation error, not an empty
surprise invocation.

## Execution contract

Before execution, show:

- manifest identity and source path;
- resolved executable and argv with sensitive input visually marked/redacted
  where appropriate;
- working directory, timeout, input source, output type and risk;
- whether confirmation is required.

Execution uses a bounded worker, minimal inherited environment policy,
cancel/timeout handling and a maximum captured-output size. Standard output is
plain text data, never instructions or rich HTML. Standard error is available
in a bounded diagnostic view and is not added to activity history by default.

Script actions cannot:

- contribute dynamic result lists or ranking scores;
- import code into the Blazelauncher process;
- register background/file/timer triggers;
- ask Blazelauncher to install dependencies;
- download or install additional manifests;
- bypass confirmation through stdout or exit codes;
- request root or system-level execution through a privileged helper.

## Validation and change detection

- Parse TOML strictly; reject unknown security-relevant fields rather than
  guessing intent.
- Resolve the executable predictably and show unavailable status when missing.
- Validate placeholder/input compatibility and confirmation/risk combinations.
- Store a manifest content hash. A changed manifest loses any remembered first-
  run trust/confirmation acknowledgement.
- Duplicate IDs are errors with both source paths reported.
- `blazelauncher action validate <manifest>` and `doctor` expose actionable
  diagnostics without executing the command.

## Example use cases

- project-specific formatter or report script;
- local API health check that the user explicitly marks networked;
- text cleanup/slugification tool;
- opening a known workstation layout through a reviewed helper;
- passing selected text to an existing personal CLI.

If a use case needs dynamic search results, persistent background state or a
multi-stage workflow, it is outside manifest v1 and requires a separate
architecture decision.
