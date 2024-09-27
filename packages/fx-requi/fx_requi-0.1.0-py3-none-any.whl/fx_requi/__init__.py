# fx_requi/__init__.py

import os
import ast
import importlib.metadata
import sys

def find_imports(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
    except UnicodeDecodeError:
        try:
            with open(file_path, 'r', encoding='cp1251') as file:
                content = file.read()
        except UnicodeDecodeError:
            print(f"Не удалось прочитать файл {file_path}. Пропускаем.")
            return set()
    
    try:
        tree = ast.parse(content)
    except SyntaxError:
        print(f"Ошибка синтаксиса в файле {file_path}. Пропускаем.")
        return set()
    
    imports = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                imports.add(alias.name.split('.')[0])
        elif isinstance(node, ast.ImportFrom):
            if node.level == 0 and node.module:
                imports.add(node.module.split('.')[0])
    
    return imports

def get_installed_version(package):
    try:
        return importlib.metadata.version(package)
    except importlib.metadata.PackageNotFoundError:
        return None

def generate_requirements(directory):
    directory = directory.strip()
    if not os.path.exists(directory):
        print(f"Ошибка: Директория {directory} не существует.")
        return
    
    if not os.path.isdir(directory):
        print(f"Ошибка: {directory} не является директорией.")
        return
    
    all_imports = set()
    
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.py'):
                file_path = os.path.join(root, file)
                all_imports.update(find_imports(file_path))
    
    requirements = []
    for package in all_imports:
        version = get_installed_version(package)
        if version:
            requirements.append(f"{package}=={version}")
        else:
            print(f"Пакет {package} импортирован, но не установлен или не найден.")
    
    requirements_path = os.path.join(directory, 'requirements.txt')
    try:
        with open(requirements_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(sorted(requirements)))
        print(f"Файл requirements.txt создан в директории {directory}")
    except PermissionError:
        print(f"Ошибка: Нет прав на запись в директорию {directory}")
    except Exception as e:
        print(f"Произошла ошибка при создании файла: {e}")

def main():
    if len(sys.argv) != 2:
        print("Использование: fx_requi <путь к директории>")
        sys.exit(1)
    generate_requirements(sys.argv[1])

if __name__ == "__main__":
    main()