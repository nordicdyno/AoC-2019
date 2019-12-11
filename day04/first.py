def check_password1(pwd: int) -> bool:
    digits = [int(c) for c in str(pwd)]
    if len(digits) != 6:
        return False

    last_value = digits[0]
    has_dup = False
    for d in digits[1:]:
        if d < last_value:
            return False

        if not has_dup:
            has_dup = last_value == d
        last_value = d
    return has_dup



if __name__ == "__main__":
    checks, passed_check = 0, 0
    for w in range(372037, 905157+1):
        checks+=1
        if check_password1(w):
            passed_check += 1
            print(w, check_password1(w))
        # break
    print(f"result: {passed_check}/{checks}")
