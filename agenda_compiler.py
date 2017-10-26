#! /bin/env/python3
# Byron Vickers, 2017

# TODO:
# - pagenums
# - links (https://stackoverflow.com/questions/23834517/add-in-document-link-to-pdf)
# - GUI?

from PyPDF2 import PdfFileWriter, PdfFileReader, pdf
from reportlab.lib.pagesizes import letter, A4
from reportlab.pdfgen import canvas
from os import walk, path, sys
try:
  import readline
except ImportError:
  import pyreadline as readline

def update_watermark(width,height,i,rotation=0):
    c = canvas.Canvas("watermark.pdf", pagesize=(width, height))
    c.setFont("Courier", 10)
    if rotation == 90:
        c.rotate(90)
        c.drawString(height-100,-20,"ATTACHMENT {}".format(i))
    else:
        c.drawString(width-100,height-20,"ATTACHMENT {}".format(i))
    c.showPage()
    c.save()

def get_path_interactive(prompt, should_be_dir=None):
    satisfied = False
    while not satisfied:
        fpath = input(prompt)
        satisfied = path.exists(fpath)
        if not satisfied:
            print("ERROR: The location you entered does not exist. Please check and try again.")
            continue
        if should_be_dir is not None:
            satisfied = satisfied and (not (should_be_dir ^ path.isdir(fpath)))
        if not satisfied:
            print("ERROR: The location entered is not a {}".format("directory" if should_be_dir else "file"))
            continue
    return fpath

def main(base_fname, attachment_dir, output_fname):
    output = PdfFileWriter()
    page_acc = 0
    bookmarks_to_add = {}

    input_base = PdfFileReader(open(base_fname, "rb"))
    bookmarks_to_add.update({page_acc:"Agenda"})
    page_acc += len(input_base.pages)
    for page in input_base.pages:
        output.addPage(page)

    attachments = []
    for (dirpath, dirnames, filenames) in walk(attachment_dir):
        attachments.extend([f for f in filenames if f.endswith(".pdf")])
        # walk does not promise any ordering, so sort
        attachments.sort()
        break # don't recurse through subdirectories

    for attch_no, attachment in enumerate(attachments):
        input_attch = PdfFileReader(open(path.join(attachment_dir,attachment), "rb"))
        bookmarks_to_add.update({page_acc:"ATTACHMENT {}".format(attch_no+1)})
        page_acc += len(input_attch.pages)
        print(attachment)
        for i, page in enumerate(input_attch.pages):
            # update watermark on every page in case size/rotation has changed
            mbox = page.mediaBox
            rotation = page['/Rotate']
            width, height = (float(a-b) for a, b in zip(mbox.upperRight, mbox.lowerLeft))
            update_watermark(width, height, attch_no+1, rotation)
            watermark = PdfFileReader(open("watermark.pdf", "rb"))
            # merge watermark page with attachment page
            page.mergePage(watermark.getPage(0))
            output.addPage(page)
            print("Attachment {}, page {}".format(attch_no+1,i+1))

    for page, label in sorted(bookmarks_to_add.items()):
        print(page,label)
        output.addBookmark(label, page, parent=None)

    output.setPageMode("/UseOutlines")
    outputStream = open(output_fname, "wb")
    output.write(outputStream)

if __name__ == "__main__":
    if len(sys.argv) == 3:
        base_fname, attachment_dir = sys.argv[1:]
    else:
        base_fname = get_path_interactive("Enter location of agenda pdf: ", False)
        attachment_dir = get_path_interactive("Enter location of attachment directory: ", True)
    main(base_fname, attachment_dir, "agenda-compiled.pdf")
