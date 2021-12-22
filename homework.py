from __future__ import annotations

from dataclasses import asdict, dataclass


@dataclass
class InfoMessage:
    """Training information message."""
    training_type: str
    duration: float  # hours
    distance: float  # km
    speed: float  # km/h
    calories: float  # Kcal

    message = ('Тип тренировки: {training_type}; Длительность: {duration:.3f} '
               'ч.; Дистанция: {distance:.3f} км; Ср. скорость: {speed:.3f} '
               'км/ч; Потрачено ккал: {calories:.3f}.')

    def get_message(self) -> str:
        return self.message.format(**asdict(self))


@dataclass
class Training:
    """Basic training class."""
    LEN_STEP: float = 0.65  # meters
    M_IN_KM: int = 1000  # meters

    def __init__(self, action: int, duration: float, weight: float) -> None:
        self.action = action
        self.duration = duration  # km
        self.weight = weight  # kg

    def get_distance(self) -> float:
        """Get the distance in km."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Get the average speed of movement."""
        return self.get_distance() / self.duration

    def get_spent_calories(self) -> float:
        """Get the number of calories consumed."""
        pass

    def show_training_info(self) -> InfoMessage:
        """Return the information message about the completed training."""
        result: InfoMessage = InfoMessage(type(self).__name__,
                                          self.duration,
                                          self.get_distance(),
                                          self.get_mean_speed(),
                                          self.get_spent_calories())
        return result


class Running(Training):
    """Training: running."""

    coeff_calorie_1 = 18
    coeff_calorie_2 = 20
    training_time_in_mints = 60  # minutes

    def __init__(self, action: int, duration: float, weight: float) -> None:
        super().__init__(action, duration, weight)

    def get_spent_calories(self) -> float:
        return ((self.coeff_calorie_1 * self.get_mean_speed()
                - self.coeff_calorie_2) * self.weight / self.M_IN_KM
                * (self.duration * self.training_time_in_mints))


class SportsWalking(Training):
    """Training: sports walking."""

    coeff_calorie_3 = 0.035
    coeff_calorie_4 = 0.029
    training_time_in_mints = 60  # minutes

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 height: float) -> None:
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        return (self.coeff_calorie_3 * self.weight
                + (self.get_mean_speed()**2 // self.height)
                * self.coeff_calorie_4
                * self.weight) * (self.duration * self.training_time_in_mints)


@dataclass
class Swimming(Training):
    """Training: swimming."""
    coeff_calorie_5 = 1.1
    coeff_calorie_6 = 2.0
    LEN_STEP = 1.38  # meters

    def __init__(self, action: int, duration: float, weight: float,
                 length_pool: int, count_pool: int) -> None:
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self):
        return (self.length_pool * self.count_pool / self.M_IN_KM
                / self.duration)

    def get_spent_calories(self) -> float:
        return ((self.get_mean_speed() + self.coeff_calorie_5)
                * self.coeff_calorie_6 * self.weight)


def read_package(workout_type: str, data: list[int]) -> Training:
    """Read the data received from the sensors."""
    read: dict = {
        'RUN': Running,
        'WLK': SportsWalking,
        'SWM': Swimming,
    }
    if workout_type not in read.keys():
        raise NameError("Type_Error")
    return read[workout_type](*data)


def main(training) -> None:
    """Main function."""
    info = training.show_training_info()
    print(info.get_message())


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
