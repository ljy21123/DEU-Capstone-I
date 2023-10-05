# 메인화면을 보여줄 소스코드입니다.
# 현재에는 아무 기능도 구현되지 않았습니다.
# 작성자: 양시현
# 수정 이력:
# - 2023-09-24: 초기버전 생성

import pygame
import sys
from pygame.locals import *
import tetris

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

def main():
    pygame.init()
    pygame.display.set_caption("Pygame에서 한국어 표시하기")
    screen = pygame.display.set_mode((800, 600))
    clock = pygame.time.Clock()
    font = pygame.font.SysFont("malgungothic", 80) # 시스템 폰트 사용 시
    tmr = 0

    while True:
        key = None
        for event in pygame.event.get():
            if event.type == QUIT: # 이벤트 타입이 종료면 게임 종료
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN: # 키를 눌렀을때 만약 esc키라면 종료
                key = event.key
                if key == K_ESCAPE:
                    pygame.display.set_mode((600, 600))
                    tetris.main('AI')


        
if __name__ == '__main__':
    main()