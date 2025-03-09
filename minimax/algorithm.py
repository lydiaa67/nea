from copy import deepcopy
import pygame
from checkers.constants import BLACK, RED, BLACK

nodes = 0  
def minimax(position, depth, max_player, game, alpha=float('-inf'), beta=float('inf')):
    print(f"Starting the run of minimax | Depth: {depth}, Max Player: {max_player}, Alpha: {alpha}, Beta: {beta}")
    global nodes
    nodes += 1  # Increment the node count (REMOVE or COMMENT OUT before production)

    # Base case: if at depth 0 or there's a winner, return the evaluation score
    if depth == 0 or position.winner() is not None:
        eval_score = position.evaluate()
        print(f"Evaluating the node | Depth: {depth}, Nodes: {nodes}, Evaluation: {eval_score}")
        return eval_score, position, 1  # Return evaluation, position, and node count

    nodes_evaluated = 0

    if max_player:  # Maximising player (RED)
        max_eval = float('-inf')
        best_move = None
        moves = get_all_moves(position, RED, game)

        print(f"\n Unsorted Moves at Depth {depth} (Max Player):")
        move_evals = [(move, move.evaluate()) for move in moves]
        for m, eval in move_evals:
            print(f"Move Eval: {eval}")
        
        move_evals.sort(key=lambda x: x[1], reverse=True)
        moves = [m[0] for m in move_evals]  # Extract sorted moves  

        print(f"\nSorted Moves at Depth {depth} (Max Player):")
        for m in moves:
            print(f"Move Eval: {m.evaluate()}")

        for move in moves:
            evaluation, _, nodes_count = minimax(move, depth-1, False, game, alpha, beta)
            nodes_evaluated += nodes_count

            if evaluation > max_eval:  # Ensure best move updates correctly
                max_eval = evaluation
                best_move = move

            alpha = max(alpha, evaluation)  # Update alpha

            print(f"Max Player | Depth: {depth} | Move Eval: {evaluation} | Alpha: {alpha} | Beta: {beta}")

            if beta <= alpha:  # Alpha-Beta Pruning
                print(f"Pruned at Depth {depth} | Alpha: {alpha}, Beta: {beta}")
                break  

        print(f"Total nodes evaluated at depth {depth}: {nodes_evaluated}")
        return max_eval, best_move, nodes_evaluated

    else:  # Minimising player (BLACK)
        min_eval = float('inf')
        best_move = None
        moves = get_all_moves(position, BLACK, game)

        print(f"\n Unsorted Moves at Depth {depth} (Min Player):")
        move_evals = [(move, move.evaluate()) for move in moves]
        for m, eval in move_evals:
            print(f"Move Eval: {eval}")

        move_evals.sort(key=lambda x: x[1])
        moves = [m[0] for m in move_evals]  # Extract sorted moves  

        print(f"\n Sorted Moves at Depth {depth} (Min Player):")
        for m in moves:
            print(f"Move Eval: {m.evaluate()}")

        for move in moves:
            evaluation, _, nodes_count = minimax(move, depth-1, True, game, alpha, beta)
            nodes_evaluated += nodes_count

            if evaluation < min_eval:  # Ensure best move updates correctly
                min_eval = evaluation
                best_move = move

            beta = min(beta, evaluation)  # Update beta

            print(f"Min Player | Depth: {depth} | Move Eval: {evaluation} | Alpha: {alpha} | Beta: {beta}")

            if beta <= alpha:  # Alpha-Beta Pruning
                print(f"Pruned at Depth {depth} | Alpha: {alpha}, Beta: {beta}")
                break  

        print(f"Total nodes evaluated at depth {depth}: {nodes_evaluated}")
        return min_eval, best_move, nodes_evaluated


def simulate_move(piece, move, board, game, skip):
    board.move(piece, move[0], move[1])
    if skip:
        board.remove(skip)

    return board


def get_all_moves(board, color, game):
    moves = []

    for piece in board.get_all_pieces(color):
        valid_moves = board.get_valid_moves(piece)

        for move, skip in valid_moves.items():
            temp_board = deepcopy(board)
            temp_piece = temp_board.get_piece(piece.row, piece.col)
            new_board = simulate_move(temp_piece, move, temp_board, game, skip)

            moves.append((new_board, skip))  # Store as tuple (board, skip)

    # Ensure `moves` contains only Board objects before returning
    return [move[0] if isinstance(move, tuple) else move for move in moves]



def draw_moves(game, board, piece): #to draw out every move and its implications that the ai considers before actually making it
    valid_moves = board.get_valid_moves(piece)
    board.draw(game.win)
    pygame.draw.circle(game.win, (0,255,0), (piece.x, piece.y), 50, 5) #colour BLACK
    #game.draw_valid_moves(valid_moves.keys())
    pygame.display.update()
    pygame.time.delay(100) #- in ms 


