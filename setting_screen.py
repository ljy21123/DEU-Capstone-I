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

def main():
    # 초기화
    pygame.init()

    # 화면 설정
    width, height = 800, 600
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("설정 화면")

    font = pygame.font.SysFont(None, 50)
    font2 = pygame.font.SysFont("malgungothic", 40, bold=True)

    label_kor = "가중치 설정"
    label_image_kor = font2.render(label_kor, True, (255, 255, 255))


    # 버튼 생성
    buttons = [
        Button(325, 370, 150, 50, "Save", "button_1"),
        Button(280, 440, 240, 80, "Back", "button_2")
    ]


    font4 = pygame.font.SysFont("malgungothic", 20, bold=True)
    label_hw = "구멍에 대한 가중치"
    label_image_hw = font4.render(label_hw, True, (255, 255, 255))

    label_hw = "총 높이에 대한 가중치"
    label_image_aw = font4.render(label_hw, True, (255, 255, 255))

    label_hw = "완성된 줄에 대한 가중치"
    label_image_clw = font4.render(label_hw, True, (255, 255, 255))

    label_hw = "높이 불연속성에 대한 가중치"
    label_image_bw = font4.render(label_hw, True, (255, 255, 255))

    font3 = pygame.font.SysFont(None, 30)

    with open("setting.csv", "r", newline="") as file:
        reader = csv.reader(file)
        headers = next(reader)
        for row in reader:
            hw, aw, clw, bw = row

    input_text1 = hw
    input_text2 = aw
    input_text3 = clw
    input_text4 = bw
    input_box_color = (200, 200, 200)

    # 입력 상자 활성화 여부
    input_active1 = False
    input_active2 = False
    input_active3 = False
    input_active4 = False

    input_rect1 = pygame.Rect(430, 150, 270, 40)  # 입력 상자의 위치와 크기

    input_rect2 = pygame.Rect(430, 205, 270, 40)  # 입력 상자의 위치와 크기

    input_rect3 = pygame.Rect(430, 260, 270, 40)  # 입력 상자의 위치와 크기

    input_rect4 = pygame.Rect(430, 315, 270, 40)  # 입력 상자의 위치와 크기


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
                            with open("setting.csv", "w", newline="") as file:
                                writer = csv.writer(file)
                                writer.writerow(["hw", "aw", "clw", "bw"])
                                writer.writerow([input_text1, input_text2, input_text3, input_text4])
                                print("setting.csv 가중치 저장 완료")
                        elif button.action == "button_2":
                            import home_screen
                            home_screen.main()
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

                if input_rect3.collidepoint(event.pos):
                    input_active3 = not input_active3
                else:
                    input_active3 = False

                if input_rect4.collidepoint(event.pos):
                    input_active4 = not input_active4
                else:
                    input_active4 = False

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

                if input_active3:
                    if event.key == pygame.K_BACKSPACE:
                        input_text3 = input_text3[:-1]  # 백스페이스를 누르면 문자열에서 한 글자 삭제
                    else:
                        input_text3 += event.unicode  # 키 이벤트의 문자를 텍스트에 추가

                if input_active4:
                    if event.key == pygame.K_BACKSPACE:
                        input_text4 = input_text4[:-1]  # 백스페이스를 누르면 문자열에서 한 글자 삭제
                    else:
                        input_text4 += event.unicode  # 키 이벤트의 문자를 텍스트에 추가

        # 화면 업데이트
        screen.fill((43, 45, 48))

        # 라벨 위치 설정
        screen.blit(label_image_kor, (290, 70))

        screen.blit(label_image_hw, (140, 155))
        screen.blit(label_image_aw, (140, 210))
        screen.blit(label_image_clw, (140, 265))
        screen.blit(label_image_bw, (140, 320))

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

        pygame.draw.rect(screen, input_box_color, input_rect3)
        if input_active3:
            pygame.draw.rect(screen, (0, 0, 0), input_rect3, 2)
        text_surface = font3.render(input_text3, True, (0, 0, 0))
        screen.blit(text_surface, (input_rect3.x + 5, input_rect3.y + 5))

        pygame.draw.rect(screen, input_box_color, input_rect4)
        if input_active4:
            pygame.draw.rect(screen, (0, 0, 0), input_rect4, 2)
        text_surface = font3.render(input_text4, True, (0, 0, 0))
        screen.blit(text_surface, (input_rect4.x + 5, input_rect4.y + 5))


        for button in buttons:
            button.draw(screen)
        pygame.display.flip()

    # 게임 종료
    pygame.quit()
    sys.exit()


if __name__ == '__main__':
    main()