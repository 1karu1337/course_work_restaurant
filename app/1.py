import os
from pathlib import Path

# Конфигурация
OUTPUT_FILE = "full_project.txt"
EXCLUDE_DIRS = {
    '.git', '__pycache__', '.venv', 'venv', 'env', 
    '.idea', '.vscode', 'node_modules', 'dist', 'build'
}
EXCLUDE_FILES = {OUTPUT_FILE, '.DS_Store', 'package-lock.json'}
# Список расширений, которые стоит включать (можно дополнить)
ALLOWED_EXTENSIONS = {
    '.py', '.txt', '.md', '.json', '.yaml', '.yml', 
    '.html', '.css', '.js', '.sql', '.ini', '.cfg'
}

def get_project_structure(root_dir):
    """Генерирует строковое представление древовидной структуры проекта."""
    structure = []
    for root, dirs, files in os.walk(root_dir):
        # Удаляем исключаемые папки из обхода
        dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS]
        
        level = root.replace(root_dir, '').count(os.sep)
        indent = ' ' * 4 * level
        folder_name = os.path.basename(root)
        if folder_name:
            structure.append(f"{indent}📁 {folder_name}/")
        
        sub_indent = ' ' * 4 * (level + 1)
        for f in files:
            if f not in EXCLUDE_FILES:
                structure.append(f"{sub_indent}📄 {f}")
    return "\n".join(structure)

def main():
    root_dir = os.getcwd()
    output_path = Path(root_dir) / OUTPUT_FILE

    with open(output_path, 'w', encoding='utf-8') as outfile:
        # 1. Записываем заголовок и структуру
        outfile.write(f"PROJECT STRUCTURE:\n")
        outfile.write("=" * 50 + "\n")
        outfile.write(get_project_structure(root_dir))
        outfile.write("\n" + "=" * 50 + "\n\n")

        # 2. Обходим файлы и записываем их содержимое
        for root, dirs, files in os.walk(root_dir):
            dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS]
            
            for file in files:
                if file in EXCLUDE_FILES:
                    continue
                
                file_path = Path(root) / file
                relative_path = file_path.relative_to(root_dir)

                # Проверяем расширение
                if file_path.suffix.lower() in ALLOWED_EXTENSIONS:
                    outfile.write(f"\n{'#'*80}\n")
                    outfile.write(f"FILE: {relative_path}\n")
                    outfile.write(f"{'#'*80}\n\n")
                    
                    try:
                        with open(file_path, 'r', encoding='utf-8', errors='replace') as infile:
                            outfile.write(infile.read())
                    except Exception as e:
                        outfile.write(f"[Ошибка при чтении файла: {e}]\n")
                    
                    outfile.write("\n\n")

    print(f"Готово! Весь проект сохранен в файл: {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
