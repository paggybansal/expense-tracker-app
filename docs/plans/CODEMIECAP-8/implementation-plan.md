# Implementation Plan

## Overview
- **Story/Sub-task:** CODEMIECAP-8 — Implement Dashboard Monthly Summary Cards + CSV Export (with empty-state) and Title/Description mapping
- **Parent story:** CODEMIECAP-6 — Implement Monthly Expense Export (CSV/PDF) and Filterable Summary Dashboard Cards
- **Goal:** Add monthly dashboard summary metrics and CSV export that matches the current filtered view,   including an empty-state message, while mapping CSV **Title** from the existing `description` field.
- **Jira::* https://paragbansalbansal.atlassian.net/browse/CODEMIECAP-8

## Scope
### In scope
- AC-1: Render 3 monthly summary metric cards: Total Monthly Spent, Top Category, Average Daily Spend.
- AC-2: Provide an “Export to CSV” action that exports the current view (same filters/sort) with columns **ID, Title, Category, Amount, Date**.