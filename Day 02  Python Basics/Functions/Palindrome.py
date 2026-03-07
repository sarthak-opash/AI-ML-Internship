def isPalindrome(n):
    reverse = 0
    temp = abs(n)
    while temp != 0:
        reverse = (reverse * 10) + (temp % 10)
        temp = temp // 10
        return (reverse==abs(n))

if __name__ == "__main__":
    n = 1
    if isPalindrome(n) == True:
        print("Palindrome Number")
    else:
        print("Not Palindrome Number")