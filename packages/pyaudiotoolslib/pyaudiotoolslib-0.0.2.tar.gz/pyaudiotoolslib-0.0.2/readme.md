# AudioTools

Небольшая библиотека для обработки аудио написанная на C++ с биндингами для python

## Возможности

- Удаление щелчков из звука (эффект основан на коде из audacity)
- Нормализация звука

## Установка

Библиотека доступна на pypi

```shell
pip install pyaudiotoolslib
```

## Установка для разработки

1. Нужно создать виртуальное окружение

   Windows

   ```shell
   python -m venv venv
   venv\Script\activate
   ```

   Linux

   ```shell
   python3 -m venv venv
   source venv/bin/activate
   ```

2. Устанавливаем нужные библиотеки для сборки

   ```shell
   pip install pybind11 scikit-build-core
   ```

3. Устанавливаем сам пакет

   ```shell
   pip install -v --no-build-isolation .
   ```
