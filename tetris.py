import sys
from math import sqrt
import random

import pygame
from pygame.locals import *

from blocks import *

import tetris_algorithm

# 전역 변수
pygame.init()
# 화면 크기 설정 600x600
SURFACE = pygame.display.set_mode([600, 600])
# 필드의 크기
WIDTH = 12 # 게임 필드의 가로 길이
HEIGHT = 22 # 게임 필드의 높이
# 필드 크기만큼의 2차원 배열 선언
FIELD = [[0 for _ in range(WIDTH)] for _ in range(HEIGHT)]
# 화면 프레임관련 변수
FPSCLOCK = pygame.time.Clock()
FPS = 60
# 현재 움직이는 블록 정보
BLOCK = None
# 키를 누르고있으면 반복해서 입력되도록 하는 기능
# (키를 누른 상태로 대기해야 하는 시간, 이벤트 발생 간격)
pygame.key.set_repeat(500, 30)

# 플레이 타입을 저장한다 USER or AI
PLAY_TYPE = ''


class Block:
    def __init__(self, name):
        self.turn = 0
        self.type = BLOCKS[name]
        self.data = self.type[self.turn]
        self.size = int(sqrt(len(self.data)))
        self.xpos = (WIDTH - self.size)//2
        self.ypos = 0
        self.stop = 0

    def update(self):
        global BLOCK
        erased = 0
        if is_overlapped(self.xpos, self.ypos+1, self.turn):
            for y_offset in range(self.size):
                for x_offset in range(self.size):
                    if ((0 <= self.xpos+x_offset < WIDTH) and
                        (0 <= self.ypos+y_offset < HEIGHT)):
                        val = self.data[y_offset*self.size + x_offset]
                        if val != 0:
                            FIELD[self.ypos+y_offset][self.xpos+x_offset] = val
            BLOCK = get_block()      
            erased = erase_line()
        else: 
            if PLAY_TYPE == 'USER':
                self.stop = self.stop + 1
                # 블록 속도
                if self.stop > FPS*1 :
                    self.stop = 0
                    self.ypos = self.ypos + 1  
            elif PLAY_TYPE == 'AI':
                pass

        return erased
                                

    def draw(self):
        for index in range(len(self.data)):
            xpos = index % self.size
            ypos = index // self.size
            val = self.data[index]
            if ((0 <= ypos + self.ypos < HEIGHT) and 
                (0 <= xpos + self.xpos < WIDTH) and
                (val != 0)):
                x_pos = 25 + (xpos + self.xpos) * 25
                y_pos = 25 + (ypos + self.ypos) * 25
                pygame.draw.rect(SURFACE, COLORS[val], (x_pos, y_pos, 24, 24))
    
    def left(self):
        if not is_overlapped(self.xpos-1, self.ypos, self.turn):
            self.xpos = self.xpos - 1   
    
    def right(self):
        if not is_overlapped(self.xpos+1, self.ypos, self.turn):
            self.xpos = self.xpos + 1
    
    def down(self):
        if not is_overlapped(self.xpos, self.ypos+1, self.turn):
            self.ypos = self.ypos + 1
    
    def up(self):
        if not is_overlapped(self.xpos-1, self.ypos, (self.turn + 1) % 4):
            self.turn = (self.turn + 1) % 4 
            self.data = self.type[self.turn]
    
    def drop(self):
        ypos = self.ypos
        while not is_overlapped(self.xpos, ypos+1, self.turn):
            ypos = ypos + 1
        self.ypos = ypos
        

# 랜덤으로 뽑은 블럭들을 저장할 공간
BLOCK_QUEUE = list()

# 랜덤으로 블록 생성
def get_block():
    global BLOCK_QUEUE
    while len(BLOCK_QUEUE) < len(BLOCKS.keys()) + 1:
        new_blocks = list()
        for name in BLOCKS.keys():
            new_blocks.append(Block(name))
        random.shuffle(new_blocks)
        BLOCK_QUEUE.extend(new_blocks)
    return BLOCK_QUEUE.pop(0)

#        if block_list is None or len(block_list) == 0:
 #           block_list = list(BLOCKS.keys())
  #          random.shuffle(block_list)
   #         return Block(block_list.pop())
    #    else:
     #       return Block(block_list.pop())



# 충돌 판정 true = 충돌, false = 충돌x
def is_overlapped(xpos, ypos, turn):
    data = BLOCK.type[turn]
    for y_offset in range(BLOCK.size):
        for x_offset in range(BLOCK.size):
            if ((0 <= xpos+x_offset < WIDTH) and
                (0 <= ypos+y_offset < HEIGHT)):
                if ((data[y_offset*BLOCK.size + x_offset] != 0) and
                    (FIELD[ypos+y_offset][xpos+x_offset] != 0)):
                    return True
    return False

# 고정된 블럭의 색을 변경한다
def recolor():
    for ypos in range(HEIGHT):
        for xpos in range(WIDTH):
            if FIELD[ypos][xpos] != 9 and FIELD[ypos][xpos] != 0:
                FIELD[ypos][xpos] = 8

# 게임오버 상태인지 확인한다
def is_game_over():
    filled = 0
    for cell in FIELD[0]:
        if cell != 0:
            filled += 1
    return filled > 2

# 현재 지울 라인이 있는지 확인한다.
def erase_line():
    erased = 0
    ypos = HEIGHT - 1
    while ypos >= 0:
        if FIELD[ypos].count(0) == 0 and FIELD[ypos].count(9) == 2:
            erased = erased + 1
            del FIELD[ypos]
            new_line = [0]*(WIDTH-2)
            new_line.insert(0, 9)
            new_line.append(9)
            FIELD.insert(0, new_line)
        else:
            ypos = ypos -1
    return erased


def main(play_type = 'USER'):
    global FIELD
    
    global PLAY_TYPE
    PLAY_TYPE = play_type

    test = list()

    global BLOCK
    if BLOCK is None:
        BLOCK = get_block()

    # 게임 점수(라인)
    score = 0
    # 폰트 생성
    smallfont = pygame.font.SysFont(None, 36)
    largefont = pygame.font.SysFont(None, 72)
    message_over = largefont.render("GAME OVER!!", True, (255, 255, 255))
    message_rect = message_over.get_rect()
    message_rect.center = (300, 300)
    # 메시지
    

    # 게임 필드 배열 초기화
    for ypos in range(HEIGHT):
        for xpos in range(WIDTH):
            # 0 = 빈공간, 9 = 벽, 8 = 고정된 블럭
            # 양 옆에 벽을 추가
            FIELD[ypos][xpos] = 9 if xpos == 0 or xpos == WIDTH - 1 else 0
     
    # 제일 아래 바닥에 벽을 추가
    for index in range(WIDTH):
        FIELD[HEIGHT-1][index] = 9     


    # 게임 무한 루프를 수행
    while 1:
        # 이벤트 루프를 확인
        key = None
        for event in pygame.event.get():
            if event.type == QUIT: # 이벤트 타입이 종료면 게임 종료
                pygame.quit()
                sys.exit()
            elif event.type == KEYDOWN: # 키를 눌렀을때 만약 esc키라면 종료
                key = event.key
                if key == K_ESCAPE:
                    pygame.quit()
                    sys.exit()

        # 플레이 타입이 USER라면 키보드 입력을 기다린다.
        if play_type == 'USER':
            if is_game_over():
                SURFACE.blit(message_over, message_rect)
                
            else: 
                if key == K_UP:
                    BLOCK.up()
                elif key == K_RIGHT:
                    BLOCK.right()
                elif key == K_LEFT:
                    BLOCK.left()
                elif key == K_DOWN:
                    BLOCK.down()
                elif key == K_SPACE:
                    BLOCK.drop()

                # 2차원 배열을 그림으로 그린다
                SURFACE.fill((0, 0, 0))
                for ypos in range(HEIGHT):
                    for xpos in range(WIDTH):
                        value = FIELD[ypos][xpos]
                        pygame.draw.rect(SURFACE, COLORS[value], 
                                        (xpos*25 + 25, ypos*25 + 25, 24 ,24))
        
        #플레이 타입이 AI라면 
        elif play_type == 'AI':
            if is_game_over():
                SURFACE.blit(message_over, message_rect)
                
            else: 
                if len(test) == 0:
                    test = tetris_algorithm.calculate_best_placement(FIELD, BLOCK)
                else:
                        for _ in range(len(test)):
                            key = test.pop(0)
                            if key == K_UP:
                                BLOCK.up()
                            elif key == K_RIGHT:
                                BLOCK.right()
                            elif key == K_LEFT:
                                BLOCK.left()
                            elif key == K_DOWN:
                                BLOCK.down()
                            elif key == K_SPACE:
                                BLOCK.drop()

                # 2차원 배열을 그림으로 그린다
                SURFACE.fill((0, 0, 0))
                for ypos in range(HEIGHT):
                    for xpos in range(WIDTH):
                        value = FIELD[ypos][xpos]
                        pygame.draw.rect(SURFACE, COLORS[value], 
                                        (xpos*25 + 25, ypos*25 + 25, 24 ,24))

        # 지워진 줄 수를 반환하여 점수에 추가한다.
        erased = BLOCK.update()
        if erased > 0:
            score += erased
        # 고정된 블럭의 색을 변경한다.
        recolor()
        # 화면을 그린다.
        BLOCK.draw()


        # 다음 블록 미리보기
        """
        global BLOCK_QUEUE
        ymargin = 0
        for next_block in BLOCK_QUEUE[0:1]:
            ymargin +=1 
            for ypos in range(next_block.size):
                for xpos in range(next_block.size):
                    value = next_block.data[xpos+ypos*next_block.size]
                    pygame.draw.rect(SURFACE, COLORS[value],
                                     (xpos*15+460, ypos*15+75*ymargin,
                                      15,15))
        """
        # 점수 출력
        # 점수 자리수 설정
        score_str = str(score).zfill(6)
        # 스코어 폰트 및 색상 설정
        score_image = smallfont.render(score_str, True, (180, 180, 180))
        #점수 출력 자리 설정
        SURFACE.blit(score_image, (500, 30))

        # 화면 업데이트
        pygame.display.update()
        # 프레임 설정
        FPSCLOCK.tick(FPS)


if __name__ == '__main__':
    main()
