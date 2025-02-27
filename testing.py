def solution(s: str, c: str) -> int:
    # Find the first newline character to extract the header
    first_new_line = s.find('\n')
    # devide to headers
    headers = s[:first_new_line].split(',')
    #find c index
    c_index = headers.index(c)

    max_value = -9999

    # Scan the remaining string manually to avoid full list splits
    i = first_new_line + 1
    commas = 0
    while i < len(s):
        if s[i] == ',':
            commas += 1
            i += 1
            if commas == c_index:
                commas = 0
                if c_index == len(headers)-1:
                    value = int(s[i:s.find("\n", i)])
                else:
                    value = int(s[i:s.find(",", i)])
                if value > max_value:
                    max_value = value
                if s.find('\n', i) != -1:
                    i = s.find('\n',i) + 1
                else:
                    return max_value
        else:
            i += 1


     # Start reading after the first newline
      # Find next newline
       # If no more newlines, process till end of string

        # Extract the row
        # Move to the next row

        # Find the target column value efficiently without splitting the whole row
         # Found column separator or end of row
                # Capture last character if end of row
                     # Convert and update max
                  # Move start to next column


if __name__ == "__main__":
    # s = "id,name,age,room,dep\n1,jack,68,t,13.8\n17,betty,28,f,15.7"
    s = "id,name,age\n1,jack,68\n17,betty,28"
    c = "age"
    print(solution(s, c))
























    # first_newline = s.find("\n")
    # headers = s[:first_newline].split(",")  # Extract headers
    # column_index = headers.index(c)  # Find index of target column
    #
    # # Initialize max value
    # max_value = -9999
    #
    # # Scan the remaining string manually to avoid full list splits
    # start = first_newline + 1  # Start reading after the first newline
    # while start < len(s):
    #     end = s.find("\n", start)  # Find next newline
    #     if end == -1:
    #         end = len(s)  # If no more newlines, process till end of string
    #
    #     row = s[start:end]  # Extract the row
    #     start = end + 1  # Move to the next row
    #
    #     # Find the target column value efficiently without splitting the whole row
    #     col_start = 0
    #     col_end = 0
    #     col_count = 0
    #
    #     for i, char in enumerate(row):
    #         if char == "," or i == len(row) - 1:  # Found column separator or end of row
    #             if col_count == column_index:
    #                 col_end = i + (1 if i == len(row) - 1 else 0)  # Capture last character if end of row
    #                 max_value = max(max_value, int(row[col_start:col_end]))  # Convert and update max
    #                 break
    #             col_count += 1
    #             col_start = i + 1  # Move start to next column
    #
    # return max_value


def find_biggest_zeroz(N):
    binaryString = bin(N)
    print(binaryString)
    i = 0
    zeroz = 0
    new_zeroz = 0
    while i < len(binaryString):
        if binaryString[i] == '1' and i+1 < len(binaryString):
            while i+1 < len(binaryString) and binaryString[i+1] == '0':
                new_zeroz += 1
                i += 1
            if i+1 < len(binaryString) and binaryString[i+1] != '1':
                new_zeroz = 0
                i += 1
            if i+1 < len(binaryString) and binaryString[i+1] == '1':
                if new_zeroz > zeroz:
                    zeroz = new_zeroz
                    new_zeroz = 0
            i += 1
        else:
            i += 1
    return zeroz


