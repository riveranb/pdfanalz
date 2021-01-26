import sys

import fitz

if len(sys.argv) <= 1:
    exit(-1)

contents = fitz.open(sys.argv[1])
pageContext = []

# parse every page
for page in contents:
    paragraphs = []
    paragraph = ''
    prevb = None

    blocks = page.getTextPage().extractBLOCKS()
    # one line a block
    # [left, top, right, bottom, <content>, block_no, block_type]
    # block_type = 0, text
    for b in blocks:
        if b[6] == 0:
            text = b[4].strip()
            if len(text) > 0:
                if prevb is not None and b[5] - prevb[5] > 1:
                    paragraphs.append(paragraph) # new paragraph
                    paragraph = ''
                paragraph += text + '\n'
                prevb = b

    # end of page
    if len(paragraph) > 0:
        paragraphs.append(paragraph)
        paragraph = ''

    pageContext.append((page.number, paragraphs))

option = ''
if len(sys.argv) > 2:
    option = sys.argv[2]

if option == '-dump':
    for page in pageContext:
        print("page: ", page[0], "\n")
        for p in page[1]:
            print("paragraph: \n", p)
elif option == '-search':
    exit(0)