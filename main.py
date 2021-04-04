# -*- coding: utf-8 -*-
"""
Created on Tue Aug  4 10:39:57 2020

@author: a.zarghami
"""

import os
import glob
import numpy as np
import pandas as pd
import tkinter as tk
from PIL import ImageTk, Image
from tkinter import filedialog
from pandastable import Table


# TODO: Add autosave option
class ImageLabelingForm(object):
    def __init__(self):
        self.img_col_title = 'image'
        self.lbl_col_title = 'label'
        self.df = self.empty_df()

        # All folders
        self.folder_name_list = []
        self.folder_list = []
        
        # Current folder
        self.dirname = ''
        self.folder_idx = 0
        self.folder_name = None
        self.img_list = []
        self.data_file = ''
        
        # Current Image
        self.current_idx = 0
        self.max_idx = 0
        self.image_name = None
        self.image_path = None
        
        self.window = tk.Tk()
        self.window.title("Image Labeling Program")
    
        # Folder Selection
        self.frm_folder = tk.Frame(master=self.window, relief=tk.FLAT)
        
        self.btn_browse = tk.Button(
            master=self.frm_folder, 
            text="Browse",
            command=self.browseFiles,
        )
        self.btn_prev = tk.Button(
            master=self.frm_folder, 
            text="Previous",
            command=self.prev_folder,
        )
        self.btn_next = tk.Button(
            master=self.frm_folder, 
            text="Next",
            command=self.next_folder,
        )
        
        self.btn_browse.pack(side=tk.TOP, padx=2, pady=2)
        self.btn_next.pack(side=tk.RIGHT, padx=2, pady=2)
        self.btn_prev.pack(side=tk.LEFT, padx=2, pady=2)
    
    
        # Label Submission
        self.frm_input = tk.Frame(master=self.window, relief=tk.FLAT)
        
        self.btn_submit = tk.Button(
            master=self.frm_input, 
            text="Submit & Next",
            command=self.submit,
        )
        self.btn_back = tk.Button(
            master=self.frm_input, 
            text="Back",
            command=self.back,
        )
        self.btn_save = tk.Button(
            master=self.frm_input, 
            text="Save",
            command=self.save,
        )
        self.btn_reset = tk.Button(
            master=self.frm_input, 
            text="RESET",
            fg="red",
            command=self.reset,
        )
        self.lbl_cow = tk.Label(master=self.frm_input, text="Cow Number: ")
        self.ent_label = tk.Entry(master=self.frm_input, width=6)
        
        self.lbl_cow.grid(row=0, column=0, padx=2, pady=2)
        self.ent_label.grid(row=0, column=1, padx=2, pady=2)
        self.btn_back.grid(row=1, column=1, padx=2, pady=2)
        self.btn_submit.grid(row=1, column=0, padx=2, pady=2)
        self.btn_save.grid(row=2, column=0, padx=2, pady=2)
        self.btn_reset.grid(row=2, column=1, padx=2, pady=2)
        
        
        # Dialogue
        self.frm_dialogue = tk.Frame(master=self.window, relief=tk.RIDGE, borderwidth=5)
        
        self.lbl_dialogue = tk.Label(master=self.frm_dialogue, text="Please browse for a folder")
        self.lbl_dialogue.pack(side=tk.BOTTOM, padx=2, pady=2)
        
        
        #Image
        self.frm_image = tk.Frame(master=self.window, relief=tk.SUNKEN)
        
        self.lbl_folder = tk.Label(master=self.frm_image, text="No folder selected")
        self.lbl_folder.pack()
        
        img = ImageTk.PhotoImage(Image.open(".\\src\\noimage_placeholder.png"))
        self.img_image = tk.Label(master=self.frm_image, image=img)
        self.img_image.pack()
        
        self.lbl_file = tk.Label(master=self.frm_image, text="No file...")
        self.lbl_file.pack()
        
        
        #Tables
        self.frm_data = tk.Frame(master=self.window, relief=tk.FLAT)
        
        self.pt = Table(self.frm_data, dataframe=self.df)
        self.pt.show()
        
        
        # Frames
        self.frm_image.pack(side=tk.LEFT)
        self.frm_dialogue.pack(side=tk.BOTTOM, pady=60)
        self.frm_folder.pack(pady=30)
        self.frm_input.pack(pady=30)
        self.frm_data.pack(pady=30)
        
        
        # Handlers
        self.pt.rowheader.bind("<Button-1>", self.select_row_handler)
        self.pt.bind("<Button-1>", self.select_row_handler)
        self.window.bind("<Return>", self.return_row_handler)
        self.window.bind("<Tab>", self.return_row_handler)
        self.window.bind("<Left>", self.return_row_handler)
        self.window.bind("<Right>", self.return_row_handler)
        self.window.bind("<Up>", self.return_row_handler)
        self.window.bind("<Down>", self.return_row_handler)
        self.window.mainloop()
        
        
    def browseFiles(self):
        self.dirname = filedialog.askdirectory(initialdir = "./images", 
                                      title = "Select the directory containing the data") 
        if not self.dirname:
            return -1
        
        self.folder_name_list = [ name for name in os.listdir(os.path.dirname(self.dirname)) if os.path.isdir(os.path.join(os.path.dirname(self.dirname), name)) ]
        self.folder_list = [ os.path.join(os.path.dirname(self.dirname), name) for name in os.listdir(os.path.dirname(self.dirname)) if os.path.isdir(os.path.join(os.path.dirname(self.dirname), name)) ]
        self.folder_idx = self.folder_name_list.index(os.path.basename(self.dirname))
        self.load_set()
        

    def next_folder(self):
        if self.folder_idx < len(self.folder_list)-1:
            self.folder_idx += 1
            self.dirname = self.folder_list[self.folder_idx]
            self.load_set()
        else:
            pass
            # self.reinitiate()
    
    def prev_folder(self):
        if self.folder_idx > 0:
            self.folder_idx -= 1
            self.dirname = self.folder_list[self.folder_idx]
            self.load_set() 
        else:
            pass
    
    def submit(self):
        # Reads the input label
        input_label = self.ent_label.get()
        self.df.at[self.current_idx, self.lbl_col_title] = input_label
        
        self.pt.redraw()
        
        if self.current_idx == self.max_idx:
            self.df.to_csv(self.data_file, index=False)
            self.ent_label.delete(0, tk.END)
            self.lbl_dialogue.configure(text="(AUTO SAVE) No more images remaining")
            self.next_folder()
        else:
            self.current_idx += 1
            self.load_image()
            
    
    def back(self):
        if self.current_idx > 0:
            self.current_idx -= 1
        
        # Place the highlight on the current row in the table
        self.pt.setSelectedRow(self.current_idx)
        self.pt.redraw()
        
        self.load_image()
        
    
    def save(self):
        self.df.to_csv(self.data_file, index=False)
        self.lbl_dialogue.configure(text="Progress saved")
        
    
    def reset(self):
        self.df.drop(columns=self.lbl_col_title, inplace=True)
        self.df[self.lbl_col_title] = np.nan
        self.df = self.df.astype(dtype={self.lbl_col_title: object})
        self.pt.redraw()
        self.ent_label.delete(0, tk.END)
        self.lbl_dialogue.configure(text="Progress reset")
    
    
    def reinitiate(self):
        self.df = self.empty_df()

        self.current_idx = 0
        self.max_idx = 0
        self.image_name = None
        self.image_path = None
        
        self.pt.model.df = self.df
        self.pt.setSelectedRow(self.current_idx)
        self.pt.redraw()  
        
        self.lbl_folder.configure(text="No folder selected")
        
        self.lbl_file.configure(text='No file...')
        
        img = ImageTk.PhotoImage(Image.open(".\\src\\noimage_placeholder.png"))
        self.img_image.configure(image=img)
        self.img_image.image = img
    
    
    def empty_df(self):
        return pd.DataFrame({self.img_col_title:[np.nan], self.lbl_col_title:[np.nan]})
    
    def select_row_handler(self, e):
        rowclicked_single = self.pt.get_row_clicked(e)
    
        if rowclicked_single <= self.max_idx:
            self.current_idx = rowclicked_single
            self.load_image()
    
    # TODO: This method is not functioning properly (Possibly a bug with pandas table)
    def return_row_handler(self, e):
        rowclicked_single = self.pt.getSelectedRow()

        if rowclicked_single <= self.max_idx:
            self.current_idx = rowclicked_single
            self.load_image()
            
    def load_set(self):
        self.data_file = '{}/labels.csv'.format(self.dirname)
        self.folder_name = os.path.basename(self.dirname)

        if os.path.isfile(self.data_file): 
            # Load the dataframe
            self.df = pd.read_csv(self.data_file, dtype={self.lbl_col_title: object})
            # Read image list from dataframe
            self.img_list = list(self.df['image'])
        else:
            # Create dataframe
            self.df = self.empty_df()
            # Create image list
            self.img_list = glob.glob(self.dirname + "//*.jpg")
            self.fill_image_column()
            self.df.to_csv(self.data_file, index=False)
        
        # Update current folder label
        self.lbl_folder.configure(text=self.folder_name)
        
        # Set image properties
        self.max_idx = len(self.df) - 1
        self.current_idx = self.find_first_unlabeled()
        
        self.load_image()
        self.update_button_status()
        self.lbl_dialogue.configure(text="Woking on folder '{}'".format(self.folder_name))
        
    
    def load_image(self):
        self.image_name = self.img_list[self.current_idx]
        self.image_path = os.path.join(self.dirname, self.image_name)
        
        # Update image label
        self.lbl_file.configure(text=self.image_name)
        
        # Update the table and place the highlight on the current row
        self.pt.model.df = self.df      
        self.pt.setSelectedRow(self.current_idx)
        self.pt.redraw()            

        # Set the default value for the text box    
        tb_value = self.determine_text_box_value()
        self.ent_label.delete(0, tk.END)
        self.ent_label.insert(0, tb_value)        
        
        # Load the image
        img = ImageTk.PhotoImage(Image.open(self.image_path).resize((960, 540)))
        self.img_image.configure(image=img)
        self.img_image.image = img
        
        self.update_button_status()
 
    def callback(self, event):
        self.ent_label.selection_range(0, tk.END)
    
    def fill_image_column(self):
        col1 = [os.path.basename(x) for x in self.img_list]
        col2 = np.nan
        temp_dict = {self.img_col_title:col1, self.lbl_col_title:col2}
        self.df = pd.DataFrame(temp_dict)
        self.df = self.df.astype(dtype={self.lbl_col_title: object})

    
    def find_first_unlabeled(self):
        first_null = 0
        nulls = self.df.index[self.df[self.lbl_col_title].isnull()]
        if nulls.any():
            first_null = nulls[0]
        return first_null
    
    
    def determine_text_box_value(self):
        current_value = self.ent_label.get()
        df_value = self.df[self.lbl_col_title][self.current_idx]
        
        if pd.isnull(df_value):
            return current_value
        else:
            return df_value
    
    
    def update_button_status(self):
        if self.folder_idx == 0:
            self.btn_prev["state"] = "disabled"
        else:
            self.btn_prev["state"] = "active"
            
        if self.folder_idx == len(self.folder_list)-1:
            self.btn_next["state"] = "disabled"
        else:
            self.btn_next["state"] = "active"
            
        if self.current_idx == 0:
            self.btn_back["state"] = "disabled"
        else:
            self.btn_back["state"] = "active"
             
        # if (self.current_idx == self.max_idx) and (self.folder_idx == len(self.folder_list)-1):
        #     self.btn_submit["state"] = "disabled"
        # else:
        #     self.btn_submit["state"] = "active"   