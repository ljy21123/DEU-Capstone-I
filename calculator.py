# 테트리스 필드에 대해 점수를 평가하는 소스코드입니다.
# 작성자: 양시현
# 수정 이력:
# - 2023-10-09: 초기버전 생성

import queue

class Calculator():
    # 클래스 초기화
    # hw: 필드의 구멍 개수에 대한 가중치
    # hc: 필드의 구멍 개수
    # aw: 모든 열의 높이 합에 대한 가중치
    # ah: 모든 열의 높이 합
    # clw: 완성된 줄에 대한 가중치
    # cl: 완성된 줄의 개수
    # bw: 높이의 불연속성 대한 가중치
    # b: 높이의 불연속성
    def __init__(self, hw: float = 0.0, aw: float = 0.0, clw: float = 0.0, bw: float = 0.0):
        self.result = 0.0
    
        self.hw = hw
        self.aw = aw
        self.clw = clw
        self.bw = bw

        self.hc = 0
        self.cl = 0
        self.b = 0
        self.ah = 0
    
    # 매개변수로 전달된 필드의 점수를 계산하는 메소드
    def calculate(self, field: int):
        self.hc = self.hole_count(field)
        self.cl = self.erase_line(field)
        self.b = self.bumpiness_height(field)
        self.ah = self.aggregate_height(field)

        # print(self.hc, self.cl, self.b, self.ah)
        # print("%f = %f * %f + %f * %f + %f * %f + %f * %f"\
        #       %(self.result, \
        #         self.hw, self.hc, \
        #         self.aw, self.ah, \
        #         self.clw, self.cl, \
        #         self.bw, self.b))
        
        self.result = (self.hw * self.hc) + \
                 (self.aw * self.ah) + \
                 (self.clw * self.cl) + \
                 (self.bw * self.b)
        
        return self.result

    # 완성된 줄의 개수를 탐색 후 반환
    def erase_line(self, field: int):
        erased = 0
        ypos = len(field) - 1
        while ypos >= 0:
            if field[ypos].count(0) == 0 and field[ypos].count(9) == 2:
                erased = erased + 1
                ypos = ypos -1
            else:
                ypos = ypos -1
        return erased


    # 높이 불연속성 탐색을 위한 메소드
    def bumpiness_height(self, field: int):
        result = 0
        height = []
        # 필드의 가로 넓이 만큼 반복
        for x in range(1, len(field[0]) - 1):
            # 해당 열의 높이 0 부터 처음 블록이 나올때 까지 빈 공간 개수
            void_count = 0
            # 필드의 높이 만큼 반복
            for y in range(len(field) - 1):
                # 빈 공간이라면 카운트 +1
                if field[y][x] == 0:
                    void_count += 1
                # 블록을 만났다면
                else:
                    break
            # 전체 높이 - 빈공간 개수 - 바닥
            height.append(len(field) - void_count - 1)
        for i in range(1, len(height)):
            result += abs(height[i-1] - height[i])

        return result

    # 모든 열에 대한 높이 합 구하는 함수
    def aggregate_height(self, field: int):
        result = 0
        
        # 필드의 가로 넓이 만큼 반복
        for x in range(1, len(field[0]) - 1):
            # 해당 열의 높이 0 부터 처음 블록이 나올때 까지 빈 공간 개수
            void_count = 0
            # 필드의 높이 만큼 반복
            for y in range(len(field) - 1):
                # 빈 공간이라면 카운트 +1
                if field[y][x] == 0:
                    void_count += 1
                # 블록을 만났다면
                else:
                    break
            # 전체 높이 - 빈공간 개수 - 바닥
            result += len(field) - void_count - 1
            
        return result

    # 현재 필드의 블럭 속 구멍 개수를 탐색
    def hole_count(self, field: int):
        hole = 0

        # 블록과 빈공간을 구분하기 위한 기존 필드와 크기가 같은 boolean 타입의 2차원 배열
        h_field = [[0] * len(field[0]) for _ in range(len(field))] # y, x

        # 필드의 크기만큼 반복하며
        for y in range(len(field)):
            for x in range(len(field[0])):
                # 빈공간이 아닌곳은 True 표현
                if field[y][x] != 0:
                    h_field[y][x] = True
                else:
                    h_field[y][x] = False  

        # 너비 우선 탐색을 통해서 블록이 처음 떨어지는 곳(블록이 있다면 게임 오버인곳)을 출발 점으로
        # 갈 수 있는 곳을 모두 탐색하고(True표시) 남은 곳은(False) 구멍으로 판단  
        self.bfs(h_field)
        
        # 구멍판단 출력
        # for y in range(len(field)):
        #     print(h_field[y])  
        # print()
        
        for y in range(len(h_field)):
            for x in range(len(h_field[0])):
                if h_field[y][x] == False:
                    hole += 1

        return hole

    # 구멍 탐색에 사용될 너비탐색 메소드
    def bfs(self, h_field):
        # 탐색할 곳을 저장하는 큐 선언
        q = queue.Queue()    
        startX = len(h_field[0]) // 2
        startY = 0
        # 보통 블록이 떨어지는 공간을 처음 시작위치로 지정
        q.put((startX, startY))

        h_field [startY][startX] = True

        dx = [-1, 0, 1, 0] # x좌표의 좌 상 우 하
        dy = [0, -1, 0, 1] # y좌표의 좌 상 우 하

        # 큐가 비어있지 않은 동안
        while not q.empty():
            # 큐의 가장 처음 값을 가져옴
            cur = q.get()  
           
            # 현재 좌표를 기준으로 4방향을 탐색
            for i in range(4):
                # 좌 상 우 하 순으로 탐색
                ny = cur[1] + dy[i]
                nx = cur[0] + dx[i]    

                # 좌표가 필드 범위를 넘어서는가?, 좌표 위치의 값이 빈공간인가?
                if 0 <= nx < len(h_field[0]) and 0 <= ny < len(h_field) and h_field[ny][nx] == False:
                    h_field[ny][nx] = True
                    q.put((nx, ny))