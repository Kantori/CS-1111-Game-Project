#score_record = open('scoreboard.txt', 'w')



score_rec_disp = open('scoreboard.txt', 'r')
line1 = score_rec_disp.readline().split(',')
for scores in range(len(line1)):
    line1[scores] = int(line1[scores])
line1 = sorted(line1)
print(line1)
score_rec_disp.close()