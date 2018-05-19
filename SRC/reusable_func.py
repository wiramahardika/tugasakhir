def is_dominating(subject, target):
    dominate = 0
    for attr in attribute_value:
        if subject[attr] > target[attr]:
            return False
        elif subject[attr] < target[attr]:
            dominate+=1
    if dominate < 1:
        return False
    else:
        return True
