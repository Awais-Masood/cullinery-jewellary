# This is second step implementation of this project.
# In first step images data was scraped.
# In this step images resized for excel and excel created.
import os
import pandas as pd
from PIL import Image, ImageChops

datalist_dir = []
datalist_dir_rings = []
def fn_recursion (start, level = 1):
    global datalist_dir
    for item in os.listdir (start):
        #print (item)
        item_path = os.path.join (start, item)
        if os.path.isdir (item_path):
            print (item_path , ' is directory and level is ', level)
            #if level == 2:
                # cols_ = item_path.split ('\\')
                # print (cols_)
            fn_recursion (item_path, level + 1)
        else:
            print (item_path , ' is not directory. Recursion terminating.') 
            cols_ = item_path.split ('\\') 
            print (cols_)
            dict_dir = {
                'One': cols_[0],
                'Two': cols_[1],
                'Three': cols_[2],
                'Four': cols_[3]
            }
            datalist_dir.append (dict_dir)

    return
def fn_recursion_png (start):
    for item in os.listdir (start):
        item_path = os.path.join (start, item) # This constructs path as program moves deep in the folders
        if os.path.isdir (item_path): 
          fn_recursion_png (item_path)
        else:
            if 'jpg' in item_path:
                image_path_name = item_path.split ('.')[0] #engagement-rings\Platinum\Asscher\Emmy\1.jpg (.jpg will  be removed)
                print (image_path_name)
                im = Image.open (item_path)
                print (image_path_name + '.png')
                im.save (image_path_name + '.png') # It will save image as png
                png_im = Image.open (image_path_name + '.png')
                png_im_resized = png_im.resize ((144, 144), Image.LANCZOS) # Reduce image in proportionate size
                png_im_resized.save (image_path_name + '.png')
                os.remove (image_path_name + '.jpg')   
def fn_recursion_rings (start, level = 1):
    global datalist_dir_rings
    empty_string = ""
    
    for item in os.listdir (start):
        #print (item)
        item_path = os.path.join (start, item) # This constructs path as program moves deep in the folders
        if os.path.isdir (item_path):
            print (item_path , ' is directory and level is ', level)
            fn_recursion_rings (item_path, level + 1)
        else:
            print (item_path , ' is not directory. Node level reached.')#engagement-rings\Platinum\Asscher\Emmy\1.jpg
            cols_ = item_path.split ('\\') # Extra \ as \ is special character in python. For python to under stand \ in above path it has to be written like \\
            
            print (cols_)
            sorting_ = cols_[4].split ('.') # Sorting column introduced as dataframe is saving images in 1,10,11, 2, 3, 4 order instead of 1, 2, 3, 4...10, 11, 12
            sorting_ = int (sorting_[0])
            dict_dir = {
                'Category': cols_[0],
                'Metal': cols_[1],
                'Shape': cols_[2],
                'Ring': cols_[3],
                'Sorting': sorting_,
                'Image': cols_[4],
                'Picture': empty_string,
                'Path': item_path,
            }
            #print ('----------Printing Dictionary--------------')
            #print (dict_dir)
            #print ('------------------------------------------')
            datalist_dir_rings.append (dict_dir)
            #print ('----------Printing List-------------------')
            #print (datalist_dir_rings)
            #print ('-------------------------------------------')
def export_to_excel ():
    global datalist_dir_rings
    print (datalist_dir_rings)
    with pd.ExcelWriter ('output.xlsx', engine='xlsxwriter') as excel_writer:
        df = pd.DataFrame (datalist_dir_rings)
        #df = df.sort_values (by='Sorting')
        df = df.groupby (['Category', 'Metal', 'Shape', 'Ring']).apply (lambda x: x.sort_values (by='Sorting')) # For sorting of images against each Ring name.
        print (df)
        df.to_excel (excel_writer, index=False)
        print (len (df))
        work_sheet = excel_writer.sheets["Sheet1"]
        work_sheet.set_default_row (108) #Height of row
        work_sheet.set_column (6, 6, 19.5) #Width of column
        for i in range (1, len (df)+1):
            row_num = 'I' + str (i+1)
            work_sheet.write (row_num, i)
            row_num = 'G' + str (i+1)
            #work_sheet.insert_image (row_num, df.iloc[i-1, 7], {'x_scale':0.25,'y_scale':0.25})
            work_sheet.insert_image (row_num, df.iloc[i-1, 7]) # df.iloc [row, column]... Gives access to an excel cell... In this case this cell contains image path. 
            #if i == 100:
            #   break
        print (df.Sorting)
        # for item in df.Path:
        #     print (item)
        print (df.iloc [0, 6])

    datalist_dir = []
    dict_dir = {
        'Category': 'engagement-rings',
        'Metal': 'Platinum',
        'Shape': 'Asscher',
        'Ring': 'Emmy',
        'Sorting': 1
    }

    datalist_dir.append (dict_dir)

    dict_dir = {
        'Category': 'engagement-rings',
        'Metal': 'Platinum',
        'Shape': 'Asscher',
        'Ring': 'Emmy',
        'Sorting': 10
    }
    datalist_dir.append (dict_dir)
    dict_dir = {
        'Category': 'engagement-rings',
        'Metal': 'Platinum',
        'Shape': 'Asscher',
        'Ring': 'Emmy',
        'Sorting': 3
    }
    datalist_dir.append (dict_dir)
    dict_dir = {
        'Category': 'engagement-rings',
        'Metal': 'Platinum',
        'Shape': 'Asscher',
        'Ring': 'Emmy',
        'Sorting': 2
    }
    datalist_dir.append (dict_dir)

    df = pd.DataFrame (datalist_dir)
    print (df)
    #print (df.Sorting)
    df_new = df.sort_values (by='Sorting')
    print (df_new)
if __name__ == "__main__":
    ######## Test section to test how recursion works #########
    #dir = 'level1'
    #fn_recursion (dir)
    dir_rings = 'engagement-rings-png'    
    ########### First Call. It will re-size images ############
    #fn_recursion_png (dir_rings)
    ########### After Call. It will generate excel ############
    #fn_recursion_rings ('engagement-rings-png')
    #export_to_excel ()
    