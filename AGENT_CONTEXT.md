# 專案上下文 (Agent Context)：Tech Unfiltered

> **最後更新時間**：2026-08-31 15:06
> **自動生成**：由 `prepare_context.py` 產生，供 AI Agent 快速掌握專案全局

---

## 🎯 1. 專案目標 (Project Goal)
* **核心目的**：> An open-source, zero-trust autonomous media network built on Next.js, LiteRT, and local LLMs.
* _完整說明見 [README.md](README.md)_

## 🛠️ 2. 技術棧與環境 (Tech Stack & Environment)
* _（未偵測到 package.json / pyproject.toml / requirements.txt）_

## 📂 3. 核心目錄結構 (Core Structure)
_(💡 AI 讀取守則：請依據此結構尋找對應檔案，勿盲目猜測路徑)_
```text
Tech Unfiltered/
├── AGENT_CONTEXT.md
├── CONTRIBUTING.md
├── LICENSE
├── LiteRT
│   ├── BUILD
│   ├── BUILD.darts_clone
│   ├── BUILD.sentencepiece
│   ├── BUILD.tomlplusplus
│   ├── CODE_OF_CONDUCT.md
│   ├── CONTRIBUTING.md
│   ├── LICENSE
│   ├── PATCH.flatbuffers_windows_no_bash
│   ├── PATCH.protobuf_port_msvc_compat
│   ├── PATCH.sentencepiece
│   ├── Package.swift
│   ├── README.md
│   ├── RELEASE.md
│   ├── SECURITY.md
│   ├── WORKSPACE
│   ├── android_ndk_env.bzl
│   ├── ci
│   │   ├── check_openvino_version_sync.py
│   │   ├── run_bazel_build.sh
│   │   ├── run_bazel_test.sh
│   │   ├── run_bazel_test_with_docker.sh
│   │   ├── setup_with_binary.py
│   │   ├── test_pip_package.sh
│   │   ├── tflite-android.Dockerfile
│   │   ├── tflite-py3-arm64.Dockerfile
│   │   ├── tflite-py3.Dockerfile
│   │   └── tools
│   ├── cmake_example
│   │   ├── CMakeLists.txt
│   │   ├── run_model_simple.cc
│   │   └── tflite_minimal.cc
│   ├── configure
│   ├── configure.py
│   ├── docker_build
│   │   ├── README.md
│   │   ├── docker-compose.yml
│   │   ├── hermetic_build.Dockerfile
│   │   ├── requirements.in
│   │   ├── requirements.txt
│   │   ├── run_build.sh
│   │   ├── setup_bazel_env.sh
│   │   └── verify_android_env.sh
│   ├── g3doc
│   │   ├── apis
│   │   ├── google
│   │   ├── instructions
│   │   └── sources
│   ├── litert
│   │   ├── BUILD
│   │   ├── CMakeLists.txt
│   │   ├── CMakePresets.json
│   │   ├── COMPILER_PLUGIN.md
│   │   ├── DISPATCH_API.md
│   │   ├── JIT_COMPILATION.md
│   │   ├── PATTERN_MATCHING.md
│   │   ├── README.md
│   │   ├── TESTING.md
│   │   ├── __init__.py
│   │   ├── _dummy.md
│   │   ├── ats
│   │   ├── c
│   │   ├── cc
│   │   ├── cc_sdk
│   │   ├── compiler
│   │   ├── core
│   │   ├── experimental
│   │   ├── google
│   │   ├── integration_test
│   │   ├── js
│   │   ├── kotlin
│   │   ├── litert.bzl
│   │   ├── objc
│   │   ├── opensource_only.files
│   │   ├── prebuilt
│   │   ├── python
│   │   ├── reviews.gwsq
│   │   ├── runtime
│   │   ├── rust
│   │   ├── samples
│   │   ├── sdk_util
│   │   ├── swift
│   │   ├── tensor
│   │   ├── test
│   │   ├── tflite_support
│   │   ├── tools
│   │   ├── vendors
│   │   └── version.bzl
│   ├── ml_drift_delegate
│   │   ├── delegate
│   │   └── tflite
│   ├── support
│   │   ├── preprocessor
│   │   ├── tokenizer
│   │   └── util
│   ├── tensor
│   │   ├── BUILD
│   │   ├── CMakeLists.txt
│   │   ├── README.md
│   │   ├── arithmetic.h
│   │   ├── arithmetic_graph.h
│   │   ├── arithmetic_test.cc
│   │   ├── backends
│   │   ├── buffer.cc
│   │   ├── buffer.h
│   │   ├── buffer_test.cc
│   │   ├── datatypes.h
│   │   ├── datatypes_test.cc
│   │   ├── examples
│   │   ├── internal
│   │   ├── parsers
│   │   ├── runners
│   │   ├── tensor.cc
│   │   ├── tensor.h
│   │   ├── tensor_api.md
│   │   ├── tensor_test.cc
│   │   ├── utils
│   │   └── wasm
│   ├── tensorflow_source_rules.bzl
│   ├── tflite
│   │   ├── BUILD
│   │   ├── CMakeLists.txt
│   │   ├── README.md
│   │   ├── acceleration
│   │   ├── allocation.h
│   │   ├── allocation_test.cc
│   │   ├── api_visibility.bzl
│   │   ├── arena_planner.cc
│   │   ├── arena_planner.h
│   │   ├── arena_planner_subgraph_test.cc
│   │   ├── arena_planner_test.cc
│   │   ├── array.cc
│   │   ├── array.h
│   │   ├── array_test.cc
│   │   ├── async
│   │   ├── builtin_op_data.h
│   │   ├── builtin_ops.h
│   │   ├── c
│   │   ├── cmake
│   │   ├── context.h
│   │   ├── context_util.h
│   │   ├── converter
│   │   ├── core
│   │   ├── create_op_resolver.h
│   │   ├── create_op_resolver_with_selected_ops.cc
│   │   ├── delegates
│   │   ├── error_reporter.h
│   │   ├── examples
│   │   ├── experimental
│   │   ├── external_cpu_backend_context.cc
│   │   ├── external_cpu_backend_context.h
│   │   ├── g3doc
│   │   ├── generate-pc.sh
│   │   ├── graph_info.cc
│   │   ├── graph_info.h
│   │   ├── graph_info_test.cc
│   │   ├── internal
│   │   ├── interpreter.h
│   │   ├── interpreter_builder.h
│   │   ├── interpreter_options.h
│   │   ├── interpreter_test.cc
│   │   ├── interpreter_test_util.h
│   │   ├── ios
│   │   ├── java
│   │   ├── kernels
│   │   ├── lib_package
│   │   ├── logger.cc
│   │   ├── logger.h
│   │   ├── memory_planner.h
│   │   ├── micro
│   │   ├── minimal_logging.cc
│   │   ├── minimal_logging.h
│   │   ├── minimal_logging_android.cc
│   │   ├── minimal_logging_default.cc
│   │   ├── minimal_logging_ios.cc
│   │   ├── minimal_logging_test.cc
│   │   ├── model.h
│   │   ├── model_builder.h
│   │   ├── model_flex_test.cc
│   │   ├── model_xnnpack_test.cc
│   │   ├── mutable_op_resolver.cc
│   │   ├── mutable_op_resolver.h
│   │   ├── mutable_op_resolver_test.cc
│   │   ├── mutable_op_resolver_utils.cc
│   │   ├── mutable_op_resolver_utils.h
│   │   ├── mutable_op_resolver_utils_test.cc
│   │   ├── namespace.h
│   │   ├── nnapi
│   │   ├── objc
│   │   ├── op_resolver.h
│   │   ├── opensource_only.files
│   │   ├── optional_debug_tools.cc
│   │   ├── optional_debug_tools.h
│   │   ├── optional_debug_tools_test.cc
│   │   ├── portable_type_to_tflitetype.h
│   │   ├── profiling
│   │   ├── python
│   │   ├── schema
│   │   ├── shared_library.h
│   │   ├── signature_runner.h
│   │   ├── simple_memory_arena.cc
│   │   ├── simple_memory_arena.h
│   │   ├── simple_memory_arena_debug_dump.cc
│   │   ├── simple_memory_arena_test.cc
│   │   ├── simple_planner.cc
│   │   ├── simple_planner.h
│   │   ├── simple_planner_test.cc
│   │   ├── special_rules.bzl
│   │   ├── stablehlo
│   │   ├── stateful_error_reporter.h
│   │   ├── stderr_reporter.cc
│   │   ├── stderr_reporter.h
│   │   ├── stderr_reporter_test.cc
│   │   ├── string_type.h
│   │   ├── string_util.cc
│   │   ├── string_util.h
│   │   ├── string_util_test.cc
│   │   ├── swift
│   │   ├── tensorflow_profiler_logger.h
│   │   ├── tensorflow_profiler_logger_shim.cc
│   │   ├── test_util.h
│   │   ├── test_util_test.cc
│   │   ├── testdata
│   │   ├── testing
│   │   ├── tflite_exported_symbols.lds
│   │   ├── tflite_version_script.lds
│   │   ├── tflite_with_xnnpack.cc
│   │   ├── tflite_with_xnnpack_optional.cc
│   │   ├── tflite_with_xnnpack_optional.h
│   │   ├── toco
│   │   ├── tools
│   │   ├── tutorials
│   │   ├── type_to_tflitetype.h
│   │   ├── type_to_tflitetype_test.cc
│   │   ├── types
│   │   ├── util.cc
│   │   ├── util.h
│   │   ├── util_test.cc
│   │   └── version.h
│   ├── third_party
│   │   ├── FP16
│   │   ├── coremltools
│   │   ├── dawn
│   │   ├── exynos_ai_litecore
│   │   ├── google_tensor
│   │   ├── intel_openvino
│   │   ├── jinja2
│   │   ├── lark
│   │   ├── litert_gpu
│   │   ├── litert_prebuilts
│   │   ├── markupsafe
│   │   ├── models
│   │   ├── neuro_pilot
│   │   ├── qairt
│   │   ├── stblib
│   │   ├── tensorflow
│   │   ├── tqdm
│   │   └── xdsl
│   ├── tools
│   │   └── cc_target_os
│   └── weight_loader
│       ├── BUILD
│       ├── external_weight_loader_litert.cc
│       ├── external_weight_loader_litert.h
│       └── external_weight_loader_litert_test.cc
├── README.md
├── agent_brain
│   ├── browser
│   │   ├── scratchpad_gcmkx2cf.md
│   │   └── scratchpad_qhv0k87m.md
│   ├── implementation_plan.md
│   ├── implementation_plan.md.metadata.json
│   ├── media__1784508268274.jpg
│   ├── media__1784511785646.jpg
│   ├── media__1784523516195.png
│   ├── media__1784569973139.jpg
│   ├── media__1784570105866.jpg
│   ├── sponsorship_deck.md
│   ├── sponsorship_deck.md.metadata.json
│   ├── task.md
│   ├── task.md.metadata.json
│   ├── walkthrough.md
│   └── walkthrough.md.metadata.json
├── agi-backend
│   ├── Dockerfile
│   ├── KGU_Ecosystem
│   │   ├── Agent-Reach
│   │   ├── AionUi
│   │   ├── AppFlowy
│   │   ├── FreeEed
│   │   ├── GraveFlow
│   │   ├── HunyuanVideo
│   │   ├── Hy3
│   │   ├── LiteRT
│   │   ├── OmniRoute
│   │   ├── OpenMontage
│   │   ├── Project_Severance_AI
│   │   ├── SEAL
│   │   ├── TensorRT-LLM
│   │   ├── Understand-Anything
│   │   ├── activepieces
│   │   ├── agent-zero
│   │   ├── ai-engineering-from-scratch
│   │   ├── baserow
│   │   ├── buzz
│   │   ├── cal.diy
│   │   ├── carbon-bloom-boost
│   │   ├── claude-code
│   │   ├── colibri
│   │   ├── deer-flow
│   │   ├── ego-lite
│   │   ├── firecrawl
│   │   ├── free-claude-code
│   │   ├── graphql-engine
│   │   ├── graphql-yoga
│   │   ├── headscale
│   │   ├── hermes-agent
│   │   ├── infinite-brain-os
│   │   ├── knowledge-work-plugins
│   │   ├── launch-your-agent
│   │   ├── marketingskills
│   │   ├── mautic
│   │   ├── mem0
│   │   ├── multica
│   │   ├── openagentskill
│   │   ├── openhuman
│   │   ├── reticulum-meshchat
│   │   ├── rr-kguinternational
│   │   ├── strix
│   │   ├── supabase
│   │   ├── twenty
│   │   ├── unsloth
│   │   └── yt-dlp
│   ├── agents
│   ├── docker-compose.yml
│   ├── headscale
│   │   └── config
│   ├── ingestion
│   ├── main.py
│   ├── media
│   ├── memory
│   ├── prometheus.yml
│   ├── requirements.txt
│   └── scripts
│       └── register_node.sh
├── diary
│   └── 2026
│       └── 08
├── landing_page.html
└── tech-unfiltered
    ├── AGENTS.md
    ├── CLAUDE.md
    ├── README.md
    ├── app
    │   ├── globals.css
    │   ├── layout.tsx
    │   └── page.tsx
    ├── components
    │   ├── AgentChat.tsx
    │   ├── CinematicGallery.tsx
    │   ├── CommandCenter.tsx
    │   ├── OrganoidBackground.tsx
    │   ├── PitchDeck.tsx
    │   └── SignalDashboard.tsx
    ├── data
    │   └── targets.json
    ├── eslint.config.mjs
    ├── next-env.d.ts
    ├── next.config.ts
    ├── package-lock.json
    ├── package.json
    ├── postcss.config.mjs
    ├── public
    │   ├── ai-brain.jpg
    │   ├── ai-brain.png
    │   ├── file.svg
    │   ├── globe.svg
    │   ├── logo.jpg
    │   ├── next.svg
    │   ├── vercel.svg
    │   └── window.svg
    ├── scripts
    │   └── autonomous-outreach.ts
    ├── src
    │   └── app
    ├── tsconfig.json
    └── tsconfig.tsbuildinfo
```

## 🏛️ 4. 架構與設計約定 (Architecture & Conventions)
* _（尚無 `.auto-skill-local.md`，專案踩坑經驗將在開發過程中自動累積）_

## 🚦 5. 目前進度與待辦 (Current Status & TODO)
_(自動提取自最近日記 2026-08-31)_

### 🚧 待辦事項
- [ ] Minimize storage footprint of KGU Ecosystem and agent memory.
- [ ] Connect `voicebox` for TTS integration into the podcast logic.
- [ ] Activate the `Automated PR Firm` pipeline for automated social publishing.

