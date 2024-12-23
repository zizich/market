from django.contrib.postgres.search import SearchVector, SearchQuery, SearchRank, SearchHeadline
from django.db.models import Q
from goods.models import Products


def q_search(query):
    # проверяем поступающую информацию на значение: строка или цифра
    if query.isdigit() and len(query) <= 5:
        # если цифра, то передаем в БД id равную переданной цифры и достаем тот продукт
        return Products.objects.filter(id=int(query))

    vector = SearchVector("name", 'description')  # выбираем колонны в БД для поиска
    query = SearchQuery(query)  # передаем query (строку, вводимую для поиска)

    # тут как раз таки полученные vector и query передаем в SearchRank чтобы нашел нам наиболее подходящий ответ
    # и через фильтр с параметром rank__gt=0 указываем что результат выдаем где ранк больше 0 и сортируем в order_by
    # обратном порядке по результатам -rank
    result = (Products.objects.annotate(rank=SearchRank(vector, query)).filter(rank__gt=0).order_by("-rank"))

    # тут же полученные результаты окрашиваем в желтый цвет
    result = result.annotate(
        headline=SearchHeadline(
            "name",
            query,
            start_sel="<span style='background-color: yellow;'>",
            stop_sel="</span>",
        )
    )

    result = result.annotate(bodyline=SearchHeadline(
        "description",
        query,
        start_sel="<span style='background-color: yellow;'>",
        stop_sel="</span>",
        )
    )

    return result

    # Searching against a single field is great but rather limiting. The Entry instances we’re searching belong
    # to a Blog, which has a tagline field. To query against both fields, use a SearchVector:
    # return Products.objects.annotate(search=SearchVector("name", "description")).filter(search=query)


# TODO это неплохой вариант поиска
# в этой функции производится поиск по цифрам и нескольким словам
def q_search_test(query):
    # проверяем поступающую информацию на значение: строка или цифра
    if query.isdigit() and len(query) <= 5:
        # если цифра, то передаем в БД id равную переданной цифры и достаем тот продукт
        return Products.objects.filter(id=int(query))

    # если это слово или предложение, то сначала разделяем его через итерацию строки
    keywords = [word for word in query.split() if len(word) > 2]

    # функция для упрощения запроса в БД несколькими параметрами
    q_objects = Q()

    # перебираем полученный лист и передаем в экземпляр Q
    for token in keywords:
        # description__icontains = token: Это условие поиска. Оно означает, что поле description должно содержать
        # значение token, при этом регистр символов не имеет значения из-за использования icontains.
        # - |=: Оператор "или", который объединяет текущее значение q_objects(если оно уже определено) с
        # новым условием, заданным объектом Q.

        q_objects |= Q(description__icontains=token)  # поиск по описанию продукта
        q_objects |= Q(name__icontains=token)  # поиск по наименованию продукта

    return Products.objects.filter(q_objects)
