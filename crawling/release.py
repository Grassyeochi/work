import pyautogui
import pyperclip
import pygetwindow as gw
import time

# 카카오톡 채팅방 이름 설정
kakao_chatroom_name = "여상윤"

# 채팅방 활성화 함수
def activate_kakao_chatroom(chatroom_name):
    try:
        windows = gw.getWindowsWithTitle(chatroom_name)
        if windows:
            kakao_window = windows[0]
            kakao_window.activate()
            time.sleep(1)
            return True
        else:
            print(f"{chatroom_name} 채팅방을 찾을 수 없습니다.")
            return False
    except Exception as e:
        print(f"창을 활성화하는 중 오류가 발생했습니다: {e}")
        return False

# 카카오톡 업로드 함수
def upload_to_kakao(title, press, link):
    if not activate_kakao_chatroom(kakao_chatroom_name):
        return

    message = f"{title}\n{press}\n{link}"
    pyperclip.copy(message)  # 메시지를 클립보드에 복사
    pyautogui.hotkey('ctrl', 'v')  # 붙여넣기
    pyautogui.press('enter')  # 메시지 전송

# "upload.txt" 파일에서 데이터 읽기
with open('upload.txt', 'r', encoding='utf-8') as file:
    news_items = file.read().strip().split("\n\n")


lines = news_items[0].split('\n')
title = lines[0].replace("제목 : ", "").strip()
link = lines[1].replace("링크 : ", "").strip()
press = lines[2].replace("언론사 : ", "").strip()

upload_to_kakao(title, press, link)

# 각 뉴스 항목을 카카오톡에 업로드
for news_item in news_items[1:]:
    lines = news_item.split('\n')
    title = lines[0].replace("제목 : ", "").strip()
    link = lines[1].replace("링크 : ", "").strip()
    press = lines[2].replace("언론사 : ", "").strip()

    user_input = input(f"다음 뉴스는 '{title}' 입니다. 업로드 할까요? (y/n): ")
    if (user_input.lower()) == 'n':
        continue
    elif (user_input.lower()) == "break":
        break
    elif (user_input.lower() == 'y'):
        upload_to_kakao(title, press, link)

