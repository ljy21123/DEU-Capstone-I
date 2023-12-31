# 테트리스 메인화면 소스코드
# 작성자: 김찬솔
# 수정 이력:
# 2023-10-11: 초기버전 생성
# 2023-10-12: 프로그램이 종료되지 않던 버그 수정, 
#             setting.csv에서 읽어 들인 데이터를 부동소수점 형태로 변환하지 않던 문제 수정,
#             key입력 처리를 위한 pygame.locals import 추가,
#             ESC키가 눌렸을때 프로그램이 종료되도록 기능 추가
# 2023-11-03: 옵션 추가, 모드 선택 및 시작 기능 추가


import csv

import pygame
from pygame.locals import *
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

    label_type = ""

    label_image_type = font.render(label_type, True, (255, 255, 255))

    with open("play_type.csv", "r", newline="") as file:
        reader = csv.reader(file)
        headers = next(reader)
        for row in reader:
            play_type = row[0]  # play_type 변수를 리스트에서 문자열로 수정

    input_text0 = play_type

    # 버튼 생성
    buttons = [
        Button(280, 200, 240, 80, "Run "+input_text0, "button_1"),
        Button(280, 320, 240, 80, "Setting", "button_3")
    ]


    # 게임 루프
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                #running = False
                # 프로그램 종료
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                for button in buttons:
                    if button.rect.collidepoint(pos):
                        if button.action == "button_1":
                            with open("play_type.csv", "r", newline="") as file:    #테트리스 실행 모드 확인을 위해, play_type.csv 값을 받아옴
                                reader = csv.reader(file)
                                headers = next(reader)
                                for row in reader:
                                    play_type = row[0]
                            if play_type == "AI":           #테트리스 실행 모드 확인 : AI 모드일 경우
                                print("테트리스 AI 모드 화면")
                                with open("settingNew.csv", "r", newline="") as file:
                                    reader = csv.reader(file)
                                    headers = next(reader)
                                    for row in reader:
                                        goal, individuals_size = row                            
                                import genetic_algorithm
                                game = genetic_algorithm.Genetic_algorithm(int(goal), int(individuals_size))
                                
                            elif play_type == "CUSTOM":
                                with open("setting.csv", "r", newline="") as file:
                                    reader = csv.reader(file)
                                    headers = next(reader)
                                    for row in reader:
                                        hw, aw, clw, bw = row                                    

                                import individual
                                temp = individual.Individual(0, float(hw), float(aw), float(clw), float(bw))
                                import tetris
                                game = tetris.main('AI', 0, temp)
                                screen = pygame.display.set_mode((width, height))
                            else:           #테트리스 실행 모드 확인 : 사용자 모드일 경우
                                print("테트리스 사용자 모드 화면")
                                import tetris
                                game = tetris.main()
                                # individuals = [hw, aw, clw, bw]
                                #
                                # import tetris
                                # print(tetris.main('USER', 0, individuals))


                        elif button.action == "button_2":
                            import records_screen
                            records_screen.main()

                        elif button.action == "button_3":
                            import settingNew_screen
                            settingNew_screen.main()
            elif event.type == KEYDOWN: # 키를 눌렀을때 만약 esc키라면 종료
                key = event.key
                if key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()

        # 화면 업데이트
        screen.fill((43, 45, 48))

        # 라벨 위치 설정
        screen.blit(label_image_kor, (235, 70))
        screen.blit(label_image_eng, (245, 130))


        for button in buttons:
            button.draw(screen)
        pygame.display.flip()


main()