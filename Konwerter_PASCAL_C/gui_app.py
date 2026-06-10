import sys
import os
import threading
import re
from tkinter import filedialog
import customtkinter as ctk

from antlr4 import FileStream, CommonTokenStream
from Tools.PascalLexer import PascalLexer
from Tools.PascalParser import PascalParser
from main import CodeGeneratorVisitor, ASTBuilder
from error_handler import CompilerException

ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")


class CodeEditor(ctk.CTkFrame):
    def __init__(self, master, language="pascal", **kwargs):
        super().__init__(master, **kwargs)
        self.language = language

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        self.line_numbers = ctk.CTkTextbox(self, width=40, font=("Courier New", 13),
                                           fg_color="#1e1e1e", text_color="#858585",
                                           activate_scrollbars=False, corner_radius=0)
        self.line_numbers.grid(row=0, column=0, sticky="ns")
        self.line_numbers.configure(state="disabled")

        self.text_editor = ctk.CTkTextbox(self, font=("Courier New", 13), corner_radius=0, undo=True)
        self.text_editor.grid(row=0, column=1, sticky="nsew")

        self._original_yscroll = self.text_editor._textbox.cget("yscrollcommand")
        self.text_editor._textbox.configure(yscrollcommand=self._yscroll_interceptor)

        self.text_editor.bind("<KeyRelease>", self._on_text_change)
        self.text_editor.bind("<MouseWheel>", self._on_text_change)
        self.text_editor.bind("<Return>", self._on_text_change)
        self.text_editor.bind("<BackSpace>", self._on_text_change)

        self.text_editor.tag_config("keyword", foreground="#569cd6")  # Niebieski
        self.text_editor.tag_config("string", foreground="#ce9178")  # Pomarańczowy
        self.text_editor.tag_config("comment", foreground="#6a9955")  # Zielony

        if self.language == "pascal":
            self.keywords_regex = r'(?i)\b(program|var|begin|end|if|then|else|while|do|for|to|repeat|until|case|of|procedure|function|integer|real|boolean|char|string|longint|true|false|array|and|or|not|div|mod|writeln|write|readln|read|randomize|random)\b'
            self.string_regex = r"'.*?'"
            self.comment_regex = r'\{.*?\}|\(\*.*?\*\)'
        else:  # C
            self.keywords_regex = r'#include|\b(int|float|char|void|if|else|while|for|do|switch|case|break|return|bool|true|false|printf|scanf|srand|rand|time|NULL)\b'
            self.string_regex = r'".*?"|\'.*?\''
            self.comment_regex = r'//[^\n]*|/\*.*?\*/'

    def _yscroll_interceptor(self, *args):
        """Przechwytuje ruch paska przewijania, nie psując domyślnego zachowania CustomTkinter."""
        if self._original_yscroll:
            self.text_editor._textbox.tk.call(self._original_yscroll, *args)
        self.line_numbers._textbox.yview_moveto(args[0])

    def _update_line_numbers(self):
        lines = self.text_editor.get("1.0", "end-1c").count("\n") + 1
        current_lines = self.line_numbers.get("1.0", "end-1c").count("\n") + 1

        if lines != current_lines or lines == 1:
            line_numbers_content = "\n".join(str(i) for i in range(1, lines + 1))
            self.line_numbers.configure(state="normal")
            self.line_numbers.delete("1.0", "end")
            self.line_numbers.insert("1.0", line_numbers_content)
            self.line_numbers.configure(state="disabled")

    def _highlight_syntax(self):
        text_content = self.text_editor.get("1.0", "end-1c")

        for tag in ["keyword", "string", "comment"]:
            self.text_editor.tag_remove(tag, "1.0", "end")

        def apply_tags(regex_pattern, tag_name):
            flags = re.MULTILINE
            if tag_name == "comment":
                flags |= re.DOTALL

            for match in re.finditer(regex_pattern, text_content, flags):
                start_index = f"1.0 + {match.start()} chars"
                end_index = f"1.0 + {match.end()} chars"
                self.text_editor.tag_add(tag_name, start_index, end_index)

        apply_tags(self.keywords_regex, "keyword")
        apply_tags(self.string_regex, "string")
        apply_tags(self.comment_regex, "comment")

    def _on_text_change(self, event=None):
        self._update_line_numbers()
        self.after(10, self._highlight_syntax)

    def get_text(self):
        return self.text_editor.get("1.0", "end-1c")

    def set_text(self, text):
        self.text_editor.delete("1.0", "end")
        self.text_editor.insert("1.0", text)
        self._on_text_change()

    def set_state(self, state):
        self.text_editor.configure(state=state)


class PascalToCConverterGUI(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Pascal to C Converter")
        self.geometry("1200x800")
        self.minsize(900, 600)

        self.grid_rowconfigure(0, weight=4)
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        self.temp_pas_path = os.path.join(os.getcwd(), "temp_gui_input.pas")

        self._create_widgets()

    def _create_widgets(self):
        main_panel = ctk.CTkFrame(self)
        main_panel.grid(row=0, column=0, padx=15, pady=(15, 5), sticky="nsew")
        main_panel.grid_rowconfigure(0, weight=1)
        main_panel.grid_columnconfigure(0, weight=1)
        main_panel.grid_columnconfigure(1, weight=1)

        left_frame = ctk.CTkFrame(main_panel)
        left_frame.grid(row=0, column=0, padx=10, pady=10, sticky="nsew")
        left_frame.grid_rowconfigure(1, weight=1)
        left_frame.grid_columnconfigure(0, weight=1)

        left_label = ctk.CTkLabel(left_frame, text="Kod źródłowy Pascal", font=ctk.CTkFont(size=14, weight="bold"))
        left_label.grid(row=0, column=0, padx=10, pady=5, sticky="w")

        self.pascal_editor = CodeEditor(left_frame, language="pascal")
        self.pascal_editor.grid(row=1, column=0, padx=10, pady=5, sticky="nsew")

        sample_code = "program Przyklad;\nvar\n    x: integer;\nbegin\n    { Inicjalizacja zmiennej }\n    x := 10;\n    writeln('Wartosc x: ', x);\nend."
        self.pascal_editor.set_text(sample_code)

        left_buttons_frame = ctk.CTkFrame(left_frame, fg_color="transparent")
        left_buttons_frame.grid(row=2, column=0, padx=10, pady=10, sticky="ew")

        self.btn_load = ctk.CTkButton(left_buttons_frame, text="Wgraj plik z dysku", command=self._load_file)
        self.btn_load.pack(side="left", padx=5)

        self.btn_convert = ctk.CTkButton(left_buttons_frame, text="Konwertuj do C ⚡", fg_color="#2c82c9",
                                         hover_color="#246b04", command=self._start_conversion_thread)
        self.btn_convert.pack(side="right", padx=5)

        right_frame = ctk.CTkFrame(main_panel)
        right_frame.grid(row=0, column=1, padx=10, pady=10, sticky="nsew")
        right_frame.grid_rowconfigure(1, weight=1)
        right_frame.grid_columnconfigure(0, weight=1)

        right_label = ctk.CTkLabel(right_frame, text="Wyjściowy kod C", font=ctk.CTkFont(size=14, weight="bold"))
        right_label.grid(row=0, column=0, padx=10, pady=5, sticky="w")

        self.c_editor = CodeEditor(right_frame, language="c")
        self.c_editor.grid(row=1, column=0, padx=10, pady=5, sticky="nsew")

        right_buttons_frame = ctk.CTkFrame(right_frame, fg_color="transparent")
        right_buttons_frame.grid(row=2, column=0, padx=10, pady=10, sticky="ew")

        self.btn_save = ctk.CTkButton(right_buttons_frame, text="Zapisz kod C", command=self._save_file,
                                      state="disabled")
        self.btn_save.pack(side="right", padx=5)

        bottom_panel = ctk.CTkFrame(self)
        bottom_panel.grid(row=1, column=0, padx=15, pady=(5, 15), sticky="nsew")
        bottom_panel.grid_rowconfigure(1, weight=1)
        bottom_panel.grid_columnconfigure(0, weight=1)

        bottom_label = ctk.CTkLabel(bottom_panel, text="Konsola / Status kompilacji",
                                    font=ctk.CTkFont(size=12, weight="bold"))
        bottom_label.grid(row=0, column=0, padx=10, pady=(5, 0), sticky="w")

        self.console_textbox = ctk.CTkTextbox(bottom_panel, activate_scrollbars=True, fg_color="#1e1e1e",
                                              text_color="#d4d4d4", font=("Consolas", 12))
        self.console_textbox.grid(row=1, column=0, padx=10, pady=5, sticky="nsew")
        self._log_message(
            "System gotowy. Wprowadź kod Pascala lub wgraj plik z dysku, a następnie kliknij 'Konwertuj do C'.")

    def _log_message(self, message: str, is_error: bool = False):
        self.console_textbox.configure(state="normal")
        if is_error:
            self.console_textbox.insert("end", f"[BŁĄD] {message}\n")
            self.console_textbox.configure(border_color="#ff4a4a", border_width=1)
        else:
            self.console_textbox.insert("end", f"[INFO] {message}\n")
            self.console_textbox.configure(border_width=0)

        self.console_textbox.see("end")
        self.console_textbox.configure(state="disabled")

    def _load_file(self):
        file_path = filedialog.askopenfilename(
            title="Wybierz plik Pascal",
            filetypes=[("Pliki Pascala", "*.pas"), ("Wszystkie pliki", "*.*")]
        )
        if file_path:
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    content = f.read()
                self.pascal_editor.set_text(content)
                self._log_message(f"Pomyślnie wczytano plik: {os.path.basename(file_path)}")
            except Exception as e:
                self._log_message(f"Nie udało się odczytać pliku: {str(e)}", is_error=True)

    def _save_file(self):
        c_code = self.c_editor.get_text().strip()
        if not c_code:
            return

        file_path = filedialog.asksaveasfilename(
            title="Zapisz wygenerowany kod C",
            defaultextension=".c",
            filetypes=[("Pliki C", "*.c"), ("Wszystkie pliki", "*.*")]
        )
        if file_path:
            try:
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(c_code)
                self._log_message(f"Kod C został pomyślnie zapisany w: {file_path}")
            except Exception as e:
                self._log_message(f"Błąd podczas zapisu pliku: {str(e)}", is_error=True)

    def _start_conversion_thread(self):
        self.btn_convert.configure(state="disabled", text="Konwertowanie...")
        self.btn_save.configure(state="disabled")

        conversion_thread = threading.Thread(target=self._perform_conversion)
        conversion_thread.daemon = True
        conversion_thread.start()

    def _perform_conversion(self):
        pascal_code = self.pascal_editor.get_text()

        try:
            with open(self.temp_pas_path, "w", encoding="utf-8") as f:
                f.write(pascal_code)
        except Exception as e:
            self.after(0, self._ui_safe_fallback, f"Błąd przygotowania pliku tymczasowego: {str(e)}", True)
            return

        try:
            builder = ASTBuilder(self.temp_pas_path)
            tree = builder.build()

            generator = CodeGeneratorVisitor(builder.stream)
            c_code = generator.visit(tree)

            if os.path.exists(self.temp_pas_path):
                os.remove(self.temp_pas_path)

            self.after(0, self._ui_safe_success, c_code)

        except CompilerException as e:
            self.after(0, self._ui_safe_fallback, str(e), True)
        except Exception as e:
            self.after(0, self._ui_safe_fallback, f"Krytyczny błąd systemu: {str(e)}", True)

    def _ui_safe_success(self, generated_c_code: str):
        self.c_editor.set_text(generated_c_code)
        self.btn_convert.configure(state="normal", text="Konwertuj do C ⚡")
        self.btn_save.configure(state="normal")
        self._log_message("Translacja zakończona sukcesem! Kod C jest gotowy.")

    def _ui_safe_fallback(self, error_msg: str, is_error: bool = True):
        self.btn_convert.configure(state="normal", text="Konwertuj do C ⚡")
        self.btn_save.configure(state="disabled")
        self._log_message(error_msg, is_error=is_error)


if __name__ == "__main__":
    app = PascalToCConverterGUI()
    app.mainloop()