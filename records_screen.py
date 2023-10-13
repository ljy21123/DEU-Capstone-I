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

    label_kor = "유전 알고리즘 기록 확인"
    label_image_kor = font2.render(label_kor, True, (255, 255, 255))

    # 버튼 생성
    buttons = [
        Button(300, 370, 200, 50, "Next Page", "button_1"),
        Button(280, 440, 240, 80, "Back", "button_2")
    ]

    font4 = pygame.font.SysFont("malgungothic", 20, bold=True)

    #label_page_num = page
    #label_image_page = font4.render(label_page_num, True, (255, 255, 255))

    label_gene_num = "세대 번호 : "
    label_image_gene = font4.render(label_gene_num, True, (255, 255, 255))

    label_individual_num = "개체 번호 : "
    label_image_individual = font4.render(label_individual_num, True, (255, 255, 255))

    label_hw = "구멍에 대한 가중치"
    label_image_hw = font4.render(label_hw, True, (255, 255, 255))

    label_aw = "총 높이에 대한 가중치"
    label_image_aw = font4.render(label_aw, True, (255, 255, 255))

    label_clw = "완성된 줄에 대한 가중치"
    label_image_clw = font4.render(label_clw, True, (255, 255, 255))

    label_bw = "높이 불연속성에 대한 가중치"
    label_image_bw = font4.render(label_bw, True, (255, 255, 255))

    label_hw_dot = ":"
    label_image_hw_dot = font4.render(label_hw_dot, True, (255, 255, 255))
    label_aw_dot = ":"
    label_image_aw_dot = font4.render(label_aw_dot, True, (255, 255, 255))
    label_clw_dot = ":"
    label_image_clw_dot = font4.render(label_clw_dot, True, (255, 255, 255))
    label_bw_dot = ":"
    label_image_bw_dot = font4.render(label_bw_dot, True, (255, 255, 255))


    label_gene_num_int = "csv_gene1"
    label_image_gene_int = font4.render(label_gene_num_int, True, (255, 255, 255))

    label_individual_num_int = "csv_indi2"
    label_image_individual_int = font4.render(label_individual_num_int, True, (255, 255, 255))

    label_hw_int = "csv_hw1"
    label_image_hw_int = font4.render(label_hw_int, True, (255, 255, 255))

    label_aw_int = "csv_aw2"
    label_image_aw_int = font4.render(label_aw_int, True, (255, 255, 255))

    label_clw_int = "csv_clw3"
    label_image_clw_int = font4.render(label_clw_int, True, (255, 255, 255))

    label_bw_int = "csv_bw4"
    label_image_bw_int = font4.render(label_bw_int, True, (255, 255, 255))



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
                            print("다음 페이지 버튼")

                        elif button.action == "button_2":
                            import home_screen
                            home_screen.main()

        # 화면 업데이트
        screen.fill((43, 45, 48))

        # 라벨 위치 설정
        screen.blit(label_image_kor, (170, 70))

        screen.blit(label_image_gene, (200, 150))
        screen.blit(label_image_individual, (450, 150))

        screen.blit(label_image_gene_int, (310, 150))
        screen.blit(label_image_individual_int, (560, 150))

        screen.blit(label_image_hw, (180, 200))
        screen.blit(label_image_aw, (180, 240))
        screen.blit(label_image_clw, (180, 280))
        screen.blit(label_image_bw, (180, 320))     #200

        screen.blit(label_image_hw_dot, (500, 200))
        screen.blit(label_image_aw_dot, (500, 240))
        screen.blit(label_image_clw_dot, (500, 280))
        screen.blit(label_image_bw_dot, (500, 320))

        screen.blit(label_image_hw_int, (520, 200))
        screen.blit(label_image_aw_int, (520, 240))
        screen.blit(label_image_clw_int, (520, 280))
        screen.blit(label_image_bw_int, (520, 320))


        for button in buttons:
            button.draw(screen)
        pygame.display.flip()

    # 게임 종료
    pygame.quit()
    sys.exit()


if __name__ == '__main__':
    main()