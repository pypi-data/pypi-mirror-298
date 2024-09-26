import fitz  # PyMuPDF
import os
import shutil
import time  # For introducing a delay

def pdf_to_img_pdf(pdf):
    '''
    f(x): it takes a pdf and creates a new pdf out of images of it.
    in  : pdf file path
    out : new pdf made of png images
    '''
    # 1° creates folder with imgs:
    file_name = pdf_to_imgs(pdf, save=True)
    
    # 2° create files:
    new_pdf_path = imgs_to_pdf(file_name)
    
    if new_pdf_path:
        # 3° add a small delay to ensure save process completes
        time.sleep(1)  # Wait for 1 second to ensure save completes
        # 4° remove_all if PDF saved:
        delete_folder('temp')
    else:
        print("PDF creation failed. Temp folder not deleted.")


def pdf_to_imgs(pdf_file, save=True):
    '''
    f(x): it creates a temp folder with png images from the original pdf and provides a file_name for the final pdf
    in  : pdf file path
    out : file_name 
    '''
    doc = fitz.open(pdf_file)
    zoom = 4
    mat = fitz.Matrix(zoom, zoom)
    count = 0

    folder_name = 'temp'
    os.makedirs(folder_name, exist_ok=True)
    
    for p in doc:
        count += 1
    for i in range(count):
        val = os.path.join(folder_name, f"image_{i + 1000000}.png")
        page = doc.load_page(i)
        pix = page.get_pixmap(matrix=mat)
        pix.save(val)    
    doc.close()
    print('Images saved to temp')
    
    return pdf_file.replace('.pdf','')
 

def imgs_to_pdf(file_name, save=True):
    '''
    Converts images from temp folder back to a PDF.
    '''
    doc = fitz.open() 
    imglist = os.listdir('temp')  
    imglist = [f for f in imglist if f.endswith('.png')]  # Only process PNG files
    imglist.sort()  # Ensure images are in order
    
    if not imglist:
        print("No images found in the 'temp' folder.")
        return None
    
    for f in imglist:
        img = fitz.open(os.path.join('temp', f)) 
        rect = img[0].rect  
        pdfbytes = img.convert_to_pdf() 
        img.close() 
        imgPDF = fitz.open("pdf", pdfbytes)  
        page = doc.new_page(width=rect.width, height=rect.height) 
        page.show_pdf_page(rect, imgPDF, 0)  
    
    if save:
        new_pdf_name = file_name + '_dist.pdf'
        c = 1
        while os.path.exists(new_pdf_name):
            new_pdf_name = file_name + f'_dist_v{c}.pdf'
            c += 1
        try:
            doc.save(new_pdf_name)
            print(f"{new_pdf_name} created successfully")
        except Exception as e:
            print(f"Error saving PDF: {e}")
            return None
        finally:
            doc.close()  # Make sure the document is properly closed
        
        return new_pdf_name

    return doc


def delete_folder(folder_path):
    '''
    Deletes a folder and all its contents.
    '''
    # Delete the folder and all its contents
    try:
        shutil.rmtree(folder_path)
        print(f"Folder '{folder_path}' and its contents deleted.")
    except Exception as e:
        print(f"Error deleting folder: {e}")