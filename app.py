import streamlit as st
from sommeiler import describe_dish_flavor, search_wine, recommand_wine

st.title('Somelier AI')

col1, col2 = st.columns([3,1])

with col1:
    uploaded_img = st.file_uploader('요리 이미지를 업로드하세요.', type=['jpg', 'jpeg', 'png'])
    user_prompt = st.text_input('프롬프트를 입력하세요.', '이 요리에 어울리는 와인을 추천해주세요.')

with col2:
    if uploaded_img:
        st.image(uploaded_img, caption='업로드된 요리 이미지', use_container_width=True)

import base64

with col1:
    if st.button('추천하기'):
        if not uploaded_img:
            st.warning('이미지를 업로드 해 주세요.')
        else:
            with st.spinner('1단계 : 요리의 맛과 향을 분석하는 중...'):
                # 멀티 모달 모델 -> 사진의 요리의 특성을 분석
                ## 출력
                st.markdown('### 요리의 맛과 향 분석 결과')
                image_bytes = base64.b64encode(uploaded_img.read()).decode('utf-8')
                dish_flavor = describe_dish_flavor(image_bytes, query='이 요리의 맛과 향 같은 특징을 한글로 분석해주세요.')
                st.info(dish_flavor)

            
            with st.spinner('2단계 : 요리에 어울리는 와인 리뷰를 검색하는 중..'):
                # 추천 AI 동작
                # 요리 특성정보로 와인을 추천
                st.markdown('### 와인 리뷰 검색 결과')

                searched_wine = search_wine(dish_flavor)
                st.text(searched_wine['wine_reviews'])


            with st.spinner('3단계 : AI 소믈리에가 와인 페어링에 대한 추천글을 생성하는 중...'):
                # LLM응 이용해서 추천글을 생성
                st.markdown('### AI 소믈리에 와인 페어링 추천')

                wine_recommandation = recommand_wine({
                    'dish_flavor' : dish_flavor,
                    'wine_reviews' : searched_wine['wine_reviews']
                })
                st.info(wine_recommandation)


            st.success("추천이 완료되었습니다.")

# 유사도를 높이는 방법 -- 
# 추천된 와인의 이미지를 생성 또는 검색으로 출력