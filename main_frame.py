# 메인화면(시작화면)을 보여줄 소스코드입니다.
# 현재에는 아무 기능도 구현되지 않았습니다.
# 작성자: 양시현
# 수정 이력:
# - 2023-09-24: 초기버전 생성
# - 2023-10-07: 한글 출력 테스트를 위한 폰트 추가 및 출력 추가

import pygame
import sys
from pygame.locals import *

#import tetirs


def main():
    pygame.init()
    pygame.display.set_caption("메인화면")
    screen = pygame.display.set_mode((800, 600))
    clock = pygame.time.Clock()
    # 폰트 생성
    font = pygame.font.SysFont("malgungothic", 80)

    while True:
        key = None
        for event in pygame.event.get():
            # 이벤트 타입이 QUIT이면 프로그램 종료
            if event.type == QUIT: 
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN: # 키를 눌렀을때 만약 esc키라면 종료
                key = event.key
                if key == K_ESCAPE:
                    pygame.display.set_mode((600, 600))
                    #tetris.main('AI')
                    
        # 점수 자리수 설정
        score_str = "한글 출력"
        # 스코어 폰트 및 색상 설정
        score_image = font.render(score_str, True, (180, 180, 180))
        # 점수 출력 자리 설정
        screen.blit(score_image, (100, 100))

        # 화면 업데이트 
        pygame.display.update()
    

if __name__ == '__main__':
    main()