# djvu_outliner

Add outlines (bookmarks) to DJVU files from a plain-text input file.

## Input file format

The input file contains hierarchical entries with page numbers. Indentation determines nesting level — entries at the same indent level are siblings, deeper indentation creates children.

```
Chapter 1 Title 1
    1.1 Section Title 10
    1.2 Another Section 20
        1.2.1 Subsection 25
    1.3 More 30
    References 35
```

### `#SHIFT` directive

Use `#SHIFT <offset>` to adjust page numbers when the source document's page numbering doesn't start at 1 (e.g., front matter in Roman numerals). The offset is added to every page number that follows it. You can change the shift mid-file.

```
Cover 3
#SHIFT 12
Chapter 1 Chapter 1 1     → actual page 1 + 12 = #13
    1.1 Section 10         → actual page 10 + 12 = #22
```

Negative shifts are also supported:

```
#SHIFT -2
Cover 3                    → actual page 3 - 2 = #1
```

### Empty lines and comments

- Lines starting with `#` (other than `#SHIFT`) are treated as comments and ignored.
- Blank lines are also ignored.

## Installation

```bash
pip install .
```

Or install with [pixi](https://pixi.sh):

```bash
pixi install
```

## Usage

### 1. Create an input file

Write your outline in the format above and save it as a text file (e.g., `examples/example_in.txt`).

### 2. Generate the DJVU outline file

```bash
py-djvu-outliner -i examples/example_in.txt -o examples/example_out.txt
```

This produces a S-expression file in DJVU bookmark format.

### 3. Apply the outline to a DJVU document

```bash
djvused -s -e "set-outline examples/example_out.txt" file.djvu
```

The `djvused` tool is part of [DjVuLibre](https://djvu.sourceforge.net/).

## Example

Given `examples/example_in.txt`:

```
#SHIFT -2
Cover 3
Contents 7
Introduction 11
#SHIFT 12
Chapter 1 Chapter 1 1
    1.1 Sub Chapter 1.1 10
    1.2 Sub Chapter 1.2 20
    References 30
#SHIFT 8
Chapter 2 Chapter 2 35
    2.1 Sub Chapter 2.1 40
    2.2 Sub Chapter 2.2 50
    References 60
Index 65
```

Running:

```bash
py-djvu-outliner -i examples/example_in.txt -o examples/example_out.txt
```

Produces `examples/example_out.txt`:

```
(bookmarks
  ("Cover" "#1")

  ("Contents" "#5")

  ("Introduction" "#9")

  ("Chapter 1 Chapter 1" "#13"
    ("1.1 Sub Chapter 1.1" "#22")
    ("1.2 Sub Chapter 1.2" "#32")
    ("References" "#42")
  )

  ("Chapter 2 Chapter 2" "#43"
    ("2.1 Sub Chapter 2.1" "#48")
    ("2.2 Sub Chapter 2.2" "#58")
    ("References" "#68")
  )

  ("Index" "#73")

)
```

Then apply it to your DJVU file:

```bash
djvused -s -e "set-outline examples/example_out.txt" file.djvu
```
