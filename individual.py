# 유전알고리즘에 사용되는 개체 정보(가중치, 개체 번호)를 저장하는 클래스입니다.
# 작성자: 양시현
# 수정 이력:
# 2023-10-11: 초기버전 생성


class Individual():
    # 클래스 초기화
    # fittness: 적합도(해당 유전자의 게임 점수)
    # no: 개체 번호
    # hw: 필드의 구멍 개수에 대한 가중치
    # aw: 모든 열의 높이 합에 대한 가중치
    # clw: 완성된 줄에 대한 가중치
    # bw: 높이의 불연속성 대한 가중치
    def __init__(self, no, hw, aw, clw, bw):    
        self.fittness = 0
        self.no = no
        self.hw = hw
        self.aw = aw
        self.clw = clw
        self.bw = bw

    def print(self):
        print(self.fittness, self.hw, self.aw, self.clw, self.bw)

    def setFittness(self, fittness):
        self.fittness = fittness

    # 정렬을 위한 메서드
    def __lt__(self, other):
        return self.fittness < other.fittness   
    

if __name__ == '__main__':
    test = Individual(1,2,3,4,5)
    test.print()