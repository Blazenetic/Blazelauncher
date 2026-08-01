# Command Palette specification

## Product position

Blazelauncher's palette is the fast action surface for a developer workstation.
It complements KRunner instead of competing on basic application launching.
The differentiators are local developer workflows, typed composition, visible
risk and rich previews.

The first complete palette milestone has exactly 15 built-in actions. New ideas
wait until these are useful, fast, private and well tested.

## Presentation surface

Everything below assumes an overlay that appears centred on the active output,
takes keyboard focus and dismisses on Escape. On Wayland that is not something
a client can simply do, and how Blazelauncher achieves it is an open question —
see decision record 0004, which must be accepted before this specification can
be implemented. The performance targets at the end of this document may need to
be restated as compositor-dependent once it is answered.

## Interaction model

The palette opens as a compact, keyboard-first Kirigami overlay with:

- query field and optional provider scope chips;
- ranked results with icon, title, context and risk/status badge;
- rich preview for paths, repository state, note excerpts, task commands,
  conversions and exact invocations;
- primary action on Enter, alternate actions through an explicit action menu;
- a compose control that passes a typed value to a compatible transform;
- Escape to cancel/close and complete keyboard navigation.

Provider prefixes/keywords may speed expert use, but ordinary natural labels
must remain discoverable. Prefix syntax should be data-driven and must not make
the empty palette resemble a terminal prompt.

## The 15 built-in actions

### Navigation and local knowledge

1. **Search files** — search configured roots; preview path, type, size and
   modification time; open the file or containing folder.
2. **Open recent projects** — rank explicitly configured and locally observed
   project roots; open in a configured editor, terminal or file manager.
3. **Open Git repositories** — find repositories beneath configured roots;
   preview branch/worktree state; open locally or visit a configured remote.
4. **Search Obsidian notes** — search explicitly configured vaults read-only;
   preview bounded title/path/excerpt; open by file or Obsidian URI.
5. **Search browser history** — search explicitly enabled local browser
   profiles through disposable read-only database snapshots; preview title,
   domain and timestamp; open only after selection.

### Execution and workstation control

6. **Run saved commands** — user-defined structured argv, working directory,
   environment differences, risk and confirmation policy.
7. **Trigger workstation sessions** — run a named, reviewable bundle of terminal,
   editor and project-opening actions; MVP+ sessions are a bounded ordered
   preset, not a general workflow language.
8. **Control media** — play/pause, next, previous and volume through a
   capability-detected desktop adapter such as `playerctl`.
9. **Open SSH destinations** — list concrete aliases from explicitly selected
   SSH config sources; preview resolved alias/user/host where safe; open through
   the configured terminal without reading keys or secrets.
10. **Run `just` tasks** — discover task names for a selected/current project;
    preview recipe description, directory and exact argv before execution.
11. **Run `mise` tasks** — discover tasks through a version-checked adapter;
    preview source, directory and exact argv before execution.

### Utilities and composition

12. **Convert units** — pure local conversion across an intentionally supported
    unit set; show expression, result and copy action.
13. **Generate UUIDs** — generate standards-based UUIDs locally; default to
    UUIDv4 initially; preview/copy without persisting values.
14. **Encode/decode text** — explicit UTF-8-safe Base64, URL and hexadecimal
    transformations with size limits and clear invalid-input errors.
15. **Transform clipboard text** — feed current text clipboard into compatible
    pure transforms, preview the result, then explicitly copy it back.

The numbering above is canonical for MVP+ acceptance. Implementations may group
actions into fewer providers internally.

## Provider source rules

| Source | Default | Privacy and safety rule |
| --- | --- | --- |
| Files/projects/repos | Configured roots only | Honour ignores and budgets; do not crawl the whole home directory silently. |
| Obsidian | Disabled until a vault path is selected | Read-only; no note edits or query/content logging. |
| Browser history | Disabled per profile until enabled | Copy the SQLite database to a bounded temporary snapshot; never modify the live profile. |
| SSH | Explicit config source | Concrete aliases only; no keys, passwords or `known_hosts` content. |
| `just`/`mise` | Capability-detected per project | Version-check commands; discovery is read-only; execution shows exact argv. |
| Media | Capability-detected | Local session only; clear unavailable state. |
| Clipboard | Explicit invocation | Text only in MVP+; never persisted or logged. |

Optional command-line tools such as `fd`, `rg`, `playerctl`, `just` and `mise`
are adapters, not unconditional dependencies. `doctor` reports capability and
fallback status. Provider behaviour must be tested against the supported tool
versions rather than assuming output formats indefinitely.

## Ranking and query behaviour

- Exact IDs/aliases and explicit provider scope outrank fuzzy matches.
- Prefix, word-boundary and recency components are deterministic and testable.
- Recency is local and optional. Store stable result identity and timestamp,
  not the raw query or sensitive result text.
- Empty-query content is small and useful: pinned/saved actions and recent
  non-sensitive entities, not a noisy history dump.
- A query generation owns its results. Late work from an older generation is
  discarded.
- Provider failures appear as a quiet status/diagnostic, not a modal cascade.

## Preview contract

Previews are bounded, cancellable and side-effect free. They may include:

- highlighted path/note/history match excerpts;
- repository branch, clean/dirty summary and remote link;
- task description, project directory and exact command;
- resolved executable, argv, environment differences and working directory;
- input/output types, transformation result and copy action;
- risk, confirmation, network and mutation badges.

Do not render untrusted rich HTML. Treat excerpts and script output as plain
text unless a purpose-built safe renderer exists.

## Composition boundary

Composition passes one typed result into one compatible pure/read-only action.
Examples:

- UUID result → copy to clipboard;
- selected note path → open containing repository;
- text → Base64 encode → copy;
- browser URL → copy.

MVP+ does not save pipelines, branch, loop, schedule, react to filesystem
events or continue after a side-effecting action. Workstation sessions are
explicit ordered presets with a separate schema, not a loophole for a workflow
engine.

## Performance acceptance

Measure on the reference CachyOS/KDE Plasma/Wayland workstation and record
hardware, data-set size, cold/warm state and sample count.

- optional resident-mode toggle-to-visible target: p95 at or below 150 ms;
- cached/read-only provider first-useful-result target: p95 at or below 300 ms;
- keystroke generations cancel or quarantine stale results immediately;
- no provider blocks input/rendering on the Qt main thread.

Targets guide optimisation; measurements must remain truthful and may lead to
an ADR adjustment before release.

## Later candidates

- KRunner adapter after the action API is stable;
- Plasma widget using the CLI/local API;
- additional browsers/editors/terminals through adapters;
- script-provided dynamic result protocol, only if static script actions prove
  insufficient and a secure boundary is designed;
- semantic/AI actions only with explicit privacy and model-routing decisions.
