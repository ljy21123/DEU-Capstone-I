# 유전알고리즘 작성을 위한 소스 코드입니다. 
# 현재에는 유전알고리즘의 기능은 구현되지는 않았으며,
# 게임이 종료되었을때 점수를 반환받아 콘솔에 출력하는 기능만 있습니다.
# 작성자: 양시현
# 수정 이력:
# 2023-10-05: 초기버전 생성
# 2023-10-10: 임의의 가중치 부여
# 2023-10-11: generate_random() 함수 추가, random 패키지 추가,
#             genetic_algorithm 함수에서 클래스로 변경
# 2023-10-13: 유전알고리즘 구현,
#             토너먼트 함수에서 select가 index범위에서 벗어나던 문제 해결,
#             토너먼트 함수에서 조건을 만족하지 못하고 무한반복되던 문제 해결,
#             현재 세대의 최고 점수 출력 추가
# 2023-10-14: 랜덤한 부모가 아닌 가장 높은 점수를 받은 2개의 부모를 선택하도록 토너먼트 선택 메서드 변경,
#             적합도가 0인 개체는 완전히 새로운 개체로 대체되도록 메서드 추가,
#             세대에서 가장 높은 점수를 받은 개체의 가중치를 출력하도록 변경,
#             

import math
import random

import tetris
import individual


# 한 세대의 개채 수
SIZE = 5


class Genetic_algorithm:
    def __init__(self):
        global SIZE

        # 목표 점수
        goal_score = 2000

        # 현재 가장 높은 점수
        highest_score = 0

        # 몇 세대 인지 저장하는 변수
        generation = 1
        
        # 초기 개체를 SIZE만큼 생성
        individuals = self.generate_random(SIZE)    

        # 생성된 개체를 통해 게임을 실행하여 점수를 반환 받습니다.
        for i in range(SIZE):
            individuals[i].fitness = tetris.main('AI', generation, individuals[i])

        # for _ in range(100):
        #     # 구멍 개수, 모든 열의 높이 합, 완성된 줄의 수, 불연속성
        #     print(tetris.main('AI', -1.5, -1.2, 1.0, -0.5)) # 임시로 정한 좋은 가중치
        #     print(tetris.main('AI', -1.5, -1.2, 1.0, 0)) # 안좋은 가중치
        
        # 높은 점수 순으로 정렬
        individuals = sorted(individuals)
        
        # 현재 가장 높은 점수를 저장합니다.
        highest_score = individuals[0].fitness
        print("%d세대의 최고점: %d" %(generation, highest_score))

        # 현재 세대에서 가장 높은 점수를 받은 가중치 출력
        print("최고점을 받은 개체의 가중치: ", end='')
        individuals[0].print()
        print()


        # 목표 스코어에 도달할때 까지 반복
        while goal_score > highest_score: 
            # 세대 증가
            generation += 1

            # 생성된 후보자 개체를 저장할 배열
            candidate = []

            # 적합도가 0인 개체를 모두 제거하고 새로운 개체로 변경
            self.replace_low_fitness_individuals(individuals)

            # 기존 개체군의 30%를 저장하는 변수 \ 1명 이하라면 1명으로
            size_30 = max(int(SIZE * 0.3), 1)

            # 기존의 개체들을 이용하여 기존 개체 30%만큼 새로운 개체를 생성합니다,
            for i in range(size_30):
                temp = self.tournament_selection(individuals)

                # 선택된 개체 2개를 결합하여 새로운 개체를 생성합니다.
                final_candidate = self.cross_over(temp[0], temp[1])

                # 5% 확률로 돌연변이 생성
                if random.random() < 0.05:
                    # 돌연변이를 생성합니다.
                        self.mutation(final_candidate)

                # 개체의 가중치를 정규화 합니다.
                self.normalize(final_candidate)        

                # 생성된 개체를 추가
                candidate.append(final_candidate)

            # 기존 개체군에서 적합도가 낮은 개체를 새로운 개체로 교체합니다
            self.change_individual(individuals, candidate)

            # 번호 순으로 정렬
            individuals = sorted(individuals, key=lambda x: x.no)

            # 새로운 개체군으로 새롭게 게임을 시작합니다.
            for i in range(SIZE):
                individuals[i].fitness = tetris.main('AI', generation, individuals[i])

            # 높은 점수 순으로 정렬
            individuals = sorted(individuals)

            # 현재 가장 높은 점수를 저장합니다.
            highest_score = individuals[0].fitness

            print("%d세대의 최고점: %d" %(generation, highest_score))

            # 현재 세대에서 가장 높은 점수를 받은 가중치 출력
            print("최고점을 받은 개체의 가중치: ", end='')
            individuals[0].print()
            print()

        print("목표도달!!!")
            
    # 적합도가 0인 개체를 모두 제거하고 새로운 개체로 변경
    def replace_low_fitness_individuals(self, indv:individual.Individual):
        zero_count = 0

        # 현재 개체군에서 적합도가 0인 개체수를 찾는다
        for value in indv:
            if value.fitness == 0:
                zero_count += 1
        
        # 시작 위치를 계산
        start_index = len(indv) - zero_count
        # individuals의 사이즈
        global SIZE

        # 적합도가 0인 개체 수만큼 새로운 개채 생성
        temp_indv = self.generate_random(zero_count)

        # 기존의 개체군에서 제거되는 개체의 번호를 새로운 개체에 할당
        no_list = []
        for i in range(start_index, SIZE):
            no_list.append(indv[i].no)

        result = ', '.join(map(str, no_list))
        print("제거된 개체: ", end='')
        print(result)

        for _ in range(start_index, SIZE):
            # 기존의 개체군에서 가장 적합도가 낮은 개체 제거
            indv.pop()

        # 제거된 만큼 개체를 추가
        for i in range(zero_count):
            temp_indv[i].no = no_list[i]   
            indv.append(temp_indv[i])

    # 기존의 개체 배열에서 적합도가 낮은 개체를 제거하고 새로운 개체로 대체합니다.
    def change_individual(self, individuals: individual.Individual, candidate: individual.Individual):
        # 시작 위치를 계산
        start_index = len(individuals) - len(candidate)
        # individuals의 사이즈
        global SIZE

        # candidate의 최대 index값
        candidate_size = len(candidate) - 1
        
        # 기존의 개체군에서 제거되는 개체의 번호를 새로운 개체에 할당
        #candidate[index].no = individuals[candidate_size - index].no
        no_list = []
        for i in range(start_index, SIZE):
            no_list.append(individuals[i].no)

        # 개체번호 할당을 위해서 사용하는 candidate의 인덱스
        index = 0
        for _ in range(start_index, SIZE):
            index += 1
            # 기존의 개체군에서 가장 적합도가 낮은 개체 제거
            individuals.pop()

        # 제거된 만큼 개체를 추가
        for i in range(len(candidate)):
            candidate[i].no = no_list[i]   
            individuals.append(candidate[i])
            

    # 정규화 수행
    def normalize(self, idv:individual.Individual):
        mean = math.sqrt(idv.aw * idv.aw +
                         idv.bw * idv.bw +
                         idv.hw * idv.hw +
                         idv.clw * idv.clw)
        
        idv.aw /= mean
        idv.bw /= mean
        idv.clw /= mean
        idv.hw /= mean
         
    # 돌연변이 생성 함수
    def mutation(self, candidate: individual.Individual):
        mutation = random.random() * 0.5 * 2 - 0.5
        idx = random.randint(0, 4)

        if idx == 0:
            candidate.hw += mutation
        elif idx == 1:
            candidate.aw += mutation
        elif idx == 2:
            candidate.clw += mutation
        elif idx == 3:
            candidate.bw += mutation

    # 선택된 개체 2개를 결합하여 새로운 개체를 생성하는 함수
    def cross_over(self, gene1: individual.Individual, gene2: individual.Individual):
        temp = individual.Individual(0, 
                                    gene1.hw * gene1.fitness + gene2.hw * gene2.fitness,
                                    gene1.aw * gene1.fitness + gene2.aw * gene2.fitness,
                                    gene1.clw * gene1.fitness + gene2.clw * gene2.fitness,
                                    gene1.bw * gene1.fitness + gene2.bw * gene2.fitness)
        return temp

    # 다양성을 위해 기존의 개체군에서 적합도가 0이 아닌 개체 2개를 무작위로 선택하여 반환합니다.
    def tournament_selection(self, individuals: individual.Individual):
        # 반환할 결과를 저장하는 함수
        result = []
        # 매개변수로 전달받은 리스트에서 0이 아닌 개체의 수를 저장할 변수
        zero_count = 0

        # 현재 개체군 출력
        # print()
        # print("현재 개체군 출력:")
        for value in individuals:
            if value.fitness != 0:
                zero_count += 1
            # value.print()

        # 적합도가 0이 아닌 개체수가 2 이하라면
        if zero_count < 2:
            # 개체 생성 메서드를 사용하여 새로운 개체 생성
            result = self.generate_random(2)

            # 새로 생성된 개체 정보 출력
            # print("zero가 2 미만이기 때문에 생성된 개체:")
            # 0나누기를 방지하기 위해 생성된 개체의 적합도를 최소인 1로 변경
            for a in result:
                a.fitness = 1
                # a.print()
            return result
        else:
            # 적합도 순으로 정렬된 배열에서 0이 아닌 개체 범위
            # 사이에서 2개의 랜덤한 index를 배열로 반환
            #select_list = random.sample(range(zero_count), 2)
            # 선택된 랜덤한 개체 2개를 result에 추가하여 반환
            # 테스트: 가장 높은 점수를 받은 2개를 선택
            for index in range(2):
                result.append(individuals[index])

            # 선택된 개체 2개를 출력
            # print("zero가 2 이상:")
            # for a in result:
            #     a.print()
            
        return result

    # 매개변수 만큼의 개체를 생성하여 반환
    def generate_random(self, size):
        individual_list = []

        for no in range(size):
            # -0.5 ~ 0.5 사이의 랜덤 값
            hw = random.random() - 0.5
            aw = random.random() - 0.5
            clw = random.random() - 0.5
            bw = random.random() - 0.5
            individual_list.append(individual.Individual(no + 1, hw, aw, clw, bw))

        return individual_list 


def start():
    test = Genetic_algorithm()


if __name__ == '__main__':
    test = Genetic_algorithm()


    