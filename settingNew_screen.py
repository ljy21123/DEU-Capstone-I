import pygame
import sys
import csv

# 버튼 클래스 정의
class Button:
    def __init__(self, x, y, width, height, text, action):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.action = action
        self.font = pygame.font.SysFont(u"\ub9d1\uc740 \uace0\ub515", 50)
        self.label = self.font.render(text, True, (0, 0, 0))

    def draw(self, surface):
        pygame.draw.rect(surface, (255, 255, 255), self.rect)
        surface.blit(self.label,
                     (self.rect.centerx - self.label.get_width() / 2, self.rect.centery - self.label.get_height() / 2))

class Button2:
    def __init__(self, x, y, width, height, text, action):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.action = action
        self.font = pygame.font.SysFont(None, 40)
        self.label = self.font.render(text, True, (255, 255, 255))

    def draw(self, surface):
        pygame.draw.rect(surface, (30, 31, 34), self.rect)
        surface.blit(self.label,
                     (self.rect.centerx - self.label.get_width() / 2, self.rect.centery - self.label.get_height() / 2))

def main():
    # 초기화
    pygame.init()
    clock = pygame.time.Clock()

    # 화면 설정
    width, height = 800, 600
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("AI 설정 화면")

    font = pygame.font.SysFont(None, 50)
    font2 = pygame.font.SysFont("malgungothic", 40, bold=True)
    font0 = pygame.font.SysFont("malgungothic", 25, bold=True)

    label_kor = "테트리스 설정"
    label_image_kor = font2.render(label_kor, True, (255, 255, 255))
    label_eng = "- AI 설정 -"
    label_image_eng = font0.render(label_eng, True, (255, 255, 255))

    # 버튼 생성
    buttons = [
        Button(325, 370, 150, 50, "Save", "button_1"),
        Button(280, 440, 240, 80, "Back", "button_2"),
        Button2(290, 310, 80, 40, "AI", "button_3"),
        Button2(430, 310, 80, 40, "User", "button_4"),
        Button2(10, 10, 200, 40, "User Setting", "button_5"),
    ]


    font4 = pygame.font.SysFont("malgungothic", 20, bold=True)
    label_hw = "목표 점수"
    label_image_hw = font4.render(label_hw, True, (255, 255, 255))

    label_hw = "한 세대당 개체 수"
    label_image_aw = font4.render(label_hw, True, (255, 255, 255))

    font3 = pygame.font.SysFont(None, 30)

    with open("settingNew.csv", "r", newline="") as file:
        reader = csv.reader(file)
        headers = next(reader)
        for row in reader:
            goal, individuals_size = row

    input_text1 = goal
    input_text2 = individuals_size
    input_box_color = (200, 200, 200)

    with open("play_type.csv", "r", newline="") as file:
        reader = csv.reader(file)
        headers = next(reader)
        for row in reader:
            play_type = row[0]  # play_type 변수를 리스트에서 문자열로 수정

    input_text0 = play_type

    # 입력 상자 활성화 여부
    input_active1 = False
    input_active2 = False

    input_rect1 = pygame.Rect(450, 160, 100, 40)  # 입력 상자의 위치와 크기
    input_rect2 = pygame.Rect(450, 215, 100, 40)  # 입력 상자의 위치와 크기

    label_preset = "사용 모드 :"
    label_image_preset = font0.render(label_preset, True, (255, 255, 255))

    text_type_AI = "AI"
    text_type_USER = "USER"

    label_type = ""

    label_type = input_text0
    label_image_type = font.render(label_type, True, (255, 255, 255))

    # 게임 루프
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                for button in buttons:
                    if button.rect.collidepoint(pos):
                        if button.action == "button_1":
                            with open("settingNew.csv", "w", newline="") as file:
                                writer = csv.writer(file)
                                writer.writerow(["goal", "individuals_size"])
                                writer.writerow([input_text1, input_text2])
                                print("settingNew.csv 저장 완료")
                        elif button.action == "button_2":
                            import home_screen
                            home_screen.main()
                        elif button.action == "button_3":
                            with open("play_type.csv", "w", newline="") as file:
                                writer = csv.writer(file)
                                writer.writerow(["play_type"])
                                writer.writerow([text_type_AI])
                                print("play_type.csv AI 모드 설정 완료")
                        elif button.action == "button_4":
                            with open("play_type.csv", "w", newline="") as file:
                                writer = csv.writer(file)
                                writer.writerow(["play_type"])
                                writer.writerow([text_type_USER])
                                print("play_type.csv 사용자 모드 저장 완료")
                        elif button.action == "button_5":
                            import setting_screen
                            setting_screen.main()

            with open("play_type.csv", "r", newline="") as file:
                reader = csv.reader(file)
                headers = next(reader)
                for row in reader:
                    play_type = row[0]
            input_text0 = play_type

            label_type = input_text0
            label_image_type = font.render(label_type, True, (255, 255, 255))

            if event.type == pygame.MOUSEBUTTONDOWN:
                # 마우스 클릭시 입력 상자 활성화
                if input_rect1.collidepoint(event.pos):
                    input_active1 = not input_active1
                else:
                    input_active1 = False

                if input_rect2.collidepoint(event.pos):
                    input_active2 = not input_active2
                else:
                    input_active2 = False

            if event.type == pygame.KEYDOWN:
                if input_active1:
                    if event.key == pygame.K_BACKSPACE:
                        input_text1 = input_text1[:-1]  # 백스페이스를 누르면 문자열에서 한 글자 삭제
                    else:
                        input_text1 += event.unicode  # 키 이벤트의 문자를 텍스트에 추가
                if input_active2:
                    if event.key == pygame.K_BACKSPACE:
                        input_text2 = input_text2[:-1]  # 백스페이스를 누르면 문자열에서 한 글자 삭제
                    else:
                        input_text2 += event.unicode  # 키 이벤트의 문자를 텍스트에 추가


        # 화면 업데이트
        screen.fill((43, 45, 48))

        # 라벨 위치 설정
        screen.blit(label_image_kor, (275, 70))
        screen.blit(label_image_eng, (335, 120))

        screen.blit(label_image_hw, (260, 165))
        screen.blit(label_image_aw, (260, 220))

        screen.blit(label_image_preset, (300, 260))
        screen.blit(label_image_type, (440, 265))


        pygame.draw.rect(screen, input_box_color, input_rect1)
        if input_active1:
            pygame.draw.rect(screen, (0, 0, 0), input_rect1, 2)
        text_surface = font3.render(input_text1, True, (0, 0, 0))
        screen.blit(text_surface, (input_rect1.x + 5, input_rect1.y + 5))

        pygame.draw.rect(screen, input_box_color, input_rect2)
        if input_active2:
            pygame.draw.rect(screen, (0, 0, 0), input_rect2, 2)
        text_surface = font3.render(input_text2, True, (0, 0, 0))
        screen.blit(text_surface, (input_rect2.x + 5, input_rect2.y + 5))

        for button in buttons:
            button.draw(screen)
        pygame.display.flip()

    # 게임 종료
    pygame.quit()
    sys.exit()


if __name__ == '__main__':
    main()