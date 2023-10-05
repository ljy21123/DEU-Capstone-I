# 유전알고리즘 작성을 위한 소스 코드입니다. 
# 현재에는 유전알고리즘의 기능은 구현되지는 않았으며,
# 게임이 종료되었을때 점수를 반환받아 콘솔에 출력하는 기능만 있습니다.
# 작성자: 양시현
# 수정 이력:
# 2023-10-05: 초기버전 생성


import tetris

def genetic_algorithm():
    for _ in range(5):
        print(tetris.main('AI'))

genetic_algorithm()