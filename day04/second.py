def check_password2(pwd: int) -> bool:
    digits = [int(c) for c in str(pwd)]

    last_value = digits[0]
    series_length = 1
    has_dup = False
    for d in digits[1:]:
        if d < last_value:
            return False

        if d == last_value:
            series_length += 1
        else:
            has_dup = has_dup or (series_length == 2)
            series_length = 1
        last_value = d
    return has_dup or (series_length == 2)


if __name__ == "__main__":
    print("result:", len([w for w in range(372037, 905157+1) if check_password2(w)]))
