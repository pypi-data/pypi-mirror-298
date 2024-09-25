from pathlib import Path
import os

table_files = ["csv", "xls", "xlsx", "xlsm", "xlsb", "odf", "ods", "odt", "db"]

template = {
    "headers": [],
    "rows": [],
}

class FileConverter:
    def get_absolute_path(self, relative_path: str):
        """Возвращает абсолютный путь исходя из текущей рабочей директории."""
        return (Path(os.getcwd()) / relative_path).resolve()
    
    def get_table(self, path: str, splitter=","):
        """Извлекает таблицу из файла.

        Args:
            path: Путь к файлу.

        Returns:
            Таблица.
        """
        if path.split(".")[-1] == "csv":
            with open(path, "r", encoding="utf-8") as f:
                data = f.read()
                headers = data.split("\n")[0].split(",")
                rows = [row.split(splitter) for row in data.split("\n")[1:] if row]
                template["headers"] = headers
                template["rows"] = rows
                return template

    def set_table(self, path: str, table: dict):
        """Записывает таблицу в файл.

        Args:
            path: Путь к файлу.
            table: Таблица.
        """
        if path.split(".")[-1] == "db":
            import sqlite3

            conn = sqlite3.connect(path)
            cur = conn.cursor()

            headers = ", ".join(table["headers"])
            cur.execute(f"CREATE TABLE IF NOT EXISTS test ({headers})")

            for row in table["rows"]:
                placeholders = ", ".join(["?" for _ in row])
                cur.execute(f"INSERT INTO test ({headers}) VALUES ({placeholders})", row)

            conn.commit()
            conn.close()

    def convert(self, input_path: str, output_path: str, splitter=","):
        """Конвертирует файлы из IVOfiles в IVOfiles.

        Args:
            input_path: Путь к файлу.
            output_path: Путь к сохраняемому файлу.
        """
        # Преобразуем относительные пути в абсолютные
        input_path = self.get_absolute_path(input_path)
        output_path = self.get_absolute_path(output_path)
        table = None
        
        if input_path.suffix[1:] in table_files:  # suffix возвращает расширение с точкой
            print(f"Converting {input_path} to {output_path}")
            table = self.get_table(str(input_path), splitter)
            
        if output_path.suffix[1:] in table_files:
            self.set_table(str(output_path), table)

        print("Завершено!")
