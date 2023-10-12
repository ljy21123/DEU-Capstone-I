# 유전알고리즘 작성을 위한 소스 코드입니다. 
# 현재에는 유전알고리즘의 기능은 구현되지는 않았으며,
# 게임이 종료되었을때 점수를 반환받아 콘솔에 출력하는 기능만 있습니다.
# 작성자: 양시현
# 수정 이력:
# 2023-10-05: 초기버전 생성
# 2023-10-10: 임의의 가중치 부여
# 2023-10-11: generate_random() 함수 추가, random 패키지 추가,
#             genetic_algorithm 함수에서 클래스로 변경


import tetris
import random

import individual

# 한 세대의 개채 수
SIZE = 10 


class Genetic_algorithm:
    def __init__(self):
        global SIZE
        for _ in range(100):
            # 구멍 개수, 모든 열의 높이 합, 완성된 줄의 수, 불연속성
            print(tetris.main('AI', -1.5, -1.2, 1.0, -0.5)) # 임시로 정한 좋은 가중치
            # print(tetris.main('AI', -1.5, -1.2, 1.0, 0)) # 안좋은 가중치
        individuals = self.generate_random(SIZE)    

        for i in range(0, SIZE):
            individuals[i].setFittness(SIZE - i)

        for i in range(len(individuals)):
            individuals[i].print()    

        # 정렬
        individuals = sorted(individuals)

        for i in range(len(individuals)):
            individuals[i].print()    

    # 매개변수 만큼의 개체를 생성하여 반환
    def generate_random(self, temp):
        individual_list = []

        for no in range(temp):
            # -0.5 ~ 0.5 사이의 랜덤 값
            hw = random.random() - 0.5
            aw = random.random() - 0.5
            clw = random.random() - 0.5
            bw = random.random() - 0.5
            individual_list.append(individual.Individual(no, hw, aw, clw, bw))

        return individual_list 


if __name__ == '__main__':
    test = Genetic_algorithm()


    