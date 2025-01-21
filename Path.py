import os
import shutil


class Path:
    __slots__ = ("_name", "_main_path", "_small_path", "_blur_path")

    def __init__(self, base_folder: tuple, path: str) -> None:
        self._name = path
        self._main_path = os.path.join('static', *base_folder, path)
        self._small_path = os.path.join(self._main_path, 'small')
        self._blur_path = os.path.join(self._main_path, 'blur')

    @property
    def main_path(self) -> str:
        return self._main_path

    @property
    def small_path(self) -> str:
        return self._small_path

    @property
    def blur_path(self) -> str:
        return self._blur_path

    @property
    def get_paths(self) -> tuple[str, str, str]:
        return self._main_path, self._small_path, self._blur_path


class PortfolioDir(Path):
    __slots__ = ('_path',)

    def __init__(self, portfolio: str) -> None:
        super().__init__(base_folder=('media',), path=portfolio)


class UserDirectories(Path):
    __slots__ = ()

    def __init__(self, username: str):
        super().__init__(base_folder=('media', 'clients'), path=username)

    def clear_gallery(self):
        if os.path.exists(self.main_path):
            # Clearing all contents of the folder
            for filename in os.listdir(self.main_path):
                file_path = os.path.join(self.main_path, filename)
                try:
                    if os.path.isfile(file_path) or os.path.islink(file_path):
                        os.unlink(file_path)
                    elif os.path.isdir(file_path):
                        shutil.rmtree(file_path)
                        os.makedirs(file_path)
                except Exception as e:
                    print(f'Failed to delete {file_path}. Reason: {e}')
                    return {'status': 'error', 'message': f'{e}'}
            return {'status': 'success', 'message': 'Все фото были удалены.'}
        else:
            return {'status': 'warning', 'message': f'Данной папки не существует, обратитесь к администратору.'}

    def delete_img_from_gallery(self, fileName: str):
        if os.path.exists(self.main_path):
            # Перебираем все подпапки
            for root, dirs, files in os.walk(self.main_path):
                for file in files:
                    # Получаем имя файла без расширения
                    name, ext = os.path.splitext(file)
                    # Сравниваем с переданным именем файла
                    if name == fileName:
                        file_path = os.path.join(root, file)
                        try:
                            os.unlink(file_path)  # Удаление файла
                            print(f'{file_path} удален.')
                        except Exception as e:
                            print(f'Не удалось удалить {file_path}. Причина: {e}')
                            return {'status': 'error', 'message': f'{e}'}
            return {'status': 'success', 'message': f'Файл {fileName} был удален из всех папок.'}
        else:
            return {'status': 'warning', 'message': 'Данной папки не существует, обратитесь к администратору.'}

    def delete_project_path(self) -> bool:
        paths = self.get_paths
        for path in paths:
            if os.path.exists(path):
                shutil.rmtree(path)  # Удаляем директорию и все её содержимое
                return True
            else:
                return False

    def create_paths(self) -> bool:
        paths = self.get_paths
        for path in paths:
            if not os.path.exists(path):
                os.makedirs(path)
        return True

    def get_client_image_url(self):
        default_img = os.path.join('static', 'img', 'back_client.svg')  # URL по умолчанию

        # Используем next() для получения первого изображения или default_img
        image = next((f for f in os.listdir(self.small_path)
                      if f.lower().endswith(('.png', '.jpg', '.jpeg', '.webp'))), None)

        return os.path.join(self.small_path, image) if image else default_img

    # Функция возвращает размер клиентских проектов
    def count_files_and_size(self):
        file_count, total_size = 0, 0

        for item in os.listdir(self.main_path):
            item_path = os.path.join(self.main_path, item)
            if os.path.isfile(item_path):
                file_count += 1
                total_size += os.path.getsize(item_path)

        total_size_mb = round(total_size / (1024 ** 2), 2)
        if total_size_mb > 0:
            return f'{file_count} files, {total_size_mb} Mb'
        else:
            return 'Пусто'
