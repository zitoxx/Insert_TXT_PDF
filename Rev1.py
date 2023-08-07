import sys
import fitz
import tkinter as tk
from tkinter import messagebox, filedialog
from PIL import Image, ImageTk
from datetime import datetime, date

# Verificar data limite
data_limite = date(2023, 12, 31)

if date.today() > data_limite:
    messagebox.showinfo("Limite Expirado", "O período de uso deste programa expirou.")
    sys.exit()


class VisualizadorPDF:
    def __init__(self, caminho_arquivo_pdf):
        self.photo = None
        self.img = None
        self.imagem = None
        self.page = None
        self.caminho_arquivo_pdf = caminho_arquivo_pdf
        self.pdf_document = fitz.open(self.caminho_arquivo_pdf)
        self.pagina_atual = 0

        self.root = tk.Toplevel()
        self.root.title("Adicionar Texto ao PDF")
        self.root.protocol("WM_DELETE_WINDOW", self.fechar_janela)

        self.frame = tk.Frame(self.root)
        self.frame.pack()

        self.canvas = tk.Canvas(self.frame, width=600, height=800)
        self.canvas.pack(side=tk.LEFT)

        self.atualizar_canvas()

        self.canvas.bind("<Button-1>", self.on_click)

        self.rotulo_explicativo = tk.Label(self.frame, text="Digite aqui o texto:")
        self.rotulo_explicativo.pack(side=tk.TOP)

        self.texto_var = tk.StringVar()
        self.texto_entry = tk.Text(self.frame, wrap=tk.WORD, width=50, height=5)
        self.texto_entry.pack(side=tk.TOP)

        self.botao_pagina_proxima = tk.Button(self.frame, text="Próxima Página", command=self.proxima_pagina)
        self.botao_pagina_proxima.pack(side=tk.TOP)

        self.botao_reabrir_pdf = tk.Button(self.frame, text="Reabrir PDF", command=self.reabrir_pdf)
        self.botao_reabrir_pdf.pack(side=tk.TOP)

        self.botao_finalizar = tk.Button(self.frame, text="Finalizar", command=self.finalizar_edicao)
        self.botao_finalizar.pack(side=tk.TOP)

    def atualizar_canvas(self):
        self.page = self.pdf_document.load_page(self.pagina_atual)
        self.imagem = self.page.get_pixmap()
        self.img = Image.frombytes("RGB", [self.imagem.width, self.imagem.height], self.imagem.samples)
        self.photo = ImageTk.PhotoImage(self.img)

        self.canvas.create_image(-5, -5, anchor=tk.NW, image=self.photo)

    def on_click(self, event):
        x, y = event.x, event.y
        if self.page.number <= self.pdf_document.page_count:
            texto = self.texto_entry.get("1.0", tk.END)
            if texto.strip():
                self.add_text_overlay(x, y, texto)
                self.atualizar_canvas()

    def add_text_overlay(self, x, y, texto):
        canvas_width = self.canvas.winfo_width()
        canvas_height = self.canvas.winfo_height()

        pdf_width = self.page.rect.width
        pdf_height = self.page.rect.height

        x_pdf = (x / canvas_width) * pdf_width
        y_pdf = (y / canvas_height) * pdf_height

        font_size = 20
        font = "helv"  # You can change the font name as needed

        self.page.insert_text((x_pdf, y_pdf), texto, fontsize=font_size, fontname=font, color=(0, 0, 0))

    def proxima_pagina(self):
        if self.pagina_atual < self.pdf_document.page_count - 1:
            self.pagina_atual += 1
            self.atualizar_canvas()

    def finalizar_edicao(self):
        nome_arquivo_editado = self.caminho_arquivo_pdf[:-4] + "_editado.pdf"
        self.pdf_document.save(nome_arquivo_editado)
        self.pdf_document.close()
        self.root.destroy()
        messagebox.showinfo("Edição Concluída", "O arquivo foi editado com sucesso.")
        root.quit()

    def reabrir_pdf(self):
        self.pdf_document.close()
        self.pdf_document = fitz.open(self.caminho_arquivo_pdf)
        self.pagina_atual = 0
        self.atualizar_canvas()

    def fechar_janela(self):
        self.pdf_document.close()
        self.root.destroy()
        root.quit()


if __name__ == "__main__":
    root = tk.Tk()
    root.withdraw()
    caminho_arquivo_pdf = filedialog.askopenfilename(filetypes=[("PDF Files", "*.pdf")])

    if not caminho_arquivo_pdf:
        print("Nenhum arquivo PDF selecionado.")
    else:
        try:
            visualizador = VisualizadorPDF(caminho_arquivo_pdf)
            root.mainloop()
        except Exception as e:
            print("Error:", e)
        finally:
            root.destroy()
