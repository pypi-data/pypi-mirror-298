#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: zj
# date: 2023/12/22

import os
try:
    import pymupdf
except:
    import fitz as pymupdf
from PIL import Image
from tqdm import tqdm
from multiprocessing import cpu_count

try:
    from .files import makedirs, get_file_path_list
    from .concurrency import multi_task
except:
    from files import makedirs, get_file_path_list
    from concurrency import multi_task


def image2pdf(image_path_lst, save_path):
    doc = pymupdf.open()  # PDF with the pictures
    print(f'convert images to pdf...')
    with tqdm(total=len(image_path_lst)) as pbar:
        for i, image_path in enumerate(image_path_lst):
            img = pymupdf.open(image_path)  # open pic as document
            rect = img[0].rect  # pic dimension
            pdfbytes = img.convert_to_pdf()  # make a PDF stream
            img.close()  # no longer needed
            imgPDF = pymupdf.open("pdf", pdfbytes)  # open stream as PDF
            page = doc.new_page(width=rect.width,  # new page with ...
                                height=rect.height)  # pic dimension
            page.show_pdf_page(rect, imgPDF, 0)  # image fills the page
            pbar.update(1)
    makedirs(os.path.dirname(save_path))
    doc.save(save_path)


def _get_pages(pdf_path, page_index_lst, dpi=200, save_dir=None, verbose=False):
    if save_dir:
        save_dir = os.path.join(save_dir, os.path.splitext(
            os.path.basename(pdf_path))[0])
        if not os.path.exists(save_dir):
            os.makedirs(save_dir, exist_ok=True)
    ret = []
    with pymupdf.open(pdf_path) as pdf:
        with tqdm(total=pdf.page_count, disable=verbose is False) as pbar:
            for i in page_index_lst:
                pm = pdf[i].get_pixmap(dpi=dpi)
                if save_dir:
                    image_save_path = os.path.join(save_dir, f'{i:03d}.png')
                    pm.save(image_save_path)
                    ret.append(image_save_path)
                else:
                    pix = Image.frombytes(
                        "RGB", [pm.width, pm.height], pm.samples)
                    ret.append(pix)
                pbar.update(1)
    if len(ret) == 1:
        ret = ret[0]
    return ret


_cpu_count = cpu_count()


def pdf2image(pdf_path, dpi=200, save_dir=None, workers=_cpu_count, verbose=True, multiprocess=True):
    with pymupdf.open(pdf_path) as pdf:
        page_count = pdf.page_count
    if multiprocess:
        args_lst = [(pdf_path, (i,), dpi, save_dir) for i in range(page_count)]
        ret = multi_task(_get_pages, args_lst, workers, verbose, 'process')
    else:
        page_index_lst = list(range(page_count))
        ret = _get_pages(pdf_path, page_index_lst, dpi, save_dir, verbose)
    return ret


def main():
    pass


if __name__ == '__main__':
    main()
