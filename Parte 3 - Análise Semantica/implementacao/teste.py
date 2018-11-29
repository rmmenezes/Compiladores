def num(s):
        try:
            return int(s)
        except ValueError:
            return float(s)


if __name__ == "__main__":
     
    a = "0"
    b = int(float(a))
    print (b)
    
    