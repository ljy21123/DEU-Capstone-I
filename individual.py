# 유전알고리즘에 사용되는 개체 정보(가중치, 개체 번호)를 저장하는 클래스입니다.
# 작성자: 양시현
# 수정 이력:
# 2023-10-11: 초기버전 생성
# 2023-10-12: fettness 속성에 대한 setter, getter 생성

class Individual():
    # 클래스 초기화
    # fittness: 적합도(해당 유전자의 게임 점수)
    # no: 개체 번호
    # hw: 필드의 구멍 개수에 대한 가중치
    # aw: 모든 열의 높이 합에 대한 가중치
    # clw: 완성된 줄에 대한 가중치
    # bw: 높이의 불연속성 대한 가중치
    def __init__(self, no, hw, aw, clw, bw):    
        self._fitness = 0
        self._no = no
        self._hw = hw
        self._aw = aw
        self._clw = clw
        self._bw = bw

    def print(self):
        print(self.fitness, self.hw, self.aw, self.clw, self.bw)

    @property
    def fitness(self):
        return self._fitness
    
    @fitness.setter
    def fitness(self, value):
        self._fitness = value

    @property
    def no(self):
        return self._no
    
    @no.setter
    def no(self, value):
        self._no = value

    @property
    def hw(self):
        return self._hw
    
    @hw.setter
    def hw(self, value):
        self._hw = value
    
    @property
    def aw(self):
        return self._aw
    
    @aw.setter
    def aw(self, value):
        self._aw = value

    @property
    def clw(self):
        return self._clw
    
    @clw.setter
    def clw(self, value):
        self._clw = value

    @property
    def bw(self):
        return self._bw
    
    @bw.setter
    def bw(self, value):
        self._bw = value

    # 정렬을 위한 메서드
    def __lt__(self, other):
        return self._fitness > other.fitness   
    

if __name__ == '__main__':
    test = Individual(1,2,3,4,5)
    test.print()