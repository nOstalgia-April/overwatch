# AGENTS.md

Purpose: quick onboarding notes for the ow2026 Overwatch Workshop scripts.

Project summary
- Workspace: `c:\Users\ROG\Desktop\ow`
- Entry point: `ow2026/main.del` imports `winston_ai.del`, `地图文本菜单.del`, and `观察视角.del`

Key files
- `ow2026/winston_ai.del`
  - Spawns Winston pet on Ability2 (uses `MinWait()` to prevent repeat triggers).
  - Uses `MinWait()` after `CreateDummyBot` before setting `bot_isPet` and `bot_isWinstonAI`.
  - Debug HUD rule "Debug1 Winston HUD" shows AI state (Host only, one-time).
  - Combat AI drives primary/secondary/melee/jump based on `bot_target`.
- `ow2026/解压形式寻路.del`
  - Pathfinding + bot state machine (wander/chase/combat).
  - Key vars: `bot_isPet`, `bot_isWinstonAI`, `bot_state`, `is_fighting`, `bot_target`, `bot_targetArray`.
  - Enemy team uses `OppositeTeamOf(TeamOf(EventPlayer()))`.
  - Pet pre-wander seek rule checks for enemies before wandering.
- `ow2026/观察视角.del`
  - Observe camera: Interact + PrimaryFire selects teammate; right-click drags orbit.
  - Camera uses `Eye` (raycast) and `Lookat`.
- `ow2026/地图文本菜单.del`
  - Class-based menu (`MenuButton` + `Button_Pool`), similar to `a/地图文本菜单.del`.
  - Observation-friendly `OpenMenu/CloseMenu` (no `StopCamera`, anchor facing from `Eye/Lookat`).
  - Menu plane uses camera `Eye/Lookat` (so it follows observation camera).
  - Button click uses per-button `OnClick` (no card-specific logic baked in).
  - Cursor math uses `AnchorFacing` and camera direction; X-axis reversal was fixed recently.
- Menu system candidates (map text menu)
  - `a/地图文本菜单.del` (and same as `小工具/地图文本菜单.del`): full OpenMenu/CloseMenu, cursor from `AnchorFacing`, button hover + click, hover background text.
  - `ostw/斗魂竞技场/地图文本菜单.del`: slim version (buttons + cursor math) but no OpenMenu/CloseMenu or click handling.
  - `boss菜单.del`: expanded, compressed button data + paging; likely newer but heavier.

Recent changes
- Winston flags set after `MinWait()` to avoid false `bot_isPet`/`bot_isWinstonAI`.
- Winston AI now falls back to `bot_targetArray` if `bot_target` is null.
- Combat entry now assigns a target from `bot_targetArray` when missing.
- Added pet seek check before wandering.
- Observation menu: holding Interact while observing opens menu; release closes. Selection is blocked while menu is open.
- Card hand UI: map text cannot scale, so cards are a vertical list; hover changes color; click toggles selection with hover text.

Known assumptions / gotchas
- If enemies are fixed to Team1, players/pets must be Team2 or change enemy selection logic.
- Debug HUD is visible to `HostPlayer()` only.
- Open item: Winston may attack while chasing because `bot_target` persists for pursuit and pet pre-wander seek sets a target; consider splitting `bot_combatTarget` (visible/attack) from `bot_target` (chase) or gate attacks by `is_fighting`/`BOT_STATE_COMBAT`.
- Lock convention: prefer a trailing `MinWait()` as the only lock mechanism unless explicitly asked to add more.

Quick checks
- Press Ability2 to spawn Winston; verify Debug1 HUD values.
- Confirm `bot_isPet` and `bot_isWinstonAI` turn true after spawn.
