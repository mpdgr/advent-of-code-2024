with open('day4.txt', 'r') as file:
    matrix = file.readlines()

for i in range(len(matrix)):
    matrix[i] = matrix[i].strip()

search_word = ['X', 'M', 'A', 'S']
search_word_l = len(search_word)

total = 0


def find_XMAS(r, c):
    found = 0
    # search left
    if c >= search_word_l - 1:
        for i in range(search_word_l):
            if search_word[i] != matrix[r][c - i]:
                break
            if i == search_word_l - 1:
                found = found + 1
    # search right
    if c <= len(matrix[0]) - search_word_l:
        for i in range(search_word_l):
            if search_word[i] != matrix[r][c + i]:
                break
            if i == search_word_l - 1:
                found += 1
    # search up
    if r >= search_word_l - 1:
        for i in range(search_word_l):
            if search_word[i] != matrix[r - i][c]:
                break
            if i == search_word_l - 1:
                found += 1
    # search down
    if r <= len(matrix) - search_word_l:
        for i in range(search_word_l):
            if search_word[i] != matrix[r + i][c]:
                break
            if i == search_word_l - 1:
                found += 1
    # diagonal
    # search left up
    if c >= search_word_l - 1 and r >= search_word_l - 1:
        for i in range(search_word_l):
            if search_word[i] != matrix[r - i][c - i]:
                break
            if i == search_word_l - 1:
                found += 1
    # search right up
    if c <= len(matrix[0]) - search_word_l and r >= search_word_l - 1:
        for i in range(search_word_l):
            if search_word[i] != matrix[r - i][c + i]:
                break
            if i == search_word_l - 1:
                found += 1
    # search left down
    if c >= search_word_l - 1 and r <= len(matrix) - search_word_l:
        for i in range(search_word_l):
            if search_word[i] != matrix[r + i][c - i]:
                break
            if i == search_word_l - 1:
                found += 1
    # search right down
    if c <= len(matrix[0]) - search_word_l and r <= len(matrix) - search_word_l:
        for i in range(search_word_l):
            if search_word[i] != matrix[r + i][c + i]:
                break
            if i == search_word_l - 1:
                found += 1
    return found


# traverse the matrix
for r in range(len(matrix)):
    for c in range(len(list(matrix[r]))):
        total = total + find_XMAS(r, c)

print(f"Total: {total}")
