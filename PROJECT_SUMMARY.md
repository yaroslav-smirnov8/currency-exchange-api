# Project Summary (Plain English)

This project is a small web service that gives currency exchange rates and converts amounts between currencies. It is built so websites, widgets, or internal tools can request rates without dealing with provider-specific APIs.

# Problem Statement

Teams often need exchange rates for pricing, reporting, or widgets. Provider APIs vary, and clients must handle errors, timeouts, and different response formats. This creates duplicated logic and inconsistent behavior across products.

# Solution Approach

I built a single REST API that standardizes rate access and conversion. It validates inputs, wraps provider errors into a consistent JSON format, and supports both a real provider and a mock provider for local development.

# My Role

- Designed the architecture and request flow
- Implemented routing, middleware, and service layers
- Integrated the external provider and created a mock provider for tests
- Wrote test coverage for business logic and HTTP endpoints
- Documented setup, configuration, and usage for developers

# Technical Complexity

- Managed async I/O with aiohttp to keep provider calls fast
- Built a provider abstraction to allow swapping data sources
- Balanced simplicity and reliability by keeping the API stateless
- Chose not to add storage to avoid stale data and extra ops overhead

# Business / User Value

- Faster integration for frontend teams and partners
- Consistent behavior across products that need currency conversion
- Lower maintenance cost by centralizing validation and error handling

# Quality Signals

- Unit and integration tests with passing green status
- Clear module boundaries: routes, services, providers, settings
- Environment-based configuration for safe deployments
- Stateless design that scales horizontally behind a load balancer
