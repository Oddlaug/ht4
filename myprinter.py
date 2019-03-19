# -*- coding: utf-8 -*-


def adv_print(func):
    def wrapper(*args, **kwargs):
        s = ''.join([str(i) for i in args])
        length = len(s)
        str_start = '\n'
        str_body = s

        if 'start' in kwargs:
            str_start = kwargs['start']

        if 'max_length' in kwargs:
            if length > kwargs['max_length']:
                str_body = s[:kwargs['max_length']] + '\n' + s[kwargs['max_length']:]
            else:
                str_body = s

        new_string = str_start + str_body

        if 'in_file' in kwargs and new_string:
            try:
                with open(kwargs['in_file'], 'w', encoding='utf-8') as f:
                    f.write(new_string)
            except OSError:
                print(f'Недопустимое имя файла => {kwargs["in_file"]}')

        return func(new_string)

    return wrapper


@adv_print
def printer(*args, **kwargs):
    return print(*args, *kwargs)
