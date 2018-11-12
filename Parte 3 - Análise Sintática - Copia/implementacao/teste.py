def num(s):
        try:
            return int(s)
        except ValueError:
            return float(s)


if __name__ == "__main__":
    a = "10.85"
    b = "5"
    print(str(type(num(b))))
    
    