# Implementation Plan — CODEMIECAP-3

_*+Jira:** CODEMIECAP-3 (Subtask under CODEMIECAP-1)

_**Summary:** Add a Category filter dropdown on the dashboard and implement server-side filtering via a `category` query parameter on the index route.

## 1. Scope

### In scope
- Support optional `?category=<value>` query param on the dashboard route (`/`).