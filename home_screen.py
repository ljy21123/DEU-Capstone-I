import csv

import pygame
import sys

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
    pygame.display.set_caption("홈 화면")

    font = pygame.font.SysFont(None, 50)
    font2 = pygame.font.SysFont("malgungothic", 40, bold=True)

    label_kor = "테트리스 알고리즘"
    label_eng = "- Tetris Algorithm -"
    # 라벨 렌더링
    label_image_kor = font2.render(label_kor, True, (255, 255, 255))

    label_image_eng = font.render(label_eng, True, (255, 255, 255))


    # 버튼 생성
    buttons = [
        Button(280, 200, 240, 80, "Run Tetris", "button_1"),
        Button(280, 320, 240, 80, "Records", "button_2"),
        Button(280, 440, 240, 80, "Setting", "button_3")
    ]


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
                            """with open("setting.csv", "r", newline="") as file:   #setting.csv를 읽어와서 hw, aw, clw, bw에 담음
                                reader = csv.reader(file)
                                headers = next(reader)
                                for row in reader:
                                    hw, aw, clw, bw = row

                                import tetris
                                for _ in range(100):
                                    print(tetris.main('AI', hw, aw, clw, bw)) #hw, aw, clw, bw를 넣은 테트리스 알고리즘 동작(값은 분명히 전달되는 거 같은데, 제대로 플레이를 하지 못함)
                                """
                            import genetic_algorithm
                            genetic_algorithm.genetic_algorithm()

                        elif button.action == "button_2":
                            print("기록 화면 버튼")
                        elif button.action == "button_3":
                            import setting_screen
                            setting_screen.main()


        # 화면 업데이트
        screen.fill((43, 45, 48))

        # 라벨 위치 설정
        screen.blit(label_image_kor, (235, 70))
        screen.blit(label_image_eng, (245, 130))

        for button in buttons:
            button.draw(screen)
        pygame.display.flip()

    # 게임 종료
    pygame.quit()
    sys.exit()


if __name__ == '__main__':
    main()