#!/usr/bin/env python3
"""
Tech Unfiltered SI — End-to-End QA & Media Stream Verifier
Tests http://127.0.0.1:8899 across:
  1. GET /landing_page.html (HTTP 200, required DOM IDs, security headers)
  2. All backend workflow endpoints (GET & POST)
  3. Media asset & HTTP 206 Partial Content byte-range streaming verification
Saves full JSON test report to services/qa_launch_report.json.
"""

import os
import sys
import json
import time
import urllib.request
import urllib.error
from datetime import datetime, timezone

BASE_URL = "http://127.0.0.1:8899"
ROOT_DIR = "/Users/jccoffey/Documents/KGU International/1. Internal Operations & Tech/Tech Unfiltered"
REPORT_PATH = os.path.join(ROOT_DIR, "services", "qa_launch_report.json")


def http_request(path, method="GET", payload=None, extra_headers=None, timeout=15):
    url = f"{BASE_URL}{path}"
    headers = {
        "User-Agent": "KGU-Sovereign-QA-Verifier/4.0",
        "Origin": BASE_URL,
    }
    if extra_headers:
        headers.update(extra_headers)

    data = None
    if payload is not None:
        data = json.dumps(payload).encode("utf-8")
        headers["Content-Type"] = "application/json"

    req = urllib.request.Request(url, data=data, headers=headers, method=method)
    t0 = time.perf_counter()
    try:
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            body = resp.read()
            latency_ms = round((time.perf_counter() - t0) * 1000, 2)
            resp_headers = {k.lower(): v for k, v in resp.getheaders()}
            return {
                "ok": True,
                "status": resp.status,
                "headers": resp_headers,
                "body": body,
                "latency_ms": latency_ms,
                "error": None,
            }
    except urllib.error.HTTPError as e:
        latency_ms = round((time.perf_counter() - t0) * 1000, 2)
        resp_headers = {k.lower(): v for k, v in e.headers.items()} if e.headers else {}
        return {
            "ok": False,
            "status": e.code,
            "headers": resp_headers,
            "body": e.read() if e.fp else b"",
            "latency_ms": latency_ms,
            "error": str(e),
        }
    except Exception as e:
        latency_ms = round((time.perf_counter() - t0) * 1000, 2)
        return {
            "ok": False,
            "status": 0,
            "headers": {},
            "body": b"",
            "latency_ms": latency_ms,
            "error": str(e),
        }


def run_qa_suite():
    started_at = datetime.now(timezone.utc).isoformat()
    tests = []

    def record_test(category, name, passed, status_code, latency_ms, details):
        tests.append({
            "category": category,
            "name": name,
            "passed": bool(passed),
            "status_code": status_code,
            "latency_ms": latency_ms,
            "details": details,
        })

    # =========================================================================
    # 1. LANDING PAGE & SECURITY HEADERS VERIFICATION
    # =========================================================================
    res = http_request("/landing_page.html", method="GET")
    html_text = res["body"].decode("utf-8", errors="replace")
    required_dom_ids = [
        "liveCharacterVideo",
        "characters-4d",
        "n8n-10core-matrix",
        "episodes",
        "monetization",
        "book-now",
    ]
    dom_presence = {
        f"#{dom_id}": (f'id="{dom_id}"' in html_text or f"id='{dom_id}'" in html_text)
        for dom_id in required_dom_ids
    }
    required_sec_headers = {
        "x-frame-options": "DENY",
        "x-content-type-options": "nosniff",
        "x-xss-protection": "1; mode=block",
        "strict-transport-security": "max-age=63072000; includeSubDomains; preload",
        "x-sovereign-shield": "KGU-Cybersecurity-Active",
        "accept-ranges": "bytes",
    }
    sec_header_checks = {
        h: (res["headers"].get(h) == expected)
        for h, expected in required_sec_headers.items()
    }
    lp_passed = (
        res["status"] == 200
        and all(dom_presence.values())
        and all(sec_header_checks.values())
    )
    record_test(
        "frontend_dom_and_security",
        "GET /landing_page.html (DOM IDs & Security Headers)",
        lp_passed,
        res["status"],
        res["latency_ms"],
        {
            "bytes": len(res["body"]),
            "domIdsVerified": dom_presence,
            "securityHeadersVerified": sec_header_checks,
        },
    )

    # =========================================================================
    # 2. BACKEND WORKFLOW ENDPOINTS VERIFICATION
    # =========================================================================
    # 2a. GET /api/workflow/state
    r_state = http_request("/api/workflow/state", method="GET")
    j_state = json.loads(r_state["body"].decode("utf-8")) if r_state["status"] == 200 else {}
    record_test(
        "backend_workflow",
        "GET /api/workflow/state",
        r_state["status"] == 200 and j_state.get("ok") is True and "stats" in j_state,
        r_state["status"],
        r_state["latency_ms"],
        {"engine": j_state.get("engine"), "stats": j_state.get("stats")},
    )

    # 2b. POST /api/workflow/avatar-call (joann, george, aris, duo)
    for speaker in ("joann", "george", "aris", "duo"):
        r_av = http_request(
            "/api/workflow/avatar-call",
            method="POST",
            payload={"speaker": speaker},
        )
        j_av = json.loads(r_av["body"].decode("utf-8")) if r_av["status"] == 200 else {}
        char_info = j_av.get("character", {})
        passed_av = (
            r_av["status"] == 200
            and j_av.get("ok") is True
            and char_info.get("id") == speaker
            and bool(j_av.get("videoStreamUrl"))
            and bool(j_av.get("workflowId"))
        )
        record_test(
            "backend_workflow",
            f"POST /api/workflow/avatar-call (speaker={speaker})",
            passed_av,
            r_av["status"],
            r_av["latency_ms"],
            {
                "workflowId": j_av.get("workflowId"),
                "speaker": char_info.get("id"),
                "name": char_info.get("name"),
                "videoStreamUrl": j_av.get("videoStreamUrl"),
            },
        )

    # 2c. POST /api/workflow/client-tool (tool: "tour")
    r_tool = http_request(
        "/api/workflow/client-tool",
        method="POST",
        payload={"tool": "tour", "actor": "Joann Coffey"},
    )
    j_tool = json.loads(r_tool["body"].decode("utf-8")) if r_tool["status"] == 200 else {}
    record_test(
        "backend_workflow",
        'POST /api/workflow/client-tool (tool="tour")',
        r_tool["status"] == 200
        and j_tool.get("ok") is True
        and j_tool.get("tool") == "tour"
        and j_tool.get("status") == "EXECUTED",
        r_tool["status"],
        r_tool["latency_ms"],
        {
            "workflowId": j_tool.get("workflowId"),
            "domTargets": j_tool.get("domTargets"),
            "status": j_tool.get("status"),
        },
    )

    # 2d. POST /api/workflow/csuite-cycle
    r_csuite = http_request(
        "/api/workflow/csuite-cycle",
        method="POST",
        payload={"episodeId": "ep-048"},
    )
    j_csuite = json.loads(r_csuite["body"].decode("utf-8")) if r_csuite["status"] == 200 else {}
    execs = j_csuite.get("executives", [])
    record_test(
        "backend_workflow",
        "POST /api/workflow/csuite-cycle",
        r_csuite["status"] == 200 and j_csuite.get("ok") is True and len(execs) == 7,
        r_csuite["status"],
        r_csuite["latency_ms"],
        {
            "workflowId": j_csuite.get("workflowId"),
            "executivesCount": len(execs),
            "marginalCost": j_csuite.get("marginalCost"),
        },
    )

    # 2e. POST /api/workflow/episode-select
    r_ep = http_request(
        "/api/workflow/episode-select",
        method="POST",
        payload={
            "episodeId": "ep-048",
            "title": "The Architecture of SI & Sovereign Hardware Nodes",
            "videoSrc": "videos/tec_26_08_05.mp4",
            "reelSrc": "videos/0805_clip1.mp4",
            "audioSrc": "audio/tec_26_08_05.mp3",
        },
    )
    j_ep = json.loads(r_ep["body"].decode("utf-8")) if r_ep["status"] == 200 else {}
    record_test(
        "backend_workflow",
        "POST /api/workflow/episode-select",
        r_ep["status"] == 200
        and j_ep.get("ok") is True
        and j_ep.get("episodeId") == "ep-048"
        and j_ep.get("notebookLmRemoved") is True,
        r_ep["status"],
        r_ep["latency_ms"],
        {
            "workflowId": j_ep.get("workflowId"),
            "episodeId": j_ep.get("episodeId"),
            "matchedVideo": j_ep.get("matchedVideo"),
            "matchedReel": j_ep.get("matchedReel"),
            "matchedAudio": j_ep.get("matchedAudio"),
        },
    )

    # 2f. POST /api/workflow/book-call
    r_book = http_request(
        "/api/workflow/book-call",
        method="POST",
        payload={
            "name": "QA Sovereign Executive Verification",
            "phone": "1-888-548-7683",
            "email": "qa-verification@kgu-sovereign.io",
            "tier": "liability-audit",
            "amount": 25000,
        },
    )
    j_book = json.loads(r_book["body"].decode("utf-8")) if r_book["status"] == 200 else {}
    record_test(
        "backend_workflow",
        "POST /api/workflow/book-call",
        r_book["status"] == 200
        and j_book.get("ok") is True
        and bool(j_book.get("bookingId"))
        and len(j_book.get("onboardingSteps", [])) == 5,
        r_book["status"],
        r_book["latency_ms"],
        {
            "bookingId": j_book.get("bookingId"),
            "workflowId": j_book.get("workflowId"),
            "tier": j_book.get("tier"),
            "amount": j_book.get("amount"),
            "onboardingSteps": len(j_book.get("onboardingSteps", [])),
        },
    )

    # 2g. POST /api/workflow/n8n-10core
    r_n8n = http_request(
        "/api/workflow/n8n-10core",
        method="POST",
        payload={
            "moduleCode": "ALL-10-CORES",
            "moduleName": "Standalone Sovereign n8n 10-Core DAG",
        },
    )
    j_n8n = json.loads(r_n8n["body"].decode("utf-8")) if r_n8n["status"] == 200 else {}
    record_test(
        "backend_workflow",
        "POST /api/workflow/n8n-10core",
        r_n8n["status"] == 200
        and j_n8n.get("ok") is True
        and j_n8n.get("status") == "EXECUTED"
        and j_n8n.get("marginalCost") == "$0.00",
        r_n8n["status"],
        r_n8n["latency_ms"],
        {
            "workflowId": j_n8n.get("workflowId"),
            "orchestrator": j_n8n.get("orchestrator"),
            "moduleCode": j_n8n.get("moduleCode"),
            "marginalCost": j_n8n.get("marginalCost"),
        },
    )

    # 2h. GET /api/sovereign-modules
    r_mods = http_request("/api/sovereign-modules", method="GET")
    j_mods = json.loads(r_mods["body"].decode("utf-8")) if r_mods["status"] == 200 else {}
    record_test(
        "backend_workflow",
        "GET /api/sovereign-modules",
        r_mods["status"] == 200
        and j_mods.get("ok") is True
        and j_mods.get("totalModules") == 10,
        r_mods["status"],
        r_mods["latency_ms"],
        {
            "engine": j_mods.get("engine"),
            "totalModules": j_mods.get("totalModules"),
            "installedModulesCount": len(j_mods.get("installedModulesOnDisk", [])),
        },
    )

    # 2i. GET /api/cyber-verify
    r_cyber = http_request("/api/cyber-verify", method="GET")
    j_cyber = json.loads(r_cyber["body"].decode("utf-8")) if r_cyber["status"] == 200 else {}
    record_test(
        "backend_workflow",
        "GET /api/cyber-verify",
        r_cyber["status"] == 200
        and j_cyber.get("ok") is True
        and j_cyber.get("shield") == "KGU-Cybersecurity-Active"
        and j_cyber.get("notebookLmPurged") is True,
        r_cyber["status"],
        r_cyber["latency_ms"],
        {
            "auditId": j_cyber.get("auditId"),
            "digest": j_cyber.get("digest"),
            "voiceVault": j_cyber.get("voiceVault"),
            "antiScraper": j_cyber.get("antiScraper"),
        },
    )

    # =========================================================================
    # 3. MEDIA ASSET & HTTP 206 PARTIAL CONTENT STREAMING VERIFICATION
    # =========================================================================
    avatar_videos = [
        "/videos/avatar_joann.mp4",
        "/videos/avatar_george.mp4",
        "/videos/avatar_aris.mp4",
        "/videos/avatar_duo.mp4",
    ]
    studio_reels = [
        "/videos/0805_clip1.mp4",
        "/videos/0805_clip2.mp4",
        "/videos/0805_clip3.mp4",
        "/videos/0805_clip4.mp4",
        "/videos/0805_clip5.mp4",
        "/videos/0827_clip1.mp4",
        "/videos/0827_clip2.mp4",
        "/videos/0827_clip3.mp4",
        "/videos/0827_clip4.mp4",
        "/videos/0827_clip5.mp4",
        "/videos/0827_clip6.mp4",
    ]
    episode_videos = [
        "/videos/ep_001_studio.mp4",
        "/videos/ep_002_studio.mp4",
        "/videos/ep_003_studio.mp4",
        "/videos/ep_004_studio.mp4",
        "/videos/ep_005_studio.mp4",
        "/videos/ep_006_studio.mp4",
        "/videos/tec_26_08_05.mp4",
        "/videos/tec_26_08_13.mp4",
        "/videos/tec_26_08_20.mp4",
        "/videos/tec_26_08_27.mp4",
        "/videos/tec_26_09_03.mp4",
        "/videos/tec_26_09_10.mp4",
    ]
    audio_masters = [
        "/audio/tec_26_08_05.mp3",
        "/audio/tec_26_08_13.mp3",
        "/audio/tec_26_08_20.mp3",
        "/audio/tec_26_08_27.mp3",
        "/audio/tec_26_09_03.mp3",
        "/audio/tec_26_09_09.mp3",
        "/audio/tec_26_09_10.mp3",
        "/audio/joann_coffey_ref.wav",
        "/audio/george_dubec_ref.wav",
    ]

    all_media = (
        [("avatar_video_206", p) for p in avatar_videos]
        + [("studio_reel_206", p) for p in studio_reels]
        + [("episode_video_206", p) for p in episode_videos]
        + [("audio_master_206", p) for p in audio_masters]
    )

    for cat, media_path in all_media:
        r_media = http_request(
            media_path,
            method="GET",
            extra_headers={"Range": "bytes=0-1023"},
        )
        content_range = r_media["headers"].get("content-range", "")
        content_type = r_media["headers"].get("content-type", "")
        chunk_len = len(r_media["body"])
        passed_media = (
            r_media["status"] == 206
            and chunk_len == 1024
            and content_range.startswith("bytes 0-1023/")
        )
        total_size = int(content_range.split("/")[-1]) if "/" in content_range else 0
        record_test(
            cat,
            f"GET {media_path} (Range: bytes=0-1023)",
            passed_media,
            r_media["status"],
            r_media["latency_ms"],
            {
                "contentType": content_type,
                "contentRange": content_range,
                "chunkBytes": chunk_len,
                "totalFileSizeBytes": total_size,
            },
        )

    completed_at = datetime.now(timezone.utc).isoformat()
    total_tests = len(tests)
    passed_tests = sum(1 for t in tests if t["passed"])
    failed_tests = total_tests - passed_tests
    pass_rate = round((passed_tests / total_tests) * 100, 2) if total_tests else 0.0
    avg_latency_ms = round(sum(t["latency_ms"] for t in tests) / total_tests, 2) if total_tests else 0.0

    report = {
        "suite": "Tech Unfiltered SI — End-to-End QA & Media Stream Verification",
        "targetServer": BASE_URL,
        "startedAt": started_at,
        "completedAt": completed_at,
        "summary": {
            "totalTests": total_tests,
            "passed": passed_tests,
            "failed": failed_tests,
            "passRatePercent": pass_rate,
            "averageLatencyMs": avg_latency_ms,
            "status": "100% PASS — PRODUCTION VERIFIED" if failed_tests == 0 else "FAILED",
        },
        "categoryBreakdown": {
            cat: {
                "total": sum(1 for t in tests if t["category"] == cat),
                "passed": sum(1 for t in tests if t["category"] == cat and t["passed"]),
            }
            for cat in sorted(set(t["category"] for t in tests))
        },
        "tests": tests,
    }

    with open(REPORT_PATH, "w", encoding="utf-8") as f:
        json.dump(report, f, indent=2)

    print(f"QA Verification Complete: {passed_tests}/{total_tests} passed ({pass_rate}%) | Avg Latency: {avg_latency_ms}ms")
    print(f"Report saved to: {REPORT_PATH}")
    if failed_tests > 0:
        for t in tests:
            if not t["passed"]:
                print(f"  [FAIL] {t['name']} -> status={t['status_code']} details={t['details']}")
        sys.exit(1)


if __name__ == "__main__":
    run_qa_suite()
