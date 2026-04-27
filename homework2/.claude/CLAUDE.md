# Core Philosophy

Write code that is **simple, maintainable, and production-ready**. Prioritize clarity over cleverness, and always leave the codebase cleaner than you found it.

## Key Principles

1. **Simplicity First**: Always choose the simplest solution that satisfies the requirements. Avoid over-engineering. (KISS principle)
2. **Consistency**: Keep the existing tech stack unless there is a clear, justified technical reason to introduce something new.
3. **Maintainability**: Write code that is easy to read and understand. Prefer explicit, self-explanatory code over clever or compact solutions.
4. **Scalability**: Structure code to support future growth, but do not optimize prematurely — only when there is a demonstrated need.
5. **Best Practices**: Follow established patterns, idioms, and conventions of the language and framework in use.
6. **Clean Architecture**: Apply SOLID principles. Keep concerns separated — business logic, data access, and presentation should not be mixed.
7. **Quality First**: Refactoring and code cleanup are part of the work, not optional extras. Leave code cleaner than you found it.

## Constraints

- **Never run `git` commands** (commit, push, stage, reset, etc.) unless explicitly instructed to do so in the current task.
- **Do not install new dependencies** to fix bugs. Find a solution using what is already available in the project.
- **Keep bug fixes minimal and focused** — prefer short, clean, targeted changes over broad rewrites.

## Code Quality Standards

### SOLID Principles (Non-negotiable)

- **Single Responsibility**: Each class/function has exactly one reason to change
- **Open/Closed**: Open for extension, closed for modification
- **Liskov Substitution**: Subtypes must be substitutable for their base types
- **Interface Segregation**: Many specific interfaces beat one general-purpose interface
- **Dependency Inversion**: Depend on abstractions, not concrete implementations

### Clean Code Practices

**Code Organization:**

- Keep functions small (< 20 lines ideally, < 100 lines maximum)
- One level of abstraction per function
- Use meaningful, pronounceable names (avoid abbreviations unless widely known)
- Self-documenting code is the goal; comments explain "why", not "what"

**Code Quality:**

- **DRY Principle**: Don't Repeat Yourself - eliminate duplication through abstraction
- **YAGNI**: You Aren't Gonna Need It - don't add features speculatively
- Write code that's easy to delete, not easy to extend
- Prefer composition over inheritance

**Error Handling:**

- Fail fast and explicitly
- Use typed errors/exceptions with clear messages
- Never silently ignore errors
- Validate inputs at system boundaries

## Development Workflow

### Before Writing Code
1. Understand the requirement completely - ask clarifying questions if needed

2. Identify impacted areas of the codebase
3. Plan the simplest approach that satisfies requirements

### While Writing Code

1. **Write clean code from the start** - don't plan to "clean it up later"
2. **Test as you go** - verify changes work before moving on
3. **Refactor continuously** - improve code structure immediately when you see issues

### After Writing Code

1. **Review and update comments** - ensure they reflect current implementation
2. **Clean up imports** - remove unused dependencies
3. **Verify tests pass** - run existing tests and add new ones if needed
4. **Check for side effects** - ensure changes don't break other functionality

## Technology Stack

### Frontend & UI

**JavaScript/TypeScript:**

- Package Manager: `yarn`
- styling: LESS 
- Type Safety: TypeScript with strict mode enabled (compiled via Babel)
- Webpack 5 as the bundler
- jQuery + Select2
- Highcharts for data visualization/charts
- Leaflet + Mapbox GL for maps
- Ant Design (antd) UI component library
- React 16 with Redux (+ redux-thunk, redux-persist) - used only in very specific cases not prefered

### Backend

**PHP:**

- PHP with the Phalcon framework (v5) 
- Symfony components (Mailer, HTTP Client)
- PDO for database access
- Memcached for caching, APCu for in-memory cache (this one will be replaced soon)
- mPDF for PDF generation
- Sentry for error tracking (PHP side)
- Prometheus client for metrics
- Type Hints: Use type annotations consistently (Phalcon v5 syntax)

### AI & Machine Learning

**Agent Development:**

- **Preferred**: Claude Agent SDK (https://docs.claude.com/en/docs/agent-sdk/overview)
- **Alternative**: Codex SDK (https://developers.openai.com/codex/sdk/)
- Keep agent chains simple and debuggable

### Infrastructure & DevOps

**Containerization:**

- Docker for local development and production
- Multi-stage builds for minimal image sizes
- .dockerignore to exclude unnecessary files

**Orchestration:**

- Kubernetes via Google Kubernetes Engine (GKE)
- Keep manifests DRY and well-documented

**Infrastructure as Code:**

- Use modules for reusability

## Code Review Checklist

Before considering code complete, verify:

### General review
- [ ] All unused code removed (functions, variables, imports, comments)
- [ ] Comments updated to reflect current implementation
- [ ] No code duplication (DRY principle applied)
- [ ] Functions are small and focused (single responsibility)
- [ ] Error handling is explicit and comprehensive
- [ ] Type safety maintained (TypeScript/Python type hints)
- [ ] Tests written/updated and passing
- [ ] No hardcoded values (use configuration/environment variables)
- [ ] Security best practices followed (no secrets in code, input validation, etc.)
- [ ] Performance considered (no obvious bottlenecks)

### Frontend review

- [ ] All UI components render correctly in dark mode (colors, contrast, borders, icons, and text are visible and properly styled)
- [ ] Layout and text display correctly for RTL (right-to-left) languages such as Arabic — including text alignment, element order, and spacing
- [ ] Pages in edited files are correctly formatted for print — margins, page breaks, font sizes, and hidden elements behave as expected when printing or exporting to PDF
- [ ] UI appearance and functionality is consistent across all supported locales and languages — no layout breaks, missing translations, or locale-specific formatting issues

## Communication Guidelines

**Context:**

- Assume 20+ years of software engineering experience
- Skip basic explanations unless specifically requested
- Be direct and technical in communication
- Ask for clarification when requirements are ambiguous

**Code Explanations:**

- Focus on "why" decisions were made, not "what" the code does
- Highlight tradeoffs and alternatives considered
- Point out areas that may need future attention

## Anti-Patterns to Avoid

- ❌ Leaving commented-out code "just in case"
- ❌ Adding TODO comments 
- ❌ Copying and pasting code instead of abstracting
- ❌ Premature optimization
- ❌ Over-engineering simple solutions
- ❌ Ignoring compiler/linter warnings
- ❌ Writing code without understanding its purpose
- ❌ Implementing features "we might need someday"

## Remember

> "Code is read far more often than it is written." - Guido van Rossum

> "Any fool can write code that a computer can understand. Good programmers write code that humans can understand." - Martin Fowler

Write code you'd be proud to maintain in 2 years.

