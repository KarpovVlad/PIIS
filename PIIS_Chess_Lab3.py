import chess
import time
import chess.engine as ce
engine = chess.engine.SimpleEngine.popen_uci(r"/Applications/Stockfish.app/Contents/MacOS/stockfish-arm64")

def evaluation(board, maxTurn):
    info = engine.analyse(board, ce.Limit(depth=1))
    if ~maxTurn:
        result = ce.PovScore(info['score'], chess.BLACK).pov(
            chess.BLACK).relative.score()
    else:
        result = ce.PovScore(info['score'], chess.WHITE).pov(
            chess.WHITE).relative.score()
    if result == None:
        result = 0
    return result

def negaMax_getMove(board, depth):
    def negaMax(board, depth, maximum):
        if depth == 0:
            return evaluation(board, maximum)
        maxValue = -1_000_000

        for legal_move in board.legal_moves:
            move = chess.Move.from_uci(str(legal_move))
            copy = board.copy()
            copy.push(move)
            value = -negaMax(copy, depth - 1, 1 - maximum)
            if value > maxValue:
                maxValue = value
        return maxValue
    maxValue = -1_000_000
    best = None

    for legal_move in board.legal_moves:
        move = chess.Move.from_uci(str(legal_move))
        copy = board.copy()
        copy.push(move)
        value = -negaMax(copy, depth, 1 - copy.turn)
        if value > maxValue:
            maxValue = value
            best = move
    return best

def negaScout_getMove(board, depth, alpha=-999999, beta=999999):
    def negaScout(board, depthIn, alpha, beta):
        if depthIn == 0:
            return evaluation(board, board.turn)
        score = -1_000_000
        n = beta
        for legal_move in board.legal_moves:
            move = chess.Move.from_uci(str(legal_move))
            copy = board.copy()
            copy.push(move)
            cur = -negaScout(copy, depthIn - 1, -n, -alpha)
            if cur > score:
                if n == beta or depthIn <= 2:
                    score = cur
                else:
                    scoreIn = -negaScout(copy, depthIn - 1, -beta, -cur)
            if score > alpha:
                alpha = score
            if alpha >= beta:
                return alpha
            n = alpha + 1
        return score

    score = -1_000_000
    best = None
    for legal_move in board.legal_moves:
        move = chess.Move.from_uci(str(legal_move))
        copy = board.copy()
        copy.push(move)
        value = -negaScout(copy, depth, alpha, beta)
        if value > score:
            score = value
            best = move
    return best

def pvs_getMove(board_instance, depth, alpha=-999999, beta=999999):
    def pvs(board, depthIn, alphaIn, betaIn):
        if depthIn == 0:
            return evaluation(board, board.turn)
        bSearch = True
        for legal_move in board.legal_moves:
            move = chess.Move.from_uci(str(legal_move))
            copy = board.copy()
            copy.push(move)
            if bSearch:
                cur = -pvs(copy, depthIn - 1, -betaIn, -alphaIn)
            else:
                cur = -pvs(copy, depthIn - 1, -alphaIn - 1, -alphaIn)
                if alphaIn < cur < betaIn:
                    cur = -pvs(copy, depthIn - 1, -betaIn, -alphaIn)
            if cur >= betaIn:
                return betaIn
            if cur > alphaIn:
                alphaIn = cur
                bSearch = False
        return alphaIn

    score = -1_000_000
    best = None
    for legal_move in board_instance.legal_moves:
        move = chess.Move.from_uci(str(legal_move))
        copy = board_instance.copy()
        copy.push(move)
        value = -pvs(copy, depth, alpha, beta)
        if value > score:
            score = value
            best = move
    return best

def negaMax_cvc(depth=1):
    a = 0
    board = chess.Board()
    while (board.is_checkmate() != True and
           board.is_fivefold_repetition() != True and
           board.is_seventyfive_moves() != True):

        start = time.time()
        if a % 2 == 0:
            print("WHITE moves")
            move = negaMax_getMove(board, depth)
        else:
            print("BLACK moves")
            move = negaMax_getMove(board, depth)
        end = time.time()

        if move == None:
            print("game finished, checkmate")
            break

        print("move:", move, "\n"
              "time:", end - start, "\n"
              "move count:", a, "\n"
              "five fold", board.is_fivefold_repetition(), "\n")

        board.push(move)
        print(board, "\n")

        a += 1
    if board.is_fivefold_repetition():
        print("game finished, fivefold")

def negaScout_cvc(depth=1):
    board = chess.Board()
    a = 0
    while (board.is_checkmate() != True and
           board.is_fivefold_repetition() != True and
           board.is_seventyfive_moves() != True):

        start = time.time()
        if a % 2 == 0:
            print("WHITE moves")
            move = negaScout_getMove(board, depth)
        else:
            print("BLACK moves")
            move = negaScout_getMove(board, depth)
        end = time.time()

        if move == None:
            print("game finished, checkmate")
            break

        print("move:", move, "\n"
              "time:", end - start, "\n"
              "move count:", a, "\n"
              "five fold", board.is_fivefold_repetition(), "\n")

        board.push(move)
        print(board, "\n")

        a += 1
    if board.is_fivefold_repetition():
        print("game finished, fivefold")

def cvc_pvs(depth=1):
    a = 0
    board = chess.Board()
    while (board.is_checkmate() != True and
           board.is_fivefold_repetition() != True and
           board.is_seventyfive_moves() != True):

        start = time.time()
        if a % 2 == 0:
            print("WHITE moves")
            move = pvs_getMove(board, depth)
        else:
            print("BLACK moves")
            move = pvs_getMove(board, depth)
        end = time.time()

        if move == None:
            print("game finished, checkmate")
            break

        print("move:", move, "\n"
              "time:", end - start, "\n"
              "move count:", a, "\n"
              "five fold", board.is_fivefold_repetition(), "\n")

        board.push(move)
        print(board, "\n")

        a += 1
    if board.is_fivefold_repetition():
        print("game finished, fivefold")

if __name__ == '__main__':
    negaMax_cvc()
    negaScout_cvc()
    cvc_pvs()
    engine.quit()
