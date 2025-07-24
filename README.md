# FCC Data Model - README

## Overview

This document describes the data modeling exercise for the FCC written exam, including the core entities, their relationships, and the transformation of existing tables into new consolidated tables.

---

## Entities and Relationships

### Tables

- dim_user  
  - This dimension table represents users, consolidated from `user_registration` and `user` tables.  
  - Contains user profile and registration details.

- fact_play_session  
  - This fact table captures user play sessions, merged from `user_play_session`, `play_session_status_code`, and `play_session_channel_code`.  
  - Tracks session events along with status and channel metadata.

- dim_plan  
  - Dimension table representing subscription plans, created by combining `plan` and `payment_frequency` tables.  
  - Includes plan details and frequency of payment.

- fact_user_plan  
  - Fact table that captures user-plan relationships, derived from `user_plan` and `user_payment_detail`.  
  - Records user subscriptions and payment details.

---

## Relationships and Cardinality

- dim_user (1) : (N) fact_play_session  
  - Each user can have multiple play sessions.

- dim_user (1) : (N) fact_user_plan  
  - Each user can have multiple subscription plans over time.

- dim_plan (1) : (N) fact_user_plan  
  - Each plan can be subscribed to by multiple users.

---
