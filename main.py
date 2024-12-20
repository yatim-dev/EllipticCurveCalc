import argparse
import os
from pydoc import describe

from Runners.Parser import Parser


def main():
    print("*-------------------*")
    print('© 2024 Ярков Тимофей КБ-5.')
    print('Пример запуска: python main.py -i tests -o out.')
    print("*-------------------*\n")
    parser = argparse.ArgumentParser(
        add_help=False,
        description="Принимает Zp, ss, nss."
    )

    parser.add_argument('-v', '--version',
                        action='version',
                        version='elliptic curve calc 1.0',
                        help="Показать номер версии программы и выйти."
                        )
    parser.add_argument('-h', '--help',
                        action='help',
                        default=argparse.SUPPRESS,
                        help='Показать это справочное сообщение и выйти.'
                        )
    parser.add_argument('-i',
                        dest='path_input',
                        nargs='?',
                        default='input',
                        help='Путь к директории ввода (по умолчанию: input)'
                        )
    parser.add_argument('-o',
                        dest='path_output',
                        nargs='?',
                        default='output',
                        help='Путь к директории вывода (по умолчанию: output)'
                        )

    args = parser.parse_args()
    path_input = args.path_input
    path_output = args.path_output
    os.makedirs(path_output, exist_ok=True)
    try:
        for file in os.listdir(path_input):
            if os.path.isfile(os.path.join(path_input, file)):
                with open(os.path.join(path_input, file)) as f:
                    parser = Parser(enumerate(f.readlines()))
                curve, tasks = parser.parse()
                for task in tasks:
                    try:
                        task.calculate(curve)
                    except ValueError as exc:
                        print(f'Ошибка в файле: {exc.args[0]} ({file})')
                        continue
                with open(os.path.join(path_output, file), 'w') as f:
                    f.write(f'\n'.join([str(task) for task in tasks]))
                print(f'Готово: {file}')
    except FileNotFoundError:
        print('Каталог или файл не найден')


if __name__ == '__main__':
    main()
