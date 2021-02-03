import json

# Format 
# h1: 2
# h2: 8
# N1: 4
# N2: 8
# vocabulary: 10
# length: 12
# calculated_length: 26.0
# volume: 39.863137138648355
# difficulty: 1.0
# effort: 39.863137138648355
# time: 2.2146187299249087
# bugs: 0.013287712379549451

VOC = 4
LEN = 5
CLEN = 6
VOL = 7
DIF = 8
EFF = 9
TIM = 10
BUG = 11

def promedio(jsondat, TIPO):
    s = 0
    for k in jsondat.keys():
        s += jsondat[k]["total"][TIPO]
    return s/len(jsondat.keys())

if __name__ == "__main__":
    with open("halstead.json", "r") as f:
        jsondat = json.load(f)

    print("\tHalstead Metrics: Average")
    print("[*] Files: " + str(len(jsondat.keys())))
    for i in jsondat.keys():
        print("- " + i)

    print("+-------------------+---------------------+")
    print("| METRIC            | AVERAGE             |")
    print("+-------------------+---------------------+")

    print("| vocabulary:        " + str(promedio(jsondat, VOC)) + " "*13 + "    |")
    print("| length:            " + str(promedio(jsondat, LEN)) + "    |")
    print("| calculated_length: " + str(promedio(jsondat, CLEN))+ "    |")
    print("| volume:            " + str(promedio(jsondat, VOL))+ "    |")
    print("| difficulty:        " + str(promedio(jsondat, DIF))+ "    |")
    print("| effort:            " + str(promedio(jsondat, EFF))+ "    |")
    print("| time:              " + str(promedio(jsondat, TIM))+ "    |")
    print("| bugs:              " + str(promedio(jsondat, BUG)) + " |")

    print("+-------------------+---------------------+")
# radon mi -s -m .
#         Halstead Metrics: Average
# [*] Files: 9
# - app\decorators.py
# - app\email.py
# - app\fake.py
# - app\models.py
# - app\auth\forms.py
# - app\auth\views.py
# - app\main\errors.py
# - app\main\forms.py
# - app\main\views.py
# +-------------------+---------------------+
# | METRIC            | AVERAGE             |
# +-------------------+---------------------+
# | vocabulary:        15.0                 |
# | length:            19.11111111111111    |
# | calculated_length: 65.10493151615515    |
# | volume:            97.09125383114674    |
# | difficulty:        1.582936507936508    |
# | effort:            437.6520622980183    |
# | time:              24.31400346100102    |
# | bugs:              0.032363751277048915 |
# +-------------------+---------------------+

# radon hal -e "*__init__.py" -j app > metrics\halstead.json


# config.py - A (53.91)
# dc19.py - A (66.47)
# testing-app.py - A (71.45)
# app\decorators.py - A (92.17)
# app\email.py - A (63.31)
# app\fake.py - A (69.65)
# app\models.py - A (26.78)
# app\__init__.py - A (100.00)
# app\auth\forms.py - A (100.00)
# app\auth\views.py - A (38.57)
# app\auth\__init__.py - A (100.00)
# app\main\errors.py - A (100.00)
# app\main\forms.py - A (67.23)
# app\main\views.py - A (71.27)
# app\main\__init__.py - A (100.00)
# metrics\main.py - A (72.46)
# migrations\env.py - A (100.00)
# migrations\versions\5cc3817a44eb_initial_migration.py - A (100.00)
# scripts\server_test.py - A (71.45)
# scripts\__init__.py - A (100.00)
# tests\test_basics.py - A (67.75)
# tests\test_login.py - A (100.00)
# tests\test_user_model.py - A (35.33)
# tests\__init__.py - A (100.00)