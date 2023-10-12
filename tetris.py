# 테트리스의 게임 기능과 알고리즘이 구현되어있는 소스코드입니다.
# 화면의 크기, 블록의 속도, 점수, 키 이벤트, 블록 생성, 블록 이동 및 회전, 
# 충돌, 블록 파괴, 스코어 출력, 게임오버 판단, 블록 미리보기, 블록의 색,
# 시간 출력, 테트리스 알고리즘
# 작성자: 양시현
# 수정 이력:
# - 2023-09-23: 초기버전 생성
# - 2023-10-05: 분리되어 있던 테트리스 알고리즘을 함수를 테트리스에 통합
# - 2023-10-06: 시작 시간 및 현재 시간 출력
# - 2023-10-07: calculate_best_placement() 함수의 매개변수에 대한 주석 추가,
#               블럭의 2차원 배열 변환 및 출력,
#               원본 필드의 변경을 막기위한 필드 복사 추가 및 복사를 위한 copy 패키지 추가
# - 2023-10-08: 복사한 필드의 충돌판정을 위한 copied_field_is_overlapped() 함수 추가,
#               calculate_best_placement() 함수에 현재 블럭에 대한 회전 포함 블럭을 
#               놓을 수 있는 모든 경우의 수를 출력하는 코드 추가
# - 2023-10-09: 게임 필드의 평가를 위한 calculator.py import 
#               지정된 좌표로 이동하기 위한 조작을 반환하는 moveto() 추가
#               테트리스 알고리즘 완성, 현재 가중치 변수 출력, 배속 변경(-, =), 유전 세대, 개체 번호 출력,
#               main()의 가중치 매개변수 추가,
#               블록 회전시 벽을 뚫고 지나가던 버그 수정
# - 2023-10-10: 막대모양의 블록의 충돌 판정에 오류가 있던 문제 수정
# - 2023-10-12: 블록을 놓을 공간을 탐색할때 탐색 결과가 아무것도 나오지 않던 문제 수정,
#               가중치가 UI에서 잘리던 현상 수정
# - 2023-10-13: 세대출력 추가, 폰트크기 수정, main()매개변수 generation과 no추가
#               

import sys
from math import sqrt
import random

import pygame
from pygame.locals import *

from blocks import *
import calculator

import datetime

import copy


# 전역 변수
pygame.init()
# 화면 크기 설정 600x600
SURFACE = pygame.display.set_mode([610, 600])
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

# 시작한 시간을 기록합니다.
START_TIME = datetime.datetime.now()

# 점수계산을 위한 객체
CALC = None


class Block:
    # 생성자
    def __init__(self, name):
        self.turn = 0  # 블록의 현재 회전 상태
        self.type = BLOCKS[name]  # 블록의 모양과 회전 상태를 나타내는 배열
        self.data = self.type[self.turn]  # 현재 회전 상태에 해당하는 블록의 데이터를 가져옴
        self.size = int(sqrt(len(self.data)))  # 블록 크기 계산
        self.xpos = (WIDTH - self.size) // 2  # 블록의 초기 x 위치 (중앙)
        self.ypos = 0   # 블록 초기 y 위치 (맨 위)
        self.stop = 0   # 블록이 멈춰있는 시간
        self.name = name    # 블록의 타입이나 이름 저장

    def update(self):
        global BLOCK  # 현재 활성화 된 블록을 나타냄
        erased = 0
        # 블록이 다음 위치(self.xpos, self.ypos+1)에서 겹치면(다른 블록이나 테트리스 판의 경계와)
        # 그 블록은 그 위치에서 고정되고, 보드에 추가
        if is_overlapped(self.xpos, self.ypos+1, self.turn):
            for y_offset in range(self.size):
                for x_offset in range(self.size):
                    # 블록이 보드 내에 있으면
                    if ((0 <= self.xpos+x_offset < WIDTH) and
                        (0 <= self.ypos+y_offset < HEIGHT)):
                        val = self.data[y_offset*self.size + x_offset]  # 현재 상태의 블록 가져옴
                        if val != 0:
                            FIELD[self.ypos+y_offset][self.xpos+x_offset] = val # FIELD 배열에 복사 (현재 블록이 보드에 추가)
            BLOCK = get_block() # 새 블럭 생성
            erased = erase_line()   # 지워진 줄 수 저장
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

    # 겹치는 부분 확인 후 없으면 xpos,ypos 하나 감소시켜 이동
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
        if not is_overlapped(self.xpos, self.ypos, (self.turn + 1) % 4):
            self.turn = (self.turn + 1) % 4 
            self.data = self.type[self.turn]    # 블록의 새 회전 상태에 맞게 업데이트
    
    def drop(self):
        ypos = self.ypos
        # 블록이 바닥이나 다른 블록과 겹치지 않을때 까지
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
    data = BLOCK.type[turn] # 현재 블록 데이터 가져오기

    # 2차원 배열로 변환
    # data_2d = [[0 for _ in range(BLOCK.size)] for _ in range(BLOCK.size)]
    
    # for y_offset in range(BLOCK.size):
    #     for x_offset in range(BLOCK.size):
    #         data_2d[y_offset][x_offset] = data[y_offset * BLOCK.size + x_offset]

    
    # for y_offset in range(BLOCK.size):
    #     for x_offset in range(BLOCK.size):
    #         if 0 <= xpos + x_offset < len(FIELD[0]) and 0 <= ypos + y_offset < len(FIELD):
    #             if FIELD[ypos + y_offset][xpos + x_offset] == 8 or FIELD[ypos + y_offset][xpos + x_offset] == 9:
    #                 if data_2d[y_offset][x_offset] != 0:
    #                     return True 
    # return False

    # 블록 데이터 순회
    for y_offset in range(BLOCK.size):
        for x_offset in range(BLOCK.size):
            # 블록이 보드 내에 있으면
            if ((0 <= xpos+x_offset < WIDTH) and
                (0 <= ypos+y_offset < HEIGHT)):
                # 블록의 해당 부분이 빈 칸이 아니고, 보드의 해당 부분도 빈 칸이 아니면 (충돌을 의미)
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
    erased = 0  # 지워진 줄 수 저장
    ypos = HEIGHT - 1   # 검사할 줄의 y 위치 나타냄, 가장 아래부터 위로 검사
    while ypos >= 0:    # 맨 위까지 검사
        # 해당 줄에 블럭이 완전히 채워져있으면 (0: 빈칸, 9: 벽)
        if FIELD[ypos].count(0) == 0 and FIELD[ypos].count(9) == 2:
            erased = erased + 1 # 지워진 줄 수 +1
            del FIELD[ypos] # 줄 삭제
            # 새로운 줄 생성
            new_line = [0]*(WIDTH-2)
            new_line.insert(0, 9)
            new_line.append(9)
            FIELD.insert(0, new_line)
        else:
            ypos = ypos -1
    return erased

def main(play_type = 'USER', hw = None, aw = None, clw = None, bw = None, generation = 0, no = 0): # 가중치를 여기서 받는다?
    global FIELD
    global FPS
    global CALC

    # 가중치를 입력 받았다면 가중치를 반영하여 계산할 계산 객체 생성
    if hw != None and aw != None and clw != None and bw != None:
        CALC = calculator.Calculator(hw, aw, clw, bw)

    # 구멍 개수, 모든 열의 높이 합, 완성된 줄의 수, 불연속성
    #CALC = calculator.Calculator(-1.5, -1.2, 1.0, -0.5)    

    global PLAY_TYPE
    PLAY_TYPE = play_type

    # 알고리즘의 계산 결과를 저장
    move = list()
    # 속도 조절을 위한 변수
    tik = 0

    global BLOCK
    if BLOCK is None:
        BLOCK = get_block()

    # 게임 점수(라인)
    score = 0
    # 폰트 생성
    smallfont = pygame.font.SysFont(None, 36)
    timefont = pygame.font.SysFont("malgungothic", 16)
    wfont = pygame.font.SysFont("malgungothic", 11)
    genefont = pygame.font.SysFont("malgungothic", 22)
    largefont = pygame.font.SysFont(None, 72)
    
    # 메시지 폰트
    message_over = largefont.render("GAME OVER!!", True, (255, 255, 255))
    message_rect = message_over.get_rect()
    message_rect.center = (300, 300)
    
    

    # 게임 필드 배열 초기화
    for ypos in range(HEIGHT):
        for xpos in range(WIDTH):
            # 0 = 빈공간, 9 = 벽, 8 = 고정된 블럭
            # 양 옆에 벽을 추가
            FIELD[ypos][xpos] = 9 if xpos == 0 or xpos == WIDTH - 1 else 0
     
    # 제일 아래 바닥에 벽을 추가
    for index in range(WIDTH):
        FIELD[HEIGHT-1][index] = 9     

    # 경과 시간 출력을 위한 변수
    current_time = datetime.datetime.now()
    last_update_time = 0    

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
                elif key == K_EQUALS and play_type == 'AI':
                    if  FPS < 200:
                        FPS += 10
                elif key == K_MINUS and play_type == 'AI':
                    if 20 < FPS:
                        FPS -= 10

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
                return score
        
            else: 
                if len(move) == 0:
                    move = calculate_best_placement(FIELD, BLOCK)
                else:
                        # 한 프레임에 블록 처리하기
                        for _ in range(len(move)):
                        # 프레임 단위로 처리
                        #tik = tik + 1
                        #if tik > FPS*0 :
                            tik = 0
                            key = move.pop(0)
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
        
        global BLOCK_QUEUE
        ymargin = 0
        for next_block in BLOCK_QUEUE[0:3]:
            ymargin +=1 
            for ypos in range(next_block.size):
                for xpos in range(next_block.size):
                    value = next_block.data[xpos+ypos*next_block.size]
                    pygame.draw.rect(SURFACE, COLORS[value],
                                     (xpos*15+460, ypos*15+75*ymargin,
                                      15,15))
        
        # 점수 출력
        # 점수 자리수 설정
        score_str = str(score).zfill(6)
        # 스코어 폰트 및 색상 설정
        score_image = smallfont.render(score_str, True, (180, 180, 180))
        #점수 출력 자리 설정
        SURFACE.blit(score_image, (500, 30))

        # 시작 시간 출력
        # 현재 시간 변수
        global START_TIME
        # 문자열 변환
        time_str = START_TIME.strftime("시작 시간: %Y.%m.%d %H:%M:%S")
        time_image = timefont.render(time_str, True, (180, 180, 180))
        SURFACE.blit(time_image, (335, 500))
        
        # 현재 시간
        # 1초(1000ms)마다 시간 업데이트
        if pygame.time.get_ticks() - last_update_time >= 1000:  # 1000 밀리초(1초)마다        
            current_time = datetime.datetime.now()
            last_update_time = pygame.time.get_ticks()

        time_str = current_time.strftime("현재 시간: %Y.%m.%d %H:%M:%S")
        time_image = timefont.render(time_str, True, (180, 180, 180))
        SURFACE.blit(time_image, (335, 520))

        if play_type == 'AI':
            ge_str = '현재 세대: ' + str(generation)
            ge_image = genefont.render(ge_str, True, (180, 180, 180))
            SURFACE.blit(ge_image, (335, 330))
            
            in_str = '개체 번호: ' + str(no)
            in_image = genefont.render(in_str, True, (180, 180, 180))
            SURFACE.blit(in_image, (335, 370))

            hw_str = '구멍에 대한 가중치: ' + str(hw)
            hw_image = wfont.render(hw_str, True, (180, 180, 180))
            SURFACE.blit(hw_image, (335, 410))

            aw_str = '총 높이에 대한 가중치: ' + str(aw)
            aw_image = wfont.render(aw_str, True, (180, 180, 180))
            SURFACE.blit(aw_image, (335, 430))

            clw_str = '완성된 줄에 대한 가중치: ' + str(clw)
            clw_image = wfont.render(clw_str, True, (180, 180, 180))
            SURFACE.blit(clw_image, (335, 450))

            bw_str = '높이 불연속성에 대한 가중치: ' + str(bw)
            bw_image = wfont.render(bw_str, True, (180, 180, 180))
            SURFACE.blit(bw_image, (335, 470))

            fps_str = '배속: ' + str(FPS) + 'FPS'
            fps_image = timefont.render(fps_str, True, (180, 180, 180))
            SURFACE.blit(fps_image, (335, 550))



        # 화면 업데이트
        pygame.display.update()
        # 프레임 설정
        FPSCLOCK.tick(FPS)

# 복사필드의 충돌 판정 true = 충돌, false = 충돌x
def copied_field_is_overlapped(xpos, ypos, turn, field):
    data = BLOCK.type[turn]
    for y_offset in range(BLOCK.size):
        for x_offset in range(BLOCK.size):
            if ((0 <= xpos+x_offset < WIDTH) and
                (0 <= ypos+y_offset < HEIGHT)):
                if ((data[y_offset*BLOCK.size + x_offset] != 0) and
                    (field[ypos+y_offset][xpos+x_offset] != 0)):
                    return True
    return False


# 블록을 놓을 위치를 계산하는 알고리즘 함수
def calculate_best_placement(FIELD, BLOCK: Block):
    # FIELD: 현재 테트리스 게임판 정보를 가진 2차원 배열입니다.
    # 놓을 위치를 계산할때 원본을 훼손하면 안 되기 때문에 아래와 같이 복사하여 연산해야 합니다.
    # copy 패키지를 이용하여 배열 복사
    copied_field = copy.deepcopy(FIELD)

    # 블록 또한 복사
    copied_block = Block(BLOCK.name)
    
    # 계산을 위한 객체
    global CALC

    # BLOCK: 현재 움직이고 있는 다음과 같은 블록의 정보들을 가지고 있습니다.
    # BLOCK.turn: 블록의 회전 상태를 나타내며 모든 블록은 총 4가지 상태(0 ~ 3)를 가지고 있습니다.
    # BLOCK.data: 현재 모습의(회전한) 블럭 정보(1차원 배열)을 저장하는 변수 
    # 아래와 같이 블럭의 회전 모습을 변경할 수 있습니다.
    # BLOCK.turn = i 
    # BLOCK.data = BLOCK.type[BLOCK.turn] 
    # Block.size: 현재 블록의 길이(총길이의 제곱근) 정보를 가지는 변수 int(sqrt(len(self.data)))
     


    # 블록을 놓을 위치로 가기위한 조작을 반환하는 배열
    # 예 movements.append(K_LEFT) 블록을 왼쪽으로 이동
    # movements.append(K_SPACE) 지금 위치에서 가장 아래로 블록을 이동시킨다
    movements = []
    
    # 각 블럭의 회전 상태와 배치 경우에 따른 점수 평가를 저장할 배열
    score_list = []

    # 블록의 상태는 1차원 배열로 되어있기 떄문에 2차원 배열로 변환
    # 2차원 배열로 변환된 블럭(회전한 모습 포함 4종류)를 저장할 3차원 배열
    block_list = []

    # 현재 블록의 모든 형태(회전한 4종류)를 반복
    for i in range(len(copied_block.type)):
        # 변환할 블럭의 모양을 설정
        copied_block.turn = i
        copied_block.data = BLOCK.type[copied_block.turn] 

        # 현재 블럭을 2차원 배열로 변환
        block = list(copied_block.data)
        # 1차원 배열로 되어있는 현재 블럭의 총길이의 제곱근을 구해
        # 2차원 배열로 변환하였을 때의 가로 길이를 구한다
        width = int(sqrt(len(copied_block.data)))

        # 구한 길이만큼 1차원 배열을 잘라서 저장
        temp_block_list = []
        for i in range(0, len(copied_block.data), width):
            row = block[i:i + width]
            temp_block_list.append(row)
        
        block_list.append(temp_block_list)


    # 저장된 블럭을 출력합니다. 
    #for i in range(len(BLOCK.type)):
    # for i in range(1):
    #     for j in range(len(block_list[i])):
    #         for k in range(len(block_list[i][j])):
    #             if block_list[i][j][k] != 0:
    #                 print('◼', end='')
    #             else:
    #                 print('◻',end='')
                
    #         print()
    #     print()

    # 모든 위치 계산
    # 블록의 초기 위치는 x=4 y=0
    # 계산식 = (WIDTH - self.size)//2

    # 현재 블록의 모든 회전형태를 반복
    for i in range(len(copied_block.type)):
        # 블록의 회전 형태 변환
        copied_block.turn = i
        copied_block.data = copied_block.type[copied_block.turn] 
        copied_block.xpos = (WIDTH - copied_block.size) // 2
        copied_block.ypos = 0
        
        # 반복문이 한번이라도 작동하였는지 체크를 위한 변수
        c = False
        # 현재 블록을 가장 왼쪽으로 옮긴 후 오른쪽으로 1칸씩 이동
        # 가장 왼쪽으로 이동/ 충돌 판정이 False(충돌 x인 동안)
        while not copied_field_is_overlapped(copied_block.xpos-1, copied_block.ypos, copied_block.turn, copied_field): 
            copied_block.xpos = copied_block.xpos - 1
            c = True

        # 반복문이 한번이라도 동작 했다면 반복문을 위해 한번 더 감소
        if c:
            copied_block.xpos = copied_block.xpos - 1
        # 오른쪽으로 이동
        while not copied_field_is_overlapped(copied_block.xpos+1, copied_block.ypos, copied_block.turn, copied_field):
            # 블록의 위치를 오른쪽으로 이동 시킨다
            copied_block.xpos = copied_block.xpos + 1
            # 필드 초기화
            # copy 패키지를 이용하여 배열 복사
            copied_field = copy.deepcopy(FIELD)
            # 높이 계산
            ypos = copied_block.ypos
            while not copied_field_is_overlapped(copied_block.xpos, ypos+1, copied_block.turn, copied_field):
                if ypos > len(copied_field):
                    print(copied_block.xpos, copied_block.turn, copied_block.data ,copied_field)
                    print(copied_block.data, '에러발생')
                    sys.exit(1)
                ypos = ypos + 1
            # 현재 모양의 블록을 게임 필드에 반영
            for i in range(copied_block.size):
                for j in range(copied_block.size):
                    # indexerror를 방지하기 위해 블록만 반영
                    if block_list[copied_block.turn][i][j] != 0:
                        copied_field[ypos + i][copied_block.xpos + j] += block_list[copied_block.turn][i][j]

            # 블록의 x좌표, 회전 형태, 점수 저장            
            data = (copied_block.xpos, copied_block.turn % 4, CALC.calculate(copied_field))
            score_list.append(data)


    # calculator클래스 메서드 테스트
    # print('현재 필드의 지울 라인 수: %d' %CALC.erase_line(copied_field))
    # print('구멍 개수: %d' %CALC.hole_count(copied_field))
    # print('필드의 총 높이: %d' % CALC.aggregate_height(copied_field))            
    # print('불연속성: %d' %CALC.bumpiness_height(copied_field))
    # print('점수: %f'% CALC.calculate(copied_field))

    # 모든 경우의 수에 대한 점수 계산
    # print(score_list)
    
    # 점수 리스트에 들어있는 튜플의 3번째 값(score)을 기준으로 가장 높은 튜플을 가져온다
    if score_list:
        height_score = max(score_list, key=lambda x: x[2])
        # 가장 높은 점수를 받은 위치로 이동하는 조작을 반환받는다. 
        moveto(height_score, movements)
    else:
        # 필드에 더이상 블록을 놓을 수 있는 곳이 없을때 오류가 발생합니다.
        # 그냥 제자리에서 떨어지도록 합니다.
        height_score = ((WIDTH - copied_block.size) // 2, 0, 1)
        moveto(height_score, movements)

        # 가끔씩 왜인지 모를 버그로 인해서 score_list가 비어있는 경우가 발생합니다.(거의 1000번에 1번꼴)
        # 버그 원인을 찾으려고 해도 버그 자체가 거의 안일어나서 수정이 힘듭니다, 
        # 버그가 일어나면 일어난 필드와 연산중인 블록의 값을 기록해주세요!
        # print("왜 비었지? testris.py 587줄 주석 확인")
        # print(copied_block.data)
        # print(copied_field)
    #print(height_score)
   
    # 현재 필드의 모양을 콘솔에 출력
    # for i in range(len(copied_field)):
    #     for j in range(len(copied_field[i])):
    #         if copied_field[i][j] == 9:
    #             pass
    #             #print('9', end='')
    #         elif copied_field[i][j] == 0:   
    #             print('◻', end='')
    #         else:
    #             print('◼', end='')
    #     print()
    # print()          

    # 출력 속도 조절
    #time.sleep(2)
    #sys.exit(0)
    return movements


def moveto(height_score, movements: list):
    global BLOCK
    #print(BLOCK.xpos)
    
    xpos = BLOCK.xpos - height_score[0]
    
    # 블럭의 회전
    for _ in range(height_score[1]):
        movements.append(K_UP)

    # 좌우이동
    # 좌표 차이만큼 반복
    for _ in range(abs(xpos)):
        # xpos가 음수인 경우 오른쪽으로 이동
        if xpos < 0:
            movements.append(K_RIGHT)
        else:
            movements.append(K_LEFT)

    movements.append(K_SPACE)
    #print(movements)



if __name__ == '__main__':
    main()
