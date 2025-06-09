def create_image():
    with open('message.txt', 'r',encoding='utf-8') as f:
        content = f.read()

    return content

def create_system():
    with open('message.txt', 'r') as f:
        content = f.read()

    return content


def create_human():
    content = """
            와인 페어링 추천에 아래의 요리의 풍미와 와인 리뷰를 참고해 한글로 답변해ㅈ세요.
            추천된 와인이 두 개여야 하고 이를 검증한 다음에 검증이 되면
            두 개의 추천된 와인중에 가장 어울리는 와인을 추천해주세요.
            위의 두 과정을 다시 한 번 검토해서 의도대로 답변해주세요.

            '요리의 풍미:
            {dish_flavor}

            '외인 리뷰':
            {wine_reviews}
            """

    return content