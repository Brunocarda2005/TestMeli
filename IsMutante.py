def detect_sequence(sequence):
    """
    Detects if there is a sequence of four or more identical characters (case-insensitive) in a given sequence.

    Parameters:
    sequence (list of str): A list of characters representing a DNA sequence. Each element is a character ('A', 'T', 'C', 'G').

    Returns:
    bool: True if a sequence of four or more identical characters is found, False otherwise.
    """
    count = 1
    for i in range(1, len(sequence)):
        if sequence[i].lower() == sequence[i - 1].lower():
            count += 1
            if count == 4:
                return True
    return False


def check_array(matrix):
    """
    Check if there are any sequences of four or more identical characters (case-insensitive) in each row of a given matrix.

    Parameters:
    matrix (list of list of str): A 2D list representing the DNA sequence matrix. Each element is a character ('A', 'T', 'C', 'G').

    Returns:
    int: The total number of rows that contain at least one sequence of four or more identical characters.
    """
    total_sequences = 0
    for row in matrix:
        if detect_sequence(row):
            total_sequences += 1
    return total_sequences


def get_diagonals(matrix):
    """
    Get all diagonals from a given 2D matrix.

    This function extracts all the diagonals (both ↘ and ↙) from the given matrix.
    Each diagonal is represented as a list of characters.

    Parameters:
    matrix (list of list of str): A 2D list representing the DNA sequence matrix. Each element is a character ('A', 'T', 'C', 'G').

    Returns:
    list of list of str: A list of lists, where each inner list represents a diagonal from the input matrix.
    """
    diagonals = []
    n = len(matrix)

    # Diagonales de ↘
    for d in range(-n + 1, n):
        diagonal = [matrix[i][i - d] for i in range(max(d, 0), min(n + d, n))]
        if len(diagonal) >= 4:
            diagonals.append(diagonal)

    # Diagonales de ↙
    for d in range(2 * n - 1):
        diagonal = [matrix[i][d - i] for i in range(max(0, d - n + 1), min(n, d + 1))]
        if len(diagonal) >= 4:
            diagonals.append(diagonal)

    return diagonals



def is_mutant(matrix):
    """
    Determine if a given DNA sequence matrix represents a mutant.

    A mutant is defined as a matrix where there are at least two sequences of four or more
    identical characters (case-insensitive) in any horizontal, vertical, or diagonal direction.

    Parameters:
    matrix (list of list of str): A 2D list representing the DNA sequence matrix. Each element is a character ('A', 'T', 'C', 'G').

    Returns:
    bool: True if the matrix represents a mutant, False otherwise.
    """
    horizontal_sequences =  check_array(matrix)
    vertical_sequences = check_array(zip(*matrix))
    diagonal_sequences = check_array(get_diagonals(matrix))

    if horizontal_sequences > 1:
        return True
    elif vertical_sequences > 1:
        return True
    elif diagonal_sequences > 1:
        return True

    total_sequences = horizontal_sequences + vertical_sequences + diagonal_sequences
    return total_sequences > 1
