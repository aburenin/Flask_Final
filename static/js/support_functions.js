export function bytesToSize(bytes) {
    const sizes = ['Bytes', 'Kb', 'Mb', 'Gb', 'Tb'];
    if (!bytes) {
        return '0 Byte';
    }
    const i = parseInt(Math.floor(Math.log(bytes) / Math.log(1024)));
    return (bytes / Math.pow(1024, i)).toFixed(2) + ' ' + sizes[i];
}

export function totalsize(filesArray) {
    let totalSize = 0
    for (let file of filesArray) {
        totalSize += file.size;
    }
    return totalSize
}

export const element = (tag, classes = [], content) => {
    const node = document.createElement(tag)
    if (classes.length) {
        node.classList.add(...classes)
    }
    if (content) {
        node.textContent = content
    }
    return node
}

// Функция для удаления файла из массива, если он в нем присутствует
export async function deleteFileIfExist(fileName, array) {
  const index = array.indexOf(fileName); // Ищем индекс файла в массиве
  if (index !== -1) {
    array.splice(index, 1); // Удаляем файл из массива
  }
}

// Функция для переключения стиля display
export async function toggleDisplay(elements) {
    for (var i = 0; i < elements.length; i++) {
        if (elements[i].style.display === 'none') {
            elements[i].style.display = ''; // Устанавливаем на значение по умолчанию (удаляем inline стиль display)
        } else {
            elements[i].style.display = 'none'; // Скрываем элемент
        }
    }
}

