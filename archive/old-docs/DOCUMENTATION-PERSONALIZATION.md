# Documentation Personalization Enhancement

**Date**: November 2025
**Version**: 2.1
**Enhancement**: Auto-personalize documentation files during project initialization

---

## What Changed

The `init-project.sh` script now **automatically personalizes documentation files** with your project name during initialization.

### Before (v2.0)
- Documentation files remained generic templates
- `README.md` still said "Exonpro Universal App Template"
- `CLAUDE.md` had placeholder text
- Only `requirements.md` and `project.json` were updated

### After (v2.1)
- All documentation files are personalized immediately
- Project name appears throughout docs
- Title Case conversion for better readability
- Initialization timestamp added to WHATS-NEW.md

---

## Files That Get Personalized

| File | What Gets Updated |
|------|------------------|
| **README.md** | Title, project references, folder names |
| **CLAUDE.md** | Project name, context, references |
| **START_HERE.md** | Project name throughout |
| **QUICK-REFERENCE.md** | Title, all references |
| **WHATS-NEW.md** | Adds project header with init date |
| **.exon/constitution.md** | Project name, context |
| **requirements.md** | Project name in title (existing) |
| **aws-config.json** | Project name in config (existing) |

---

## How It Works

### 1. Name Conversion

The script converts your project name to Title Case for better readability:

```bash
# Input
hrms-python-serverless

# Output (in docs)
Hrms Python Serverless
```

**Examples:**
- `todo-app` → "Todo App"
- `my-saas-platform` → "My Saas Platform"
- `employee_management` → "Employee Management"

### 2. Smart Replacement

The script uses `sed` to replace placeholders and generic text:

**README.md:**
```markdown
# Exonpro Universal App Template
```
Becomes:
```markdown
# Hrms Python Serverless
```

**CLAUDE.md:**
```markdown
Project: [Project Name]
```
Becomes:
```markdown
Project: Hrms Python Serverless
```

**QUICK-REFERENCE.md:**
```markdown
# Exonpro Template - Quick Reference Guide
```
Becomes:
```markdown
# Hrms Python Serverless - Quick Reference
```

### 3. Timestamp Addition

**WHATS-NEW.md** gets a project-specific header:

```markdown
# Hrms Python Serverless - What's New

**Project**: hrms-python-serverless
**Initialized**: November 01, 2025

---

# What's New in Exonpro Template
... (rest of original content)
```

---

## When Personalization Happens

Documentation personalization occurs during the init-project.sh script execution:

```
1. Copy template files                     ✅
2. Clean up template-specific content      ✅
3. Reset state.json                        ✅
4. Update project.json with project name   ✅
5. Initialize git repository               ✅
6. Create requirements.md                  ✅
7. Create aws-config.json                  ✅
8. 🆕 PERSONALIZE DOCUMENTATION FILES      ✅ NEW!
9. Create initial git commit               ✅
10. Print next steps                       ✅
```

---

## Example: Creating "hrms-python-serverless"

### Command:
```bash
./init-project.sh hrms-python-serverless ~/projects
```

### Result:

#### README.md (First line):
```markdown
# Hrms Python Serverless
```

#### CLAUDE.md:
```markdown
# Development Guide: Hrms Python Serverless

This project (hrms-python-serverless) follows Exonpro standards...
```

#### QUICK-REFERENCE.md:
```markdown
# Hrms Python Serverless - Quick Reference

This guide provides quick access to common commands for hrms-python-serverless.
```

#### WHATS-NEW.md:
```markdown
# Hrms Python Serverless - What's New

**Project**: hrms-python-serverless
**Initialized**: November 01, 2025

---

# What's New in Exonpro Template
... (original template changelog continues)
```

---

## Benefits

### 1. Immediate Project Identity
✅ No confusion about which project you're working on
✅ Professional appearance from day one
✅ Clear project context for team members

### 2. Better Developer Experience
✅ Documentation feels specific, not generic
✅ Easier to share docs with stakeholders
✅ No manual find-and-replace needed

### 3. Consistency
✅ Project name consistent across all files
✅ Follows naming conventions automatically
✅ Title Case formatting for readability

### 4. Time Savings
✅ No need to manually update each doc file
✅ One command personalizes everything
✅ Ready to use immediately after init

---

## What Remains Generic

Some content intentionally remains generic until the builder runs:

**Will be updated by Phase 0-5:**
- Tech stack details (Python vs Node.js)
- Architecture specifics
- API documentation
- Deployment instructions
- Feature lists

**These are placeholders until builder analyzes requirements:**
```json
{
  "stack_template": "{{STACK_TEMPLATE}}",
  "hosting": "{{HOSTING}}",
  "frontend": "{{FRONTEND}}",
  "backend": "{{BACKEND}}"
}
```

---

## Testing the Enhancement

### Create a Test Project:

```bash
cd /Users/kusaldipdas/Documents/00_All_Work/exon-template

./init-project.sh test-personalization /tmp
cd /tmp/test-personalization
```

### Verify Personalization:

```bash
# Check README title
head -1 README.md
# Expected: # Test Personalization

# Check CLAUDE.md
grep "test-personalization" CLAUDE.md
# Should find multiple matches

# Check QUICK-REFERENCE
head -1 QUICK-REFERENCE.md
# Expected: # Test Personalization - Quick Reference

# Check WHATS-NEW header
head -6 WHATS-NEW.md
# Should show project name and init date
```

### Cleanup:
```bash
rm -rf /tmp/test-personalization
```

---

## Migration: Updating Existing Projects

If you have projects created with the old init script (before v2.1), you can personalize them manually:

```bash
cd your-project

# Set project name
PROJECT_NAME="your-project"
PROJECT_TITLE="Your Project"  # Title Case

# Update README
sed -i '' "1s/.*/# $PROJECT_TITLE/" README.md
sed -i '' "s/Exonpro Universal App Template/$PROJECT_TITLE/g" README.md

# Update CLAUDE.md
sed -i '' "s/\[Project Name\]/$PROJECT_TITLE/g" CLAUDE.md

# Update QUICK-REFERENCE.md
sed -i '' "1s/.*/#  $PROJECT_TITLE - Quick Reference/" QUICK-REFERENCE.md
```

---

## Technical Details

### Sed Commands Used

**macOS (BSD sed):**
```bash
sed -i '' 's/pattern/replacement/g' file.md
```

**Linux (GNU sed):**
```bash
sed -i 's/pattern/replacement/g' file.md
```

The script detects OS and uses the correct syntax automatically.

### Title Case Conversion

```bash
PROJECT_TITLE=$(echo "$PROJECT_NAME" | sed 's/-/ /g' | awk '{for(i=1;i<=NF;i++) $i=toupper(substr($i,1,1)) tolower(substr($i,2));}1')
```

**How it works:**
1. Replace hyphens with spaces: `hrms-python` → `hrms python`
2. Capitalize first letter of each word
3. Lowercase the rest: `Hrms Python`

---

## Answering Your Question

> "when i check individual project's md files like claude.md they are still copied version of template is this correct when the documents will be updated as per the each projects objective?"

### Before This Enhancement:
**Answer:** YES, it was correct. Documentation remained generic until Phase 1-5 of the builder.

### After This Enhancement (v2.1):
**Answer:** NO, they will now be personalized with your project name immediately!

**However:**
- Detailed content (features, architecture, APIs) still updates during builder phases
- Only **project name and references** are personalized during init
- **Full customization** happens when the builder analyzes your `requirements.md`

---

## Future Enhancements

Potential future improvements:

### v2.2 (Planned):
- [ ] Extract project description from requirements.md
- [ ] Auto-update README overview section
- [ ] Generate project-specific badges
- [ ] Create custom .github/ISSUE_TEMPLATE

### v3.0 (Future):
- [ ] AI-powered documentation generation during init
- [ ] Custom branding/logo support
- [ ] Multi-language documentation
- [ ] Auto-generated API documentation stubs

---

## Rollback

If you need to revert to generic templates:

```bash
cd your-project

# Copy fresh template files
cp /path/to/exon-template/README.md ./
cp /path/to/exon-template/CLAUDE.md ./
cp /path/to/exon-template/START_HERE.md ./
```

---

## Conclusion

**Now when you initialize a project, you get:**

✅ Personalized README with your project name
✅ Customized CLAUDE.md with project context
✅ Updated QUICK-REFERENCE for your project
✅ Timestamped WHATS-NEW header
✅ Consistent project name across all docs
✅ Professional appearance from day one

**No more generic "Exonpro Universal App Template" in your project docs!**

---

**Version History:**

| Version | Date | Changes |
|---------|------|---------|
| 2.0 | Nov 2025 | Added dev scripts, URL management, documentation |
| 2.1 | Nov 2025 | Added automatic documentation personalization |

---

**Built with ❤️ by Exonpro**
