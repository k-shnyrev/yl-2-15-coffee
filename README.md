# yl-2-15-coffee

## Структура
- data\coffee.sqlite — sqlite база данных для хранения всей необходимой для отображения информации о кофе;
- release\coffee.exe — исполняемый файл, полученный при помощи pyinstaller;
- UI\addEditCoffeeForm.ui — интерфейс формы для создания новой записи о кофе в базе данных и изменения существующих;
- UI\main.ui — файл с интерфейсом основного окна программы;
- addEditCoffeeForm.py — файл с классом, полученным из UI\addEditCoffeeForm.ui при помощи pyuic5;
- main.py — программа для отображения информации о кофе из базы данных data\coffee.sqlite (ID, название сорта, степень обжарки, молотый/в зернах, описание вкуса, цена, объем упаковки);
- mainUI.py — файл с классом, полученным из UI\main.ui при помощи pyuic5;
- requirements.txt — файл с используемыми библиотеками.
