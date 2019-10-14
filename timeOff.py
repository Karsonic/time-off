from datetime import datetime, timedelta, date
from typing import List
from calendar import day_abbr

class VacationDays:
    """Helps plan use of available vacation days"""
    rate = 4.62
    period = timedelta(weeks=2)
    cost = 8

    def __init__(self, next_payday: date, starting_balance: float = 0,
                 planned_days_off: List[date] = None):
        self.next_payday = next_payday
        self.starting_balance = starting_balance
        self.planned_days_off = VacationDays._remove_weekends(planned_days_off)

    def plan(self, end_date: datetime) -> None:
        """Prints out information about the time being taken off
        
        Arguments:
            end_date {datetime} -- Date to plan up until

        Returns:
            None
        """
        current_day = datetime.today().date()
        next_payday = self.next_payday
        current_balance = self.starting_balance
        
        while (current_day < end_date):
            current_day += timedelta(days=1)

            if current_day >= next_payday:
                current_balance += VacationDays.rate
                next_payday += VacationDays.period
                print(f"Vacation days increased to {self._hours_to_days(current_balance):.2f} on {current_day}")

            if current_day in self.planned_days_off:
                if current_balance < VacationDays.cost:
                    print(f"WARNING: Ran out of vacation days on {current_day}. Next refill {next_payday}")
                current_balance -= VacationDays.cost
                print(f"Taking off {current_day}, reducing vacation days to {self._hours_to_days(current_balance):.2f}")
        
        print(f"Remaining balance is {self._hours_to_days(current_balance):.2f} days")

    def _hours_to_days(self, hours) -> float:
        """
        Converts vacation hours into vacation days based on vacation day cost
        """
        return hours / self.cost

    @staticmethod
    def _remove_weekends(days: List[date]) -> List[date]:
        """Filters out "free" vacation days

        Returns:
            List[date] -- The list of dates with Saturday and Sunday dates removed
        """
        return [day for day in days if day_abbr[day.weekday()] not in ['Sat', 'Sun']]


if __name__ == "__main__":
    # Sample
    next_payday = date(month=10, day=18, year=2019)
    end_date = date(month=6, day=30, year=2020)

    trip = date(month=12, day=13, year=2019)
    christmas = [date(month=12, day=23, year=2019), date(month=12, day=26, year=2019), date(month=12, day=27, year=2019)]
    days_off = [trip, *christmas]

    vd = VacationDays(next_payday, 20, days_off)
    days_text = (f"{d.month}/{d.day}" for d in vd.planned_days_off)
    print(f"Taking off {', '.join(days_text)}")
    vd.plan(end_date)