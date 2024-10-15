import tkinter as tk
from tkinter import filedialog, messagebox
from PyPDF2 import PdfMerger

class PDFMergerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("PDF Zusammenfügen")
        self.pdf_list = []

        # Größeres Standardfenster einstellen
        self.root.geometry('800x600')

        self.create_widgets()
        self.bind_drag_and_drop()

    def create_widgets(self):
        # Größere Schriftarten verwenden
        self.button_font = ('Arial', 14)
        self.listbox_font = ('Arial', 12)

        self.frame = tk.Frame(self.root)
        self.frame.pack(padx=20, pady=20, fill=tk.BOTH, expand=True)

        self.add_button = tk.Button(self.frame, text="PDF hinzufügen", command=self.add_pdf, font=self.button_font)
        self.add_button.grid(row=0, column=0, padx=10, pady=10, sticky='ew')

        self.remove_button = tk.Button(self.frame, text="Ausgewählte entfernen", command=self.remove_pdf, font=self.button_font)
        self.remove_button.grid(row=0, column=1, padx=10, pady=10, sticky='ew')

        self.pdf_listbox = tk.Listbox(self.frame, font=self.listbox_font)
        self.pdf_listbox.grid(row=1, column=0, columnspan=2, padx=10, pady=10, sticky='nsew')

        self.merge_button = tk.Button(self.frame, text="PDFs zusammenführen", command=self.merge_pdfs, font=self.button_font)
        self.merge_button.grid(row=2, column=0, columnspan=2, pady=20, sticky='ew')

        # Zeilen und Spalten skalierbar machen
        self.frame.rowconfigure(1, weight=1)
        self.frame.columnconfigure(0, weight=1)
        self.frame.columnconfigure(1, weight=1)

    def bind_drag_and_drop(self):
        self.pdf_listbox.bind('<ButtonPress-1>', self.on_start_drag)
        self.pdf_listbox.bind('<B1-Motion>', self.on_drag_motion)
        self.pdf_listbox.bind('<ButtonRelease-1>', self.on_drop)

    def on_start_drag(self, event):
        # Startposition speichern
        self.drag_start_index = self.pdf_listbox.nearest(event.y)

    def on_drag_motion(self, event):
        # Aktuelle Position während des Ziehens ermitteln
        new_index = self.pdf_listbox.nearest(event.y)
        if new_index != self.drag_start_index:
            # Elemente in der Listbox tauschen
            item_text = self.pdf_listbox.get(self.drag_start_index)
            self.pdf_listbox.delete(self.drag_start_index)
            self.pdf_listbox.insert(new_index, item_text)
            # Pfade in der Liste aktualisieren
            self.pdf_list.insert(new_index, self.pdf_list.pop(self.drag_start_index))
            # Neue Startposition setzen
            self.drag_start_index = new_index
            # Aktuelles Element markieren
            self.pdf_listbox.selection_clear(0, tk.END)
            self.pdf_listbox.selection_set(new_index)

    def on_drop(self, event):
        # Drag-and-Drop-Vorgang beenden (kann für zukünftige Funktionen genutzt werden)
        pass

    def add_pdf(self):
        files = filedialog.askopenfilenames(filetypes=[("PDF Dateien", "*.pdf")])
        for file in files:
            if file not in self.pdf_list:
                self.pdf_list.append(file)
                self.pdf_listbox.insert(tk.END, file)

    def remove_pdf(self):
        selected_indices = self.pdf_listbox.curselection()
        for index in reversed(selected_indices):
            self.pdf_listbox.delete(index)
            del self.pdf_list[index]

    def merge_pdfs(self):
        if not self.pdf_list:
            messagebox.showwarning("Keine PDFs", "Bitte fügen Sie mindestens eine PDF-Datei hinzu.")
            return

        save_path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF Dateien", "*.pdf")])
        if not save_path:
            return

        merger = PdfMerger()

        try:
            for pdf in self.pdf_list:
                merger.append(pdf)

            merger.write(save_path)
            merger.close()
            messagebox.showinfo("Erfolg", f"PDFs wurden erfolgreich zu '{save_path}' zusammengeführt.")
        except Exception as e:
            messagebox.showerror("Fehler", f"Ein Fehler ist aufgetreten:\n{e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = PDFMergerApp(root)
    root.mainloop()
