start_num = 1
end_num = 5000
word = ' '.join([str(i) for i in range(start_num,end_num+1)])
with open("numbers.txt", "w") as text_file:
    text_file.write(word)