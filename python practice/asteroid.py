# asteroids = [5,10,-5]
asteroids = [5,10,-7,3,6,-20,-4,6,87,-5]
stack = []
for val in asteroids:
    if (not stack) or val>0:
        stack.append(val)
    else:
        while True:
            peek = (stack[-1] if stack else None)
            if (peek < 0):
                stack.append(val)
                break
            elif peek == -val:
                stack.pop()
            elif peek > -val:
                break
            else:
                stack.pop()
                if (not stack):
                    stack.append(val)
                    break


print(stack)