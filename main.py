import streamlit as st
import mysql.connector

# MySQL 연결 설정
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="31425474gg!!@@",
    database="home"
)
cursor = conn.cursor()

# 페이지 당 공지사항 개수
NOTICES_PER_PAGE = 10

# 공지사항 목록
def show_notice_list():
    st.title("공지사항 목록")
    page = st.sidebar.number_input("페이지", min_value=1, value=1)
    offset = (page - 1) * NOTICES_PER_PAGE
    
    query = "SELECT id, title FROM notices LIMIT %s OFFSET %s"
    cursor.execute(query, (NOTICES_PER_PAGE, offset))
    notices = cursor.fetchall()
    for notice in notices:
        if st.button(notice[1], key=f"notice_{notice[0]}"):
            show_notice_detail(notice[0])
    
    # 다음 페이지 버튼 생성
    query = "SELECT COUNT(*) FROM notices"
    cursor.execute(query)
    total_notices = cursor.fetchone()[0]
    total_pages = (total_notices - 1) // NOTICES_PER_PAGE + 1
    
    if page < total_pages:
        if st.button("다음 페이지", key="next_page"):
            page += 1
            st.experimental_rerun()
    elif page == total_pages:
        st.info("마지막 페이지입니다.")

# 공지사항 상세 내용
def show_notice_detail(notice_id):
    query = "SELECT title, content FROM notices WHERE id=%s"
    cursor.execute(query, (notice_id,))
    notice = cursor.fetchone()
    if notice:
        title, content = notice
        st.write(f"### {title}")
        st.write(content.replace('\n', '<br>'), unsafe_allow_html=True)  # 줄 바꿈 추가
    else:
        st.error("공지사항을 찾을 수 없습니다.")

# 메인 애플리케이션 실행
def main():
    # 공지사항 목록 표시
    show_notice_list()

if __name__ == "__main__":
    main()