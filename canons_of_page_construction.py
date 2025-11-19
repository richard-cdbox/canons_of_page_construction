#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Author: Richard Sitányi (richard@cdbox.sk)
File: canons_of_page_construction.py
Version: 1.0
Date: 11/19/2025
"""

import sys
import tkinter as tk
from tkinter import ttk

try:
    import scribus
except ImportError:
    print("This script must be run from inside Scribus.")
    sys.exit(1)


# PAPER SIZES (mm)
papers = {
    "A2": (420, 594),
    "A3": (297, 420),
    "A4": (210, 297),
    "B2": (500, 707),
    "B3": (353, 500),
    "B4": (250, 353),
    "C2": (458, 648),
    "C3": (324, 458),
    "C4": (229, 324),
    "D2": (380, 528),
    "D3": (264, 375),
    "D4": (188, 260),
    "DIN D2": (385, 545),
    "DIN D3": (272, 385),
    "DIN D4": (192, 272),
    "F2": (420, 660),
    "F3": (330, 420),
    "F4": (210, 330),
    "JB2": (515, 728),
    "JB3": (364, 515),
    "JB4": (257, 364),
    "P2": (430, 560),
    "P3": (280, 430),
    "P4": (215, 280),
    "PA2": (420, 560),
    "PA3": (280, 420),
    "PA4": (210, 280),
    "RD2": (393, 546),
    "RD3": (273, 393),
    "RD4": (196, 273),
    "SIS D2": (545, 771),
    "SIS D3": (386, 545),
    "SIS D4": (273, 386),
    "SIS E2": (439, 621),
    "SIS E3": (310, 439),
    "SIS E4": (220, 310),
    "SIS F2": (479, 677),
    "SIS F3": (339, 479),
    "SIS F4": (239, 339),
    "SIS G2": (522, 738),
    "SIS G3": (369, 522),
    "SIS G4": (261, 369),
    "Letter": (215.9, 279.4),
    "Legal": (215.9, 355.6),
    "Ledger": (279.4, 431.8),
    "Folio": (304.8, 482.6),
    "Executive": (184.15, 266.7),
    "4to (Quarto)": (241.3, 304.8),
    "8vo (Imperial Octavo)": (209.55, 292.1),
    "Kiku 4": (227, 306),
    "Shiroku ban 4": (264, 379),
    "Crown": (381, 508),
    "Demy": (444.5, 571.5),
    "Foolscap": (203.2, 330.2),
    "Large Post": (419.1, 533.4),
    "Medium": (457.2, 584.2),
    "Post": (393.7, 488.95),
    "Quarto": (203.2, 254),
    "Royal": (508, 635),
}

canons = ("Van de Graaf canon", "Interpretation of Rosarivo", "Golden rectangle (facing pages)", "Golden rectangle (single page)", "Golden ratio", "Fibonacci 2:3:5:8", "2:3:4:6", "Page ratio canon")


# BASIC HELPERS
def mm():
    try:
        scribus.setUnit(scribus.UNIT_MM)
    except:
        pass


def new_layer(name):
    if name not in scribus.getLayers():
        scribus.createLayer(name)
    scribus.setActiveLayer(name)


def draw_line(x1, y1, x2, y2):
    scribus.gotoPage(2)
    scribus.createLine(x1, y1, x2, y2)


def ensure_color(name, c, m, y, k):
    if name not in scribus.getColorNames():
        scribus.defineColorCMYKFloat(name, c, m, y, k)


# Compute intersection point of segments AB and CD
def seg_intersection(A, B, C, D):
    (xA, yA), (xB, yB) = A, B
    (xC, yC), (xD, yD) = C, D
    den = (xB - xA) * (yD - yC) - (yB - yA) * (xD - xC)
    if abs(den) < 1e-9:
        return None
    t = ((xC - xA) * (yD - yC) - (yC - yA) * (xD - xC)) / den
    x = xA + t * (xB - xA)
    y = yA + t * (yB - yA)
    return (x, y)


# DOCUMENT CREATION
def create_new_doc_facing_pages(paper_name):
    mm()
    w, h = papers[paper_name]
    number_of_pages = 3
    scribus.newDocument((w, h), (0, 0, 0, 0), scribus.PORTRAIT, 1, scribus.UNIT_MM, scribus.PAGE_2, 1, number_of_pages)
    return w, h

def create_new_doc_single_page(paper_name):
    mm()
    w, h = papers[paper_name]
    number_of_pages = 1
    scribus.newDocument((w, h), (0, 0, 0, 0), scribus.PORTRAIT, 1, scribus.UNIT_MM, scribus.PAGE_1, 1, number_of_pages)
    return w, h


# VAN DE GRAAF CANON
def draw_vandegraaf(paper_name):
    mm()
    new_layer("Van de Graaf construction")
    alayer = scribus.getActiveLayer()
    W, H = papers[paper_name]

    A = (0, 0)
    B = (W, 0)
    C = (2*W, 0)
    D = (2*W, H)
    F = (0, H)

    draw_line(A[0], A[1], D[0], D[1])
    draw_line(F[0], F[1], C[0], C[1])
    draw_line(F[0], F[1], B[0], B[1])
    draw_line(B[0], B[1], D[0], D[1])

    long_diag = (F, C)
    short_right = (B, D)
    short_left  = (F, B)

    P1 = seg_intersection(long_diag[0], long_diag[1], short_right[0], short_right[1])
    P2 = (P1[0], 0)
    mirror_P1 = (P1[0] - (2 * (P1[0] - W)), P1[1])
    P3 = seg_intersection(short_right[0], short_right[1], P2, mirror_P1)
    P4 = seg_intersection(long_diag[0], long_diag[1], (P3[0], P3[1]), (2 * W, P3[1]))
    P5 = seg_intersection(short_right[0], short_right[1], (P4[0], 0), (P4[0], H))

    draw_line(P2[0], P2[1], P1[0], P1[1])
    draw_line(P2[0], P2[1], mirror_P1[0], mirror_P1[1])

    B_width = P4[0] - P3[0]
    A_height = P5[1] - P4[1]

    ensure_color("GR_grey", 0, 0, 0, 20)

    grey_rect = scribus.createRect(P3[0], P3[1], B_width, A_height)
    scribus.setFillColor("GR_grey", grey_rect)
    scribus.setLineColor("None", grey_rect)

    scribus.setLayerOutlined(alayer, True)
    scribus.setActiveLayer("Background")

    left = P3[0] - W
    right = 2 * left 
    top = P3[1]
    bottom = H - P5[1]

    return left, right, top, bottom


# INTERPRETATION OF ROSARIVO
def draw_rosarivo(paper_name):
    mm()
    new_layer("Rosarivo construction")
    alayer = scribus.getActiveLayer()
    W, H = papers[paper_name]

    A = (0, 0)
    B = (W, 0)
    C = (2*W, 0)
    D = (2*W, H)
    F = (0, H)

    draw_line(A[0], A[1], D[0], D[1])
    draw_line(F[0], F[1], C[0], C[1])
    draw_line(F[0], F[1], B[0], B[1])
    draw_line(B[0], B[1], D[0], D[1])

    Grey_x = abs(W/9)
    Grey_y = H/9

    B_width = W - (Grey_x + 2 * Grey_x)
    A_height = H - (Grey_y + 2 * Grey_y)

    scribus.gotoPage(3)

    scribus.setColumnGuides(8, gap=0.0, refer_to=0)
    scribus.setRowGuides(8, gap=0.0, refer_to=0)

    ensure_color("GR_grey", 0, 0, 0, 20)

    grey_rect = scribus.createRect(Grey_x, Grey_y, B_width, A_height)
    scribus.setFillColor("GR_grey", grey_rect)
    scribus.setLineColor("None", grey_rect)

    scribus.setLayerOutlined(alayer, True)
    scribus.setActiveLayer("Background")

    left = Grey_x
    right = 2 * left
    top = Grey_y
    bottom = 2 * top

    return left, right, top, bottom


# GOLDEN RECTANGLE (FACING PAGES)
def draw_golden_rectangle_facing_pages(paper_name, scale):
    mm()
    new_layer("Golden rectangle (facing pages) construction")
    alayer = scribus.getActiveLayer()

    W, H = papers[paper_name]
    φ = (1 + 5**0.5) / 2
    s = scale / 100.0

    B_width = 2 * W
    A_height = B_width / φ
    B_small_width = A_height / φ
    A_small_height = A_height

    Final_B_width = B_width * s
    Final_A_height = A_height * s
    Final_B_small_width = B_small_width * s
    Final_A_small_height = A_small_height * s

    Grey_x = (2 * W - Final_B_width) / 2
    Grey_y = (H - Final_A_height) / 2

    scribus.gotoPage(2)

    ensure_color("GR_grey", 0, 0, 0, 20)

    grey_rect = scribus.createRect(Grey_x, Grey_y, Final_B_width, Final_A_height)
    scribus.setFillColor("GR_grey", grey_rect)
    scribus.setLineColor("None", grey_rect)

    scribus.setLayerOutlined(alayer, True)
    scribus.setActiveLayer("Background")

    left = W - (Grey_x + Final_B_small_width)
    right = Grey_x
    top = Grey_y
    bottom = H - (Grey_y + Final_A_small_height)

    return left, right, top, bottom


# GOLDEN RECTANGLE (SINGLE PAGE)
def draw_golden_rectangle_single_page(paper_name, scale):
    mm()
    new_layer("Golden rectangle (single page) construction")
    alayer = scribus.getActiveLayer()

    W, H = papers[paper_name]
    φ = (1 + 5**0.5) / 2
    s = scale / 100.0

    A_height = H
    B_width = A_height / φ

    Final_B_width = B_width * s
    Final_A_height = A_height * s

    Grey_x = (W - Final_B_width) / 2
    Grey_y = (H - Final_A_height) / 2

    scribus.gotoPage(1)

    ensure_color("GR_grey", 0, 0, 0, 20)

    grey_rect = scribus.createRect(Grey_x, Grey_y, Final_B_width, Final_A_height)
    scribus.setFillColor("GR_grey", grey_rect)
    scribus.setLineColor("None", grey_rect)

    scribus.setLayerOutlined(alayer, True)
    scribus.setActiveLayer("Background")

    left = Grey_x
    right = Grey_x
    top = Grey_y
    bottom = Grey_y

    return left, right, top, bottom


# GOLDEN RATIO
def draw_golden_ratio(paper_name, left_inside):
    mm()
    new_layer("Golden ratio construction")
    alayer = scribus.getActiveLayer()

    W, H = papers[paper_name]
    φ = (1 + 5**0.5) / 2

    inside = left_inside

    A_height = H - 2 * (inside * φ)
    B_width = A_height / φ 

    Grey_x = inside
    Grey_y = inside * φ

    Grey_small_x = 0
    Grey_small_y = 0

    scribus.gotoPage(3)

    ensure_color("GR_grey", 0, 0, 0, 20)

    grey_rect = scribus.createRect(Grey_x, Grey_y, B_width, A_height)
    scribus.setFillColor("GR_grey", grey_rect)
    scribus.setLineColor("None", grey_rect)

    grey_small_rect = scribus.createRect(Grey_small_x, Grey_small_y, Grey_x, Grey_y)
    scribus.setFillColor("GR_grey", grey_small_rect)
    scribus.setLineColor("None", grey_small_rect)

    scribus.setLayerOutlined(alayer, True)
    scribus.setActiveLayer("Background")

    left = inside
    right = W - left - B_width
    top = left * φ
    bottom = top

    return left, right, top, bottom


# FIBONACCI 2:3:5:8
def draw_fibonacci_2358(paper_name, left_inside):
    mm()
    new_layer("Fibonacci 2:3:5:8 construction")
    alayer = scribus.getActiveLayer()
    W, H = papers[paper_name]

    inside = left_inside

    Grey_x = inside
    Grey_y = inside + inside/2
    width = W - (2 * Grey_x + Grey_y)
    height = H - (3 * Grey_y + Grey_x)

    scribus.gotoPage(3)

    ensure_color("GR_grey", 0, 0, 0, 20)

    grey_rect = scribus.createRect(Grey_x, Grey_y, width, height)
    scribus.setFillColor("GR_grey", grey_rect)
    scribus.setLineColor("None", grey_rect)

    left   = Grey_x
    right  = left + Grey_y
    top    = Grey_y
    bottom = top + right

    scribus.setLayerOutlined(alayer, True)
    scribus.setActiveLayer("Background")

    return left, right, top, bottom


# 2:3:4:6
def draw_2346(paper_name, left_inside):
    mm()
    new_layer("2:3:4:6 construction")
    alayer = scribus.getActiveLayer()
    W, H = papers[paper_name]

    inside = left_inside

    Grey_x = inside
    Grey_y = inside + inside/2
    width = W - 3 * Grey_x
    height = H - 3 * Grey_y

    scribus.gotoPage(3)

    ensure_color("GR_grey", 0, 0, 0, 20)

    grey_rect = scribus.createRect(Grey_x, Grey_y, width, height)
    scribus.setFillColor("GR_grey", grey_rect)
    scribus.setLineColor("None", grey_rect)

    left   = Grey_x
    right  = 2 * left
    top    = Grey_y
    bottom = left + right

    scribus.setLayerOutlined(alayer, True)
    scribus.setActiveLayer("Background")

    return left, right, top, bottom


# Page ratio canon
def draw_page_ratio_canon(paper_name, left_inside):
    mm()
    new_layer("Page ratio canon construction")
    alayer = scribus.getActiveLayer()
    W, H = papers[paper_name]

    inside = left_inside

    page_ratio = H/W

    Grey_x = inside
    Grey_y = inside * page_ratio
    width = W - 3 * Grey_x
    height = H - 3 * Grey_y

    scribus.gotoPage(3)

    ensure_color("GR_grey", 0, 0, 0, 20)

    grey_rect = scribus.createRect(Grey_x, Grey_y, width, height)
    scribus.setFillColor("GR_grey", grey_rect)
    scribus.setLineColor("None", grey_rect)

    left   = Grey_x
    right  = 2 * left
    top    = Grey_y
    bottom = 2 * top

    scribus.setLayerOutlined(alayer, True)
    scribus.setActiveLayer("Background")

    return left, right, top, bottom


# MASTER PAGES
def create_masterpages_and_apply(left, right, top, bottom, canon_name):
    scribus.setMargins(left, right, top, bottom)

    CN = canon_name

    if CN == "Van de Graaf canon":
        try:
            rpage = scribus.createMasterPage(CN+" right")
            rpage.scribus.setPageType(2)
        except:
            pass
        try:
            lpage = scribus.createMasterPage(CN+" left")
            lpage.scribus.setPageType(0)
        except:
            pass
    elif CN == "Interpretation of Rosarivo":
        try:
            rpage = scribus.createMasterPage(CN+" right")
            rpage.scribus.setPageType(2)
        except:
            pass
        try:
            lpage = scribus.createMasterPage(CN+" left")
            lpage.scribus.setPageType(0)
        except:
            pass
    elif CN == "Golden rectangle (facing pages)":
        try:
            rpage = scribus.createMasterPage(CN+" right")
            rpage.scribus.setPageType(2)
        except:
            pass
        try:
            lpage = scribus.createMasterPage(CN+" left")
            lpage.scribus.setPageType(0)
        except:
            pass
    elif CN == "Golden rectangle (single page)":
        try:
            spage = scribus.createMasterPage(CN)
            spage.scribus.setPageType(2)
        except:
            pass
    elif CN == "Golden ratio":
        try:
            rpage = scribus.createMasterPage(CN+" right")
            rpage.scribus.setPageType(2)
        except:
            pass
        try:
            lpage = scribus.createMasterPage(CN+" left")
            lpage.scribus.setPageType(0)
        except:
            pass
    elif CN == "Fibonacci 2:3:5:8":
        try:
            rpage = scribus.createMasterPage(CN+" right")
            rpage.scribus.setPageType(2)
        except:
            pass
        try:
            lpage = scribus.createMasterPage(CN+" left")
            lpage.scribus.setPageType(0)
        except:
            pass
    elif CN == "2:3:4:6":
        try:
            rpage = scribus.createMasterPage(CN+" right")
            rpage.scribus.setPageType(2)
        except:
            pass
        try:
            lpage = scribus.createMasterPage(CN+" left")
            lpage.scribus.setPageType(0)
        except:
            pass
    elif CN == "Page ratio canon":
        try:
            rpage = scribus.createMasterPage(CN+" right")
            rpage.scribus.setPageType(2)
        except:
            pass
        try:
            lpage = scribus.createMasterPage(CN+" left")
            lpage.scribus.setPageType(0)
        except:
            pass
    else:
        pass

    total = scribus.pageCount()
    if total == 1:
        scribus.applyMasterPage(CN, 1)
    else:
        for page in range(1, total + 1):
            if page % 2 == 0:
                scribus.applyMasterPage(CN+" left", page)
            else:
                scribus.applyMasterPage(CN+" right", page)


# DIALOG WINDOW
def get_values(parent=None):
    dialog = tk.Toplevel(parent)
    dialog.title("Canons of page construction")
    dialog.geometry("410x290")
    dialog.resizable(False, False)
    dialog.grab_set()

    ttk.Label(dialog, text="Select paper size:").place(x=20, y=20)
    paperCombo = ttk.Combobox(dialog, width="30", state="readonly", values=list(papers.keys()))
    paperCombo.place(x=180, y=20)
    paperCombo.current(2)

    ttk.Label(dialog, text="Select canon:").place(x=20, y=60)
    canonCombo = ttk.Combobox(dialog, width="30", state="readonly", values=list(canons))
    canonCombo.place(x=180, y=60)
    canonCombo.current(0)

    ttk.Label(dialog, text="Golden rectangle (%):").place(x=20, y=100)
    scale_var = tk.IntVar(value=80)
    scaleSlider = ttk.Scale(dialog, from_=50, to=90, orient="horizontal", variable=scale_var)
    scaleSlider.place(x=180, y=100, width=150)
    scaleLabel = ttk.Label(dialog, text="80 %")
    scaleLabel.place(x=180, y=130)

    ttk.Label(dialog, text="Left (inside) margin:").place(x=20, y=170)
    left_inside_var = tk.IntVar(value=20)
    left_insideSlider = ttk.Scale(dialog, from_=10, to=50, orient="horizontal", variable=left_inside_var)
    left_insideSlider.place(x=180, y=170, width=150)
    left_insideLabel = ttk.Label(dialog, text="20 mm")
    left_insideLabel.place(x=180, y=200)

    def update_state(*args):
        if canonCombo.get() == "Golden rectangle (facing pages)" or canonCombo.get() == "Golden rectangle (single page)":
            scaleSlider.state(["!disabled"])
            scaleLabel.config(foreground="black")
            left_insideSlider.state(["disabled"])
            left_insideLabel.config(foreground="#999")
        elif canonCombo.get() == "Golden ratio" or canonCombo.get() == "Fibonacci 2:3:5:8" or canonCombo.get() == "2:3:4:6" or canonCombo.get() == "Page ratio canon":
            left_insideSlider.state(["!disabled"])
            left_insideLabel.config(foreground="black")
            scaleSlider.state(["disabled"])
            scaleLabel.config(foreground="#999")
        else:
            scaleSlider.state(["disabled"])
            scaleLabel.config(foreground="#999")
            left_insideSlider.state(["disabled"])
            left_insideLabel.config(foreground="#999")

    def update_left_inside_range(*args):
        paper = paperCombo.get()
        if paper in papers:
            W, H = papers[paper]

            max_inside = round(W / 6)
            left_insideSlider.config(to=max_inside)

            if left_inside_var.get() > max_inside:
                left_inside_var.set(max_inside)

            left_insideLabel.config(text=f"{left_inside_var.get()} mm")

    canonCombo.bind("<<ComboboxSelected>>", update_state)
    update_state()

    paperCombo.bind("<<ComboboxSelected>>", update_left_inside_range)
    update_left_inside_range()

    def update_scale_label(*args):
        scaleLabel.config(text=f"{scale_var.get()} %")
    scale_var.trace_add("write", update_scale_label)

    def update_left_inside_label(*args):
        left_insideLabel.config(text=f"{left_inside_var.get()} mm")
    left_inside_var.trace_add("write", update_left_inside_label)

    result = {"paper": None, "canon": None, "scale": None, "left_inside": None}

    def on_create():
        result["paper"] = paperCombo.get()
        result["canon"] = canonCombo.get()
        result["scale"] = scale_var.get()
        result["left_inside"] = left_inside_var.get()
        dialog.destroy()

    def on_cancel():
        result["paper"] = None
        result["canon"] = None
        result["scale"] = None
        result["left_inside"] = None
        dialog.destroy()

    def on_close():
        result["paper"] = None
        result["canon"] = None
        result["scale"] = None
        result["left_inside"] = None
        dialog.destroy()

    dialog.protocol("WM_DELETE_WINDOW", on_close)

    ttk.Button(dialog, text="Create", command=on_create).place(x=20, y=240)
    ttk.Button(dialog, text="Cancel", command=on_cancel).place(x=120, y=240)

    dialog.wait_window()
    return result["paper"], result["canon"], result["scale"], result["left_inside"]


# MAIN EXECUTION
def main(argv):
    root = tk.Tk()
    root.withdraw()

    paper_name, canon_name, scale, left_inside = get_values(parent=root)
    if not paper_name:
        scribus.messageBox("Info", "The script has been canceled.", scribus.ICON_WARNING, scribus.BUTTON_OK)
        return

    if canon_name == "Golden rectangle (single page)":
        create_new_doc_single_page(paper_name)
    else:
        create_new_doc_facing_pages(paper_name)

    if canon_name == "Van de Graaf canon":
        left, right, top, bottom = draw_vandegraaf(paper_name)
        create_masterpages_and_apply(left, right, top, bottom, canon_name)
    elif canon_name == "Interpretation of Rosarivo":
        left, right, top, bottom = draw_rosarivo(paper_name)
        create_masterpages_and_apply(left, right, top, bottom, canon_name)
    elif canon_name == "Golden rectangle (facing pages)":
        left, right, top, bottom = draw_golden_rectangle_facing_pages(paper_name, scale)
        create_masterpages_and_apply(left, right, top, bottom, canon_name)
    elif canon_name == "Golden rectangle (single page)":
        left, right, top, bottom = draw_golden_rectangle_single_page(paper_name, scale)
        create_masterpages_and_apply(left, right, top, bottom, canon_name)
    elif canon_name == "Golden ratio":
        left, right, top, bottom = draw_golden_ratio(paper_name, left_inside)
        create_masterpages_and_apply(left, right, top, bottom, canon_name)
    elif canon_name == "Fibonacci 2:3:5:8":
        left, right, top, bottom = draw_fibonacci_2358(paper_name, left_inside)
        create_masterpages_and_apply(left, right, top, bottom, canon_name)
    elif canon_name == "2:3:4:6":
        left, right, top, bottom = draw_2346(paper_name, left_inside)
        create_masterpages_and_apply(left, right, top, bottom, canon_name)
    elif canon_name == "Page ratio canon":
        left, right, top, bottom = draw_page_ratio_canon(paper_name, left_inside)
        create_masterpages_and_apply(left, right, top, bottom, canon_name)
    else:
        pass


def main_wrapper(argv):
    try:
        scribus.statusMessage("Running script...")
        scribus.progressReset()
        main(argv)
    finally:
        if scribus.haveDoc():
            scribus.setRedraw(True)
            scribus.redrawAll()
        scribus.statusMessage("Script finished successfully.")
        scribus.progressReset()


if __name__ == "__main__":
    main_wrapper(sys.argv)
