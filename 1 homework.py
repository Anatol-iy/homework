from collections import defaultdict
from datetime import datetime, timedelta

day_mapping = {
    0: "Monday",
    1: "Tuesday",
    2: "Wednesday",
    3: "Thursday",
    4: "Friday",
    5: "Saturday",
    6: "Sunday"
}
def get_birthdays_per_week(users):

    
    today = datetime.now().date()  # Отримуємо поточну дату
    
    birthdays_by_day = defaultdict(list)  # призначений для зберігання значень за неіснуючими ключами в словнику 
 
  
    for user in users:           # Перебираємо користувачів
        name = user["name"]
        birthday = user["birthday"].date()  # Конвертуємо до типу date
        birthday_this_year = birthday.replace(year=today.year) #рік змінюємо на сьогоднішій рік
        

        if birthday_this_year < today:  # Перевіряємо, чи вже минув день народження цього року
           birthday_this_year = birthday_this_year.replace(year=today.year + 1) # Розглядаємо дату на наступний рік
        
        delta_days = (birthday_this_year - today).days # Порівняння з Поточною Датою:

        #Визначення Дня Тижня: Визначаємо день тижня дня народження. Якщо це вихідний, переносимо на понеділок. 

        birthday_day_of_week = (today.weekday() + delta_days) % 7 if delta_days < 7 else 0
        
 
        if delta_days < 7:
            birthday_day_name = day_mapping[birthday_day_of_week]
            birthdays_by_day[birthday_day_name].append(name) #Зберігання Результату 

     # Користувачів з днями народження на вихідних привітаємо в понеділок
    if today.weekday() == 6:  #поточний день тижня є неділею, номери днів тижня починаються з 0, а неділя має номер 6
        birthdays_by_day["Monday"].extend(birthdays_by_day["Saturday"] + birthdays_by_day["Sunday"])# extend- добавляем в Понедельник
        birthdays_by_day["Saturday"] = []        # списки користувачів для суботи та неділі очищаються.
        birthdays_by_day["Sunday"] = []          #привітання для цих днів були перенесені на понеділок       
    
      # Виведення результатів
    for day, names in birthdays_by_day.items():
        if names:
            print(f"{day}: {', '.join(names)}")  #если есть имя, условие виконується, join - обєднує елементи в рядок, разделяє комой
        else:
            print(f"{day}: Немає днів народжень") 
users = [
    {"name": "katay Smian", "birthday": datetime(1988, 8, 9)},
    {"name": "Dima Okun", "birthday": datetime(1992, 3, 17)},
    {"name": "Sasha Leshiy", "birthday": datetime(1991, 2, 25)},
    {"name": "Lesha Vlas", "birthday": datetime(1993, 2, 26)},
]            

get_birthdays_per_week(users)