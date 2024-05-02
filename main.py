import csv
from tkinter import Tk, Label, Entry, Button, filedialog, Frame, messagebox
from hashlib import sha1


def generate_variation_code(file_name, base_increment):
  """Generates a variation code based on the file name and a base increment value."""
  hash_object = sha1(file_name.encode())
  hash_hex = hash_object.hexdigest()[:5]
  return f"V-{hash_hex}-{base_increment}"


class Application(Frame):

  def __init__(self, master=None):
    super().__init__(master)
    self.master = master
    self.config(bg="#f0f0f0")
    self.pack(padx=10, pady=10)
    self.create_widgets()

  def create_widgets(self):
    self.master.title("CSV Variations")

    label_options = {"bg": "#f0f0f0", "anchor": "w"}
    entry_options = {"bg": "white", "width": 50}
    button_options = {"bg": "#0052cc", "fg": "white", "padx": 10, "pady": 5"}

    self.file_label = Label(self, text="Choose a csv file:", **label_options)
    self.file_label.pack(fill="x")
    self.file_entry = Entry(self, **entry_options)
    self.file_entry.pack(fill="x", pady=(0, 5))
    self.browse_button = Button(self,
                                text="Browse",
                                command=self.browse_file,
                                **button_options)
    self.browse_button.pack()

    self.column_label = Label(self,
                              text="Column for variations:",
                              **label_options)
    self.column_label.pack(fill="x")
    self.column_entry = Entry(self, **entry_options)
    self.column_entry.pack(fill="x", pady=(0, 5))

    self.process_button = Button(self,
                                 text="Process",
                                 command=self.process_file,
                                 **button_options)
    self.process_button.pack()

  def browse_file(self):
    file_name = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
    self.file_entry.delete(0, "end")
    self.file_entry.insert(0, file_name)

  def process_file(self):
    input_file = self.file_entry.get()
    column_for_variation = self.column_entry.get()

    if not input_file:
      messagebox.showerror("Error", "File not selected.")
      return

    if not column_for_variation:
      messagebox.showerror("Error", "Column name not specified.")
      return

    output_file = 'VAR-' + input_file.split('/')[-1]
    delimiter = ';'
    variation_increment = 10
    unique_sku_prefix = "SKU-"

    try:
      with open(input_file, mode='r',
                encoding='UTF-8') as infile, open(output_file,
                                                  mode='w',
                                                  encoding='utf-8-sig',
                                                  newline='') as outfile:
        reader = csv.DictReader(infile, delimiter=delimiter)
        fieldnames = reader.fieldnames + ["Variation group code", "SKU"]
        writer = csv.DictWriter(outfile,
                                fieldnames=fieldnames,
                                delimiter=delimiter)
        writer.writeheader()

        variation_code_number = 0
        for row in reader:
          if column_for_variation in row:
            colors = row[column_for_variation].split('/')
            is_variation = len(colors) > 1
            if is_variation:
              variation_code_number += variation_increment
            variation_group_code = generate_variation_code(
                input_file, variation_code_number) if is_variation else ""
            for color in colors:
              new_row = row.copy()
              new_row[column_for_variation] = color.strip()
              new_row["Variation group code"] = variation_group_code
              writer.writerow(new_row)
      messagebox.showinfo(
          "Success",
          f"File successfully processed. Results saved in {output_file}")
    except Exception as e:
      messagebox.showerror("Error", str(e))


root = Tk()
app = Application(master=root)
app.mainloop()
