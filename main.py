import random
import time
DEPTH = 2
EMPTY_WEIGHT = 500
SNAKE_WEIGHT = [
    [160, 15, 14, 13],
    [9, 10, 11, 12],
    [8, 7, 6, 5],
    [1, 2, 3, 4],
]

board = [
    [0, 2, 0, 2],
    [2, 0, 0, 2],
    [0, 0, 0, 0],
    [4, 4, 0, 0],
]


def print_board(board):#打印棋盘
    print("+------"*4 + "+")
    for row in board:
        line = "|"
        for value in row:
            if value != 0:
                line += str(value).center(6) + "|"
            else:
                line += "      |"
        print(line)
        print("+------" *4 +"+")
   
        
def count_empty(board): #数棋盘上空格的数量
    empty = 0
    for row in board:
        for value in row:
            if value==0:
                empty += 1
    return empty

                 
def empty_positions(board):#返回棋盘上的空位坐标列表
    empty_list = []
    for r, row in enumerate(board):
        for c, value in enumerate(row):
            if value == 0:
                empty_list.append((r,c))
    return empty_list

def compress_row(row):#向左压缩一行返回压缩后的行
    new_row =[]
    length = len(row)
    for value in row:
        if value != 0:
            new_row.append(value)
    while len(new_row) < length:
        new_row.append(0)
    return new_row

def merge_row(compressed_row):#向左合并一行返回合并后的行和得分
    new_row = []
    gained = 0
    length =len(compressed_row)
    i = 0
    while i<length:
        if compressed_row[i]!=0 and  i+1<length and compressed_row[i] == compressed_row[i+1]:
            new_row.append(compressed_row[i]*2)
            gained += compressed_row[i]*2
            i += 2
        else:
            new_row.append(compressed_row[i])
            i += 1 
    while len(new_row) < length:
        new_row.append(0)
    return new_row, gained

def move_row_left(row):#对一行进行左操作
    return merge_row(compress_row(row))       


def move_row_right(row):
    new_row, gained = move_row_left(list(reversed(row)))
    return list(reversed(new_row)), gained


def move_left(board):#对棋盘进行左操作,但是不进行生成新方块
    new_board = []
    total_gained = 0
    for row in board:
        new_row, gained = move_row_left(row)
        new_board.append(new_row)
        total_gained += gained
    return new_board, total_gained


def move_right(board):
    new_board = []
    total_gained = 0
    for row in board:
        new_row, gained =move_row_right(row)
        new_board.append(new_row)
        total_gained += gained
    return new_board,total_gained


def transpose(board):#对棋盘进行横纵坐标的置换返回棋盘
    new_board = []
    for c in range(len(board)):
        new_row = []
        for r in range(len(board)):
            new_row.append(board[r][c])
        new_board.append(new_row)
    return new_board 

def move_up(board):
    new_board,total_gained =move_left( transpose(board))
    return transpose(new_board), total_gained

def move_down(board):
    new_board, total_gained =move_right(transpose(board))
    return transpose(new_board), total_gained

def has_legal_move(board):#判断是否有可以行动的方向
    moved_left, _ = move_left(board)
    moved_right, _ = move_right(board)
    moved_up, _ = move_up(board)
    moved_down, _ = move_down(board)

    return (
        moved_left != board
        or moved_right != board
        or moved_up != board
        or moved_down != board
    )

    
def copy_board(board):#复制棋盘并且输出一个一模一样的新棋盘
    return [row[:] for row in board]


def spawn_tile(board):#生成新数字
    positions = empty_positions(board)
    if positions:
        new_board = copy_board(board)
        r,c =random.choice(positions)
        new_board[r][c] = random.choices([2,4], weights = [0.9,0.1], k =1)[0]
        return new_board
    else:
        return board
    

def game_over(board):#判断游戏是否结束
    return not has_legal_move(board)

def new_game():#创造一个可以游戏的棋盘
    board = [[0]*4 for _ in range(4)] 
    for _ in range(2):
        board = spawn_tile(board)
    return board

    

MOVES = {
    "a":  move_left,
    "d" : move_right,
    "w"  :move_up,
    "s"  :move_down,
}


def play():
    board = new_game()
    score = 0
    print("游戏开始:")
    print_board(board)
    print("当前分数",score)
    
    while True:
        if not has_legal_move(board):
            print("\n")
            print("游戏结束, 你的分数是:",score)
            break
        else:
            cmd = input("方向 (w/a/s/d), q 退出: ").strip().lower()
            if cmd == "q":
                print("\n")
                print("已退出, 你的分数是: ",score)
                break
            elif cmd in MOVES:
                new_board, gained = MOVES[cmd](board)
                if new_board != board:
                    score += gained
                    board = new_board
                    board =spawn_tile(board)
                    print("\n")
                    print_board(board)
                    print("得分: ",score)
                else:
                    print("这个方向不能移动")
            else:
                print("\n无效输入")
                print_board(board)
                

def greedy_choose(board):#给出greedy策略的一步操作
    best_gain = -1
    best_moves = []
    
    for cmd in MOVES:
        new_board, gained = MOVES[cmd](board)
        if new_board != board:
            if gained > best_gain:
                best_gain = gained
                best_moves = [cmd]
            elif gained == best_gain:
                best_moves.append(cmd)
    if not best_moves:
        return None
    else:
        return random.choice(best_moves)

def survive_choose(board):
    best_space = -1
    move = []
    for cmd in MOVES:
        new_board, _ = MOVES[cmd](board)
        if new_board==board:
            continue
        space = count_empty(new_board)
        if space > best_space:
            move = [cmd]
            best_space = space
        elif space == best_space:
            move.append(cmd)
    if move:
        return random.choice(move)
    else:
        return None

def gsurvive_choose(board):#返回gsurvive策略下的一步行动
    best_score = -1
    move = []
    for cmd in MOVES:
        new_board, gained = MOVES[cmd](board)
        if new_board ==board:
            continue
        score = gained + EMPTY_WEIGHT*count_empty(new_board)
        if score >best_score:
            move = [cmd]
            best_score = score
        elif score == best_score:
            move.append(cmd)
    if move:
        return random.choice(move)
    else:
        return None

def snake_choose(board): #输入一个棋盘, 返回一步蛇形操作
    best_score = -1
    move= []
    for cmd in MOVES:
        new_board,_ = MOVES[cmd](board)
        if new_board == board:
            continue
        score = average_future(new_board)
        if best_score < score:
            move = [cmd]
            best_score = score
        elif best_score ==score:
            move.append(cmd)
    if move:
        return random.choice(move)
    else:
        return None      
    
def snake_search(board) :#输入一个棋盘, 进行depth层搜索, 返回depth次操作后分数最高的一步
    best_score = -1
    move = []
    for cmd in MOVES:
        new_board,_ = MOVES[cmd](board)#对每步操作都得到一个新棋盘
        if new_board == board:
            continue    #如果新棋盘和旧棋盘一样, 说明这步操作无效, 直接跳过这轮循环
        p_list = make_possibilitys(new_board)#对于每个新棋盘, 模拟新棋子刷新的位置, 得到可能的棋盘列表
        score = 0#重置每个方向的加权概率分数
        for possible_board, possible in p_list:
            score += possible*search(possible_board, DEPTH-1)#循环结束得到这一步的分数
        
        if score > best_score:
            move = [cmd]
            best_score = score
        elif score == best_score:
            move.append(cmd)
    if move:
            return random.choice(move)
    else:
            return None   
        
def random_choose(board):
    move_list = legal_moves(board)
    if move_list:
        return random.choice(move_list)       
    else:
        return None
#策略              
STRATEGIES = {
    "greedy":greedy_choose,
    "survive": survive_choose,
    "gsurvive": gsurvive_choose,
    "snake": snake_choose,
    "snake_search": snake_search,
    "random": random_choose,
}

def ai_play(): #ai自己玩并且显示在屏幕上
    board = new_game()
    score = 0
    strategy = input("输入策略名: ").strip()
    while True:
        print_board(board)
        cmd =STRATEGIES[strategy](board)
        if cmd:
            board,gained =MOVES[cmd](board)   
            score += gained
            print("当前分数: ",score)
            board =spawn_tile(board)
            
        else:
            print("游戏结束, AI分数: ",score)
            break


def test_play(choose):#ai进行一局游戏, 返回得分和最大方块
    board = new_game()
    score = 0
    turns = 0
    while True:
        cmd = choose(board)
        if cmd is None:
            break
        new_board, gained = MOVES[cmd](board)
        score += gained
        turns += 1
        board = spawn_tile(new_board)
    largest = max(max(row) for row in board)
    return score, largest, turns
    
def amount_test(): #对一个字典里的策略进行大量测试
    name = input("输入策略名: ").strip()
    text = input("输入测试次数: ").strip()
    n = int(text)
    
    choose = STRATEGIES[name]
    scores = []
    blocks = []
    turns = []
    for _ in range(n):
        score, largest , turn= test_play(choose)
        scores.append(score)
        blocks.append(largest)
        turns.append(turn)
    print("平均分：", sum(scores) / n)
    print("单局最高分：", max(scores))
    print("最大方块纪录：", max(blocks))
    print("平均游戏长度: ", sum(turns)/n)

def make_possibilitys(board):#检查未来所有的可能性并放入一个list中
    p_list = []
    empty = empty_positions(board)
    for value, possible in ((2,0.9),(4,0.1)):
        for (r, c) in empty:
            new_board = copy_board(board)
            new_board[r][c] =value
            p_list.append((new_board,possible/len(empty)))
    return p_list

def evaluate(board):#用蛇形评估一个棋盘返回分数
    score = 0
    for r, row in enumerate(board):
        for c, value in enumerate(row):
            score +=value* SNAKE_WEIGHT[r][c]
    return score

def average_future(board):#计算一个棋盘刷新后的蛇形评估的平均分数
    score_list = []
    for future, possible in make_possibilitys(board):
        score_list.append(evaluate(future)*possible)
    if score_list:
        return sum(score_list)
    else:
        return evaluate(board)
#当没执行到递归最底层时:
#对棋盘四个方向:
#统计执行这个方向后可能出现的所有棋盘
#对每个棋盘, 都进行该搜索
#这个分数应该乘这个分数出现的概率
#把这个分数加入到这层的分数和中
#对每个棋盘都得到分数和
#返回这个分数和到上一层 
#当执行到最底层时
#返回这个棋盘的分数
def search(board, depth):#输入棋盘和搜索深度n, 可以给出
    child_score = 0
    best_score = 0
    
    if not has_legal_move(board):
        return 0
    
    
    if depth != 0:
        for cmd in MOVES:
            new_board, _ = MOVES[cmd](board)
            
            if new_board == board:
                continue
            
            
            possible_list = make_possibilitys(new_board)
                
            total_child_score = 0
            for possible_board, possible in possible_list:#循环完成时, 应该得到最后一次操作后的概率平均分数
                child_score =search(possible_board,depth-1)
                child_score *= possible
                total_child_score += child_score
                
            if total_child_score > best_score:
                best_score = total_child_score
                        
        return best_score        
    else:
        return evaluate(board)
                
def legal_moves(board): #接受一个棋盘, 返回一个可以行动的列表
    legal_list = []
    for cmd in MOVES:
        new_board, _= MOVES[cmd](board)
        if new_board != board:
            legal_list.append(cmd)
        
    
    return legal_list        
    
def step(board, action):
    if action not in MOVES:
        raise ValueError("unknown action")
    
    new_board , gained = MOVES[action](board)
    if new_board == board:
        return board, 0, game_over(board), False
    
    spawn_board = spawn_tile(new_board)
    return spawn_board, gained, game_over(spawn_board), True


if __name__ == "__main__":
    amount_test()
                      

    

        
        
        