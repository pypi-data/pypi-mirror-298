def stack():
    """
    This Python function implements a stack data structure with push and pop operations, allowing the
    user to interact with the stack by adding or removing elements based on a specified limit.
    """
    stack = []
    global counter 
    counter = 0
    def puch_operation(n):
        global counter
        if len(stack)==n:
            print("\nStack is full\nYou may choose another operation ! ")
        else:
            element = int(input("\nenter the element at {} index:".format(counter)))
            stack.append(element)
            print("\n{} has been inserted in stack".format(element))
            print("\nand the elements are :",stack)
            counter+=1
    def pop_operation():
        if stack == []:
            print("\nStack is empty\nYou may exit now or do other task ! ")
        else:
            e = stack.pop()
            print("\n{} has been removed from the stack\n".format(e))
            print("and the remaining elements are :",stack)
    n = int(input("\nenter the limit of the stack:"))
    while True:
        print("\nselect the operation 1. puch 2. pop 3. exit")
        choice = int(input("\nenter your choice:"))
        if choice==1:
            puch_operation(n)
        elif choice==2:
            pop_operation()
        elif choice==3:
            print("\nsuccessfully exit...!")
            break
        else:
            print("\nPlease enter valid choice")
            

def add_list_index_element():	
    """
    This function takes user input to create a list, then calculates the sum of digits for each element
    in the list and stores the results in a new list.
    """
    ls = []
    sum = 0
    index = 0
    sum_of_index_element = []
    size = int(input("enter the limit of list :"))
    for i in range(0,size):
        ls.append(int(input("enter the element at {} index:".format(i))))

    print()
    print("the original list are :",ls)

    for j in range(len(ls)):
        sum = 0
        while ls[j]!=0:
            rem = ls[index]%10
            sum = sum+rem
            ls[index] = ls[index]//10	
        sum_of_index_element.append(sum)
        index+=1

    print()
    print("After adding the digits of each element , the list is:",sum_of_index_element)


def find_postive_and_negative():
    """
    This Python function takes user input to create a list, then separates the positive and negative
    numbers into separate lists and calculates the sum of each.
    """
    lim = int(input("enter the limit of list : "))
    ls = []
    for i in range(lim):
        el = int(input("enter the element at {} index : ".format(i)))
        ls.append(el)
    i = 0
    positive = []
    sum = 0
    negative = []
    sum1 = 0
    while i<lim:
        if ls[i]>0:
            positive.append(ls[i])
            sum = sum+ls[i]
        elif ls[i]<0:
            negative.append(ls[i])
            sum1 = sum1+ls[i]
        i+=1
    print()
    print("the original list are :",ls)
    print()
    if positive == []:
        print("you are not insert any positve number")
    else:
        print(positive)
        print("\nthe total positive items are : ",sum)
    print()
    if negative == []:
        print("you are not insert any negative number")
    else: 
        print(negative)
        print("\nthe total negative items are : ",sum1)

    

def factor_finder():
    """
    This Python function takes an input number and prints all its factors along with their sum.
    """
    number = int(input("enter any number:"))
    print()
    i = 1
    sum = 0
    print("the factor of {} are as below".format(number))
    print()
    while i<=number:
        if number%i==0:
            print("\t",i)
            sum = sum+i
        i+=1
    print()
    print("the total factor of {} is : {}".format(number,sum))


def count_vowel_and_spaces():
    """
    This function counts the number of vowels and spaces in a given text input.
    """
    text = input("enter some text : ")
    ls = ['a','e','i','o','u','A','E','I','O','U']
    vowel = []
    count_vowel = 0
    count_spaces = 0
    for i in text:
        if i == " ":
            count_spaces+=1
        if i not in ls:
            continue
        else:
            vowel.append(i)
            count_vowel+=1

    print() 
    print("the original text is : ",text)
    print()
    print("the total number of vowels present in text is {} and the vowels are : {} ".format(count_vowel,vowel))
    print() 
    print("the total number of spaces present in text is : {}".format(count_spaces))


def prime_finder():
    """
    This Python function checks whether a given number is prime or not.
    """
    num = int(input("enter any number to check whether a given number is prime or not : "))
    if num<2:
        print("the given number {} is not a prime number".format(num))
    else:
        i = 2
        while i < num:
            if num%i==0:
                print("the given number {} is not a prime".format(num))
                break
            i+=1
        else:
            print("the given number {} is a prime".format(num))


def even_and_odd():
    """
    This Python function takes user input for a list of numbers, separates even and odd numbers, and
    then prints the lists of even and odd numbers.
    """
    lim = int(input("enter the limit of list : "))
    lst = []
    for i in range(lim):
        el = int(input("enter the element at {} index : ".format(i)))
        lst.append(el)
    even = []
    odd = []

    for item in lst:
        if item%2!=0:
            continue
        else:
            even.append(item)
    else:

        for item in lst:
            if item%2==0:
                continue
            else:
                odd.append(item)
    print()
    if even == []:
        print("even number is not given by the user in this list")
    else:
        print("List of even numbers are : ",even)
    print()
    if odd == []:
         print("odd number is not given by the user in this list")
    else:
        print("List of odd numbers are : ",odd)


def fibonacci_series():
    """
    The function `fibonacci_series` generates a Fibonacci series based on user input.
    """
    n = int(input("enter how many term you want in this series : "))
    first = 0
    seccond = 1
    for i in range(n):
        print(first,end=' ')
        temp = first
        first = seccond
        seccond+=temp

def selection_sort(arr: list[int]) -> list[int]:
    """ 
    Sorts a list of integers in ascending order using the selection sort algorithm.

    The selection sort algorithm divides the list into a sorted and an unsorted part.
    It repeatedly selects the smallest element from the unsorted part and swaps it 
    with the first element of the unsorted part, thus growing the sorted part by one.

    Args:
        arr (list[int]): A list of integers to be sorted.

    Returns:
        list[int]: The sorted list of integers in ascending order.

    Time Complexity:
        O(n^2) - where n is the number of elements in the list. 
        The algorithm performs well with small datasets but is inefficient for large datasets.

    Space Complexity:
        O(1) - because it sorts the list in place, using a constant amount of extra space.
    """
    for i in range(len(arr)):
        min_ele = i
        for j in range(i+1,len(arr)):
            if arr[min_ele] > arr[j]:
                min_ele = j
        # Swap
        temp: int = arr[min_ele]
        arr[min_ele] = arr[i]
        arr[i] = temp
    return arr

def palindrome_number_pattern(n: int) -> None:
    """
    Prints a pattern of numbers in the form of a palindrome triangle. The pattern
    starts with a pyramid shape of numbers, where each row contains numbers that
    first descend and then ascend symmetrically, creating a palindrome-like effect.

    Args:
        n (int): The number of rows in the pattern.

    The pattern includes:
        - Leading spaces that decrease with each row.
        - Numbers printed in descending order from the row index down to 1.
        - Numbers printed in ascending order from 2 up to the row index.

    Example:
        For n = 5, the output will be:

            1 
          2 1 2 
        3 2 1 2 3 
      4 3 2 1 2 3 4 
    5 4 3 2 1 2 3 4 5 

    Time Complexity:
        O(n^2) - Each row has a number of operations proportional to the row index.

    Space Complexity:
        O(1) - Constant space is used aside from the input and output.
    """
    for i in range(1, n + 1):  # Outer loop for rows
        # Inner loop for leading spaces
        for j in range(1, (n - i) + 1):
            print(" ", end=' ')
        # Inner loop for printing numbers in descending order
        for k in range(i, 0, -1):
            print(k, end=' ')
        # Inner loop for printing numbers in ascending order
        for l in range(2, i + 1):
            print(l, end=' ')
        # Move to the next line after each row
        print('\n')

