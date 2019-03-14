# -*- coding: utf-8 -*-


def adv_print(func):
    def wrapper(s, **kwargs):
        new_string = ''
        if 'start' in kwargs:
            start = kwargs['start'] + '\n'
        else:
            start = '\n'

        if 'mas_length' in kwargs:
            if len(s) > kwargs['mas_length']:
                new_string += s[:kwargs['mas_length']] + '\n' + s[kwargs['mas_length']:]
                new_string = start + new_string

        if 'in_file' in kwargs:
            try:
                with open(kwargs['in_file'], 'w', encoding='utf-8') as f:
                    f.write(new_string)
            except OSError:
                print(f'Недопустимое имя файла => {kwargs["in_file"]}')
        return func(new_string)

    return wrapper


@adv_print
def printer(data):
    return print(data)
