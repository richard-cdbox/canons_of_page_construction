# canons_of_page_construction
This Scribus script draws classical and modern page-construction canons directly into a Scribus document and automatically computes correct margins for left and right master pages. All constructions are drawn on a dedicated outlined layer on the appropriate pages (facing or single), and margins are applied with proper inside/outside mirroring.

---

**NOTE:** Before using the script, please read section [Important note about Scribus API limitation](#important-note-about-scribus-api-limitation).

---

**Author:** Richard Sitányi (richard@cdbox.sk)

**File:** canons_of_page_construction.py

**Version:** 1.0

**Date:** 11/19/2025

---

## Supported canons

### **1. Van de Graaf canon**
A classical Renaissance canon based on diagonal intersections of a full spread. The text area is constructed using geometric intersection points. This system ensures that the text block has the same proportions as the page, creating a visually balanced layout.

### **2. Interpretation of Rosarivo**
The resulting page layout of this system is the same as in Van de Graaf’s canon, however, the creation process is different. The page is divided into a nine-by-nine grid. This divides the width and height of the page into thirds. The intersections of the grid with the diagonals give us the key points of the text block.

### **3. Golden rectangle (facing pages)**
The entire spread is turned into a large golden rectangle. Two smaller golden rectangles representing left and right text blocks are placed inside it. The whole construction can be uniformly scaled to adjust white space.

### **4. Golden rectangle (single page)**
A single-page variant where the golden rectangle is centered directly on the page.

### **5. Golden ratio**
A spread-based golden ratio layout. The user selects the inside margin, while all other margins follow from the golden ratio φ. Creates a highly elegant, tightly balanced page layout.

### **6. Fibonacci 2:3:5:8**
A layout derived from Fibonacci relationships. Margins follow Fibonacci-based ratios, creating an organic and naturally balanced composition. Useful for expressive, non-mechanical layouts.

### **7. 2:3:4:6**
A proportional canon based on the relationships 2:3:4:6. Margins are derived from simple proportional rules. Results in a highly predictable and structurally clean page layout.

### **8. Page ratio canon**
Margins are derived directly from the page’s aspect ratio (height/width). The text block reflects the same ratio as the physical page, creating a geometric and unified layout.

---

## Features
- Interactive GUI: paper size, canon selection, scaling, and adjustable margin parameters
- Draws construction lines and helper rectangles on their own layer
- Creates left and right master pages automatically
- Correct inside/outside mirroring for all facing-page canons
- Works with a wide library of predefined page sizes
- Clean separation of construction layers and content layers

---

## Requirements
- Scribus v1.6.4 or v1.7.0 with Python scripting enabled
- Run via **Script → Execute Script**

---

## Usage notes
- After execution, the script draws the geometric construction on a dedicated outlined layer.
- Master pages are generated automatically and applied to all pages.
- For canons using scaling (golden rectangle), recommended scale range is 80–85%.  

---

## Important note about Scribus API limitation

Scribus currently provides only *getPageType()* but not *setPageType()* or any way to assign *Left* master or normal page types through the scripting API. This means:

- All master pages created by this script are initially marked as *Right*.
- Margin mirroring **does work correctly**, however, Scribus does not automatically update the master-page type.

### What you should do manually (once after running the script)

1. Open **Edit → Master Pages**
2. Select *left* master page (e.g., *Van de Graaf left*)
3. Set **Type = Left Page** in **Page → Manage Page Properties**

Once this is done, Scribus will:
- interpret margin values correctly,
- mirror them internally,
- remove preflight warnings,
- export pages to PDF with correct inside/outside margins.

This is a known Scribus API limitation and has been reported in the issue tracker, but as of now (2025) it is not yet implemented.


