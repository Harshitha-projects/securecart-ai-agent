SecureCart AI — Secure Agentic Commerce Platform

Project Overview

SecureCart AI is a Python-based agentic commerce platform designed to integrate AI shopping agents with secure Model Context Protocol (MCP) services.

The platform is designed to enable AI agents to discover products, check inventory, manage shopping carts, and initiate order workflows through authenticated, server-enforced tools.

Key Features

AI Agent Integration: Claude API integration for natural-language shopping requests and tool calling.

MCP Server: Model Context Protocol tools exposed through Streamable HTTP.

Authentication: JWT validation using trusted JWKS endpoints and OAuth 2.0 authorization scopes.

Secure Tool Execution: Server-side identity checks and permission enforcement.

Commerce Integration: Product search, inventory checks, cart management, and order workflows.

Asynchronous Processing: Python asyncio and HTTPX for non-blocking API operations.

Reliability: Structured logging, timeout handling, error responses, and idempotent checkout requests.

Automated Testing: Pytest for API, agent workflow, and security tests.

Technology Stack

Python, FastAPI, MCP Python SDK, Claude API, asyncio, HTTPX, PostgreSQL, SQLAlchemy, JWT, JWKS, OAuth 2.0, Pytest, Ruff, Docker, and GitHub Actions.

System Architecture

Customer Request → Claude Agent → Secure MCP Server → Authentication & Authorization → Commerce APIs → PostgreSQL

Security Design

The platform is designed to enforce authentication and authorization on the server rather than trusting instructions from an AI model.

Sensitive operations, including order submission, require valid identity, appropriate scopes, and explicit user confirmation.

Getting Started

Installation and execution instructions will be added after implementation and verification.

Testing

Automated tests will cover authentication, authorization, MCP tool execution, API integrations, and order workflows.

Project Status

Architecture and implementation planning.

Disclaimer

This is an independent portfolio project using simulated commerce data. It is not affiliated with a commercial retailer and does not process real payments.
