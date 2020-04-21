from drf_yasg.openapi import Schema, TYPE_OBJECT, TYPE_STRING, TYPE_ARRAY, TYPE_INTEGER, Items, TYPE_BOOLEAN

request_for_dish = Schema(type=TYPE_OBJECT,
                          properties={
                              'name': Schema(type=TYPE_STRING, title='Название блюда'),
                              'cost': Schema(type=TYPE_INTEGER, title='Цена'),
                              'weight': Schema(type=TYPE_INTEGER, title='Вес'),
                              'composition': Schema(type=TYPE_STRING, title='Состав'),
                              'category_dish': Schema(type=TYPE_INTEGER, title='Категория блюд'),
                              'added_dish': Schema(type=TYPE_ARRAY, title='Дополнительное блюдо',
                                                   items=Items(enum={"id": TYPE_INTEGER},
                                                               type=TYPE_STRING))})

request_for_complex_dinner = Schema(type=TYPE_OBJECT,
                                    properties={
                                        'name': Schema(type=TYPE_STRING, title='Название комплексного обеда'),
                                        'dishes': Schema(type=TYPE_ARRAY, title='Блюда',
                                                         items=Items(enum={
                                                             'id': TYPE_INTEGER,
                                                             'is_remove': TYPE_BOOLEAN,
                                                             'added_dish': [{
                                                                 'id': TYPE_INTEGER,
                                                                 'is_remove': TYPE_BOOLEAN}],
                                                         }, type=TYPE_STRING))})

request_for_create_category_dish = Schema(type=TYPE_OBJECT,
                                          properties={
                                              'name': Schema(type=TYPE_STRING, title='Название категории блюда')})

request_for_update_category_dish = Schema(type=TYPE_OBJECT,
                                          properties={
                                              'name': Schema(type=TYPE_STRING, title='Название категории блюда')})
