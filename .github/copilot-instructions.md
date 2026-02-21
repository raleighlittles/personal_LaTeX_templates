# LaTeX Templates Codebase - AI Agent Instructions

## Project Overview
Personal LaTeX templates repository for creating both LaTeX documents and grid/paper templates for tablet writing apps (Notability, GoodNotes). Supports both US Letter (8.5"×11") and ISO A4 paper sizes.

## Repository Structure

### Template Categories
- **`AssignmentTemplate.tex`**: Standard homework/lab report template with dual header/footer, page numbering (x of y), and 1"×1" logo space
- **`US-Letter/`**: US Letter paper size templates for Notability/GoodNotes
- **`A4/`**: ISO A4 paper size templates for Notability/GoodNotes
- **`build/`**: LaTeX auxiliary files (.aux) - never edit directly
- **`*.tex.bak`**: Backup files created when iterating on templates

### Grid Template Types
1. **EngineeringGrid**: Standard graph paper with minor (0.1") and major (0.5") grid lines
2. **HexagonHoneycomb**: Hexagonal layout for organic chemistry drawings
3. **IsometricGrid**: Isometric 60° grid for technical drawings (uses `\IsoStep` of 0.20")
4. **MizigeGrid**: "Rice-shaped grid" - engineering grid with diagonal lines for Chinese character practice
5. **TianzegeGrid**: "Field-shaped grid" - larger engineering grid for Chinese character practice
6. **RadialLogGrid**: Polar/logarithmic grid with configurable spokes and decade rings

## Critical Conventions

### Paper Size Differentiation
- **US Letter templates**: Use `letterpaper` in geometry package
- **A4 templates**: Use `a4paper` in document class AND geometry package
  ```latex
  \documentclass[11pt, a4paper]{article}
  \usepackage[a4paper, margin=...]{geometry}
  ```

### User-Editable Fields Pattern
All Notability templates define user fields at the top:
```latex
% ===== USER FIELDS =====
\newcommand{\StudentField}{Raleigh Littles}
\newcommand{\CourseField}{Course name}
\newcommand{\TitleField}{Title}
```
Never hardcode these values in the document body.

### Grid Rendering Architecture
All grid templates use this pattern:
- **`eso-pic` package**: Adds TikZ drawings to background on every page via `\AddToShipoutPictureBG`
- **Coordinate system**: `[shift={(current page.south west)}, x=1in, y=1in]` for inch-based positioning
- **Header clearance**: Define `\GridTopOffset` or `\HeaderBandHeight` to prevent grid from overlapping header
- **Clipping**: Always clip the grid region to avoid overflow:
  ```latex
  \clip (0,0) rectangle (\PageW,\YTop);
  ```

### Grid Configuration Variables
Each grid type defines customizable parameters as `\newcommand`:
- **EngineeringGrid**: `\MinorStep`, `\MajorStep`, `\HeaderBandHeight`
- **IsometricGrid**: `\IsoStep`, `\GridTopOffset`, `\IsoOpacity`
- **RadialLogGrid**: `\SpokeStepDeg`, `\BaseRadiusIn`, opacity/width for minor/mid/major lines

## Build Workflow

### Compilation
Standard LaTeX build workflow:
```bash
pdflatex <template-name>.tex
# Output: <template-name>.pdf + build/<template-name>.aux
```

### Output Organization
- PDFs: Generated in same directory as `.tex` file
- Auxiliary files: `.aux` files appear in `build/` subdirectories

### Backup Strategy
- `.tex.bak` files exist for templates under active development
- When modifying templates, consider creating `.bak` before major changes

## Development Patterns

### Creating New Grid Templates
1. Start from existing grid template closest to desired output
2. Define grid parameters as `\newcommand` variables at top (after USER FIELDS)
3. Test grid at different paper sizes - US Letter is 8.5×11, A4 is ~8.27×11.69
4. Adjust `\GridTopOffset` to account for header boxes
5. Use `opacity` values between 0.15-0.45 to prevent overwhelming the writing space

### Modifying Existing Templates
- Always preserve the USER FIELDS section
- Test both US-Letter and A4 versions if changes affect page geometry
- Verify grid alignment by printing/previewing at 100% scale

### Math-Heavy Documents
For assignment templates, the standard math package stack is:
```latex
\usepackage{amsmath}
\usepackage{amssymb}
\usepackage{amsthm}
\usepackage{mathtools}
\usepackage{physics}  % Provides \dd, \dv, \pdv, etc.
\usepackage{siunitx}  % For proper unit formatting
```

## Key Files to Reference

- [AssignmentTemplate.tex](AssignmentTemplate.tex): Example of header/footer setup with `fancyhdr`
- [US-Letter/Notability_Template-EngineeringGrid-USLetter.tex](US-Letter/Notability_Template-EngineeringGrid-USLetter.tex): Cleanest example of TikZ grid with header boxes
- [US-Letter/Notability_Template-RadialLogGrid-USLetter.tex](US-Letter/Notability_Template-RadialLogGrid-USLetter.tex): Complex grid with logarithmic spacing and conditional styling
- [A4/Notability_Template-IsometricGrid-A4.tex](A4/Notability_Template-IsometricGrid-A4.tex): Shows isometric line calculations using `\pgfmathsetmacro`

## Common Pitfalls

- **Don't** use `\input` or `\include` - all templates are self-contained
- **Don't** assume US Letter dimensions for A4 templates - they differ significantly
- **Don't** place grid elements in document body - use `eso-pic` background layer
- **Don't** forget to define page dimensions as variables (`\PageW`, `\PageH`) for calculation clarity
