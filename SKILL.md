---
name: it-project-docs
title: IT Project Documentation Generator
description: Generate project documentation templates and fill content for software development projects
version: 1.0.0
author: Claude
category: documentation
tags: [documentation, project-management, software-development, templates]
---

# IT Project Documentation Generator

A skill for generating and managing documentation for IT software development projects. This skill provides comprehensive templates for all project stages from initiation to deployment.

## Capabilities

- **Project Structure Creation**: Create organized project documentation structures
- **Template Generation**: Generate documentation templates based on project type
- **Smart Content Filling**: Interactive template filling with variable substitution
- **Document Tracking**: Track completion status of all documents
- **Document Export**: Export documentation packages in multiple formats
- **Template Validation**: Validate template structure and consistency

## Usage

### Create a New Project

```
python scripts/create_project.py "my-project" --type web-app --tech-stack "React,Node.js,PostgreSQL"
```

### Generate a Document Template

```
python scripts/generate_template.py "需求规格说明书" --project "data/projects/my-project"
```

### Fill Template Variables

```
python scripts/fill_template.py "data/projects/my-project/02-需求/需求规格说明书.md"
```

### List Available Documents

```
python scripts/list_documents.py --category requirements
```

### Track Document Status

```
python scripts/track_status.py --project "data/projects/my-project" --report
```

### Export Documentation Package

```
python scripts/export_bundle.py --project "data/projects/my-project" --format zip
```

## Project Types

- `web-app` - Web Applications
- `mobile-app` - Mobile Applications
- `desktop-app` - Desktop Applications
- `api-service` - API Services
- `data-platform` - Data Platforms

## Document Stages

1. **Initiation** (立项) - Project proposals, feasibility studies, charters
2. **Requirements** (需求) - SRS, BRD, user stories
3. **Design** (设计) - Architecture, database, interface design
4. **Development** (开发) - Technical specifications, coding standards
5. **Testing** (测试) - Test plans, test cases, test reports
6. **Deployment** (部署) - Deployment guides, user manuals, operations guides
7. **Management** (管理) - Project plans, risk management, reports

## Configuration

All configuration is stored in `data/config/`:
- `document_catalog.json` - Document type definitions
- `variable_registry.json` - Template variable definitions
- `project_metadata.json` - Project metadata template

## Output Format

All documents are generated in Markdown format with:
- YAML frontmatter for metadata
- Variable placeholders for easy filling
- Clear section structure
- Writing guidance comments
